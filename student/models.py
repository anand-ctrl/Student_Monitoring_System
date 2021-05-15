from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Student_Report(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    subject_marks = models.JSONField()
    semester_marks = models.JSONField()
