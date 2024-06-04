from django.db import models

class TblStudents(models.Model):
    student_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    dateBirth = models.DateField()



