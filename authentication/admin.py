from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import TblStudents

@admin.register(TblStudents)
class TblStudentsAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'email', 'phone', 'dateBirth')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('dateBirth',)

# or alternatively you can use admin.site.register() method
# admin.site.register(TblStudents, TblStudentsAdmin)
