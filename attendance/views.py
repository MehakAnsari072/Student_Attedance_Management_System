from datetime import date
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Attendance
from .forms import StudentForm

def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("login")

def user_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        messages.error(request, "Invalid username or password.")
    return render(request, "attendance/login.html")

@login_required
def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return redirect("dashboard")

@login_required
def dashboard(request):
    today = date.today()
    total_students = Student.objects.count()
    today_records = Attendance.objects.filter(date=today)
    present_today = today_records.filter(status="Present").count()
    absent_today = today_records.filter(status="Absent").count()
    context = {
        "total_students": total_students,
        "present_today": present_today,
        "absent_today": absent_today,
        "not_marked": max(total_students - today_records.count(), 0),
        "today": today,
        "recent_records": Attendance.objects.select_related("student")[:8],
    }
    return render(request, "attendance/dashboard.html", context)

@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, "attendance/student_list.html", {"students": students})

@login_required
def student_add(request):
    form = StudentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Student added successfully.")
        return redirect("student_list")
    return render(request, "attendance/student_form.html", {"form": form, "heading": "Add Student"})

@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Student details updated.")
        return redirect("student_list")
    return render(request, "attendance/student_form.html", {"form": form, "heading": "Edit Student"})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted.")
        return redirect("student_list")
    return render(request, "attendance/confirm_delete.html", {"student": student})

@login_required
def mark_attendance(request):
    selected_date = request.POST.get("date") or request.GET.get("date") or date.today().isoformat()
    students = Student.objects.all()
    if request.method == "POST" and request.POST.get("save_attendance"):
        with transaction.atomic():
            for student in students:
                status_value = request.POST.get(f"status_{student.id}")
                if status_value in ("Present", "Absent"):
                    Attendance.objects.update_or_create(
                        student=student,
                        date=selected_date,
                        defaults={"status": status_value},
                    )
        messages.success(request, f"Attendance saved for {selected_date}.")
        return redirect(f"/attendance/mark/?date={selected_date}")

    existing = {
        item.student_id: item.status
        for item in Attendance.objects.filter(date=selected_date)
    }
    return render(request, "attendance/mark_attendance.html", {
        "students": students,
        "selected_date": selected_date,
        "existing": existing,
    })

@login_required
def attendance_records(request):
    records = Attendance.objects.select_related("student").all()
    selected_date = request.GET.get("date")
    if selected_date:
        records = records.filter(date=selected_date)
    return render(request, "attendance/attendance_records.html", {
        "records": records,
        "selected_date": selected_date or "",
        "students": Student.objects.all(),
    })
