from django.contrib import admin
from .models import Student, Attendance

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("roll_number", "full_name", "course", "semester", "email")
    search_fields = ("roll_number", "full_name", "email")
    list_filter = ("course", "semester")

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "date", "status")
    list_filter = ("date", "status")
    search_fields = ("student__roll_number", "student__full_name")
