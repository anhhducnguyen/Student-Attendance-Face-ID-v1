
from django.shortcuts import render
from .models import TblStudents


def studentsView(request):
    students = TblStudents.objects.all()
    return render(request, "admin/students.html", {'students': students})

def ok(request):
    return render(request,'ok.htm')
