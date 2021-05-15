from django.contrib import admin
from .models import Student_Report


# Register your models here.

class Student_ReportAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject_marks', 'semester_marks')


admin.site.register(Student_Report, Student_ReportAdmin)
