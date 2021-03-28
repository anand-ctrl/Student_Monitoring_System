from django.contrib import admin

# Register your models here.
from init_test.models import test, student_score


class TestAdmin(admin.ModelAdmin):
    list_display = ("question", "option1", "option2", "option3", "option4")


class Student_ScoreAdmin(admin.ModelAdmin):
    list_display = (
        "student", "organised", "stubborn", "introvert", "extrovert", "agreeable", "passive", "creative",
        "unpredictable", "neurotic", "versatility", "regularity", "efficiency", "teamwork", "teamwork", "psa", "business",
        "management",
        "technical", "entrepreneur", "path_finding", "space", "data_handling")


admin.site.register(test, TestAdmin)
admin.site.register(student_score, Student_ScoreAdmin)
