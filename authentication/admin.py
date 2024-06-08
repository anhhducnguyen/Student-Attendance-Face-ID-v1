from django.contrib import admin
from .models import TblStudents
from .models import Classroom

@admin.register(TblStudents)
class TblStudentsAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'email', 'phone', 'date_birth', 'classroom')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('date_birth', 'classroom')

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('class_id', 'class_name', 'teacher_name')
    search_fields = ('class_name', 'teacher_name')

