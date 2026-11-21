from django import forms
from .models import Student, Attendance

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["roll_number", "full_name", "email", "course", "semester"]
        widgets = {
            "roll_number": forms.TextInput(attrs={"placeholder": "e.g. BCA001"}),
            "full_name": forms.TextInput(attrs={"placeholder": "Student full name"}),
            "email": forms.EmailInput(attrs={"placeholder": "student@example.com"}),
        }

class AttendanceForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"]
    )
