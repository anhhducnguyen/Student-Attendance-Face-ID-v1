from django import forms
from .models import TblStudents

# class StudentForm(forms.ModelForm):
#     class Meta:
#         model = TblStudents
#         fields = ['student_id', 'name', 'email', 'phone', 'dateBirth']


# ==========================================================
class TblStudentsForm(forms.ModelForm):
    class Meta:
        model = TblStudents
        fields = ['name', 'email', 'phone', 'date_birth', 'classroom']
