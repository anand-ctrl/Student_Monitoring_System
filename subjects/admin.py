from django.contrib import admin

# Register your models here.
from subjects.models import subject, suggested_subject


class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "subject_name", "career", "organised", "stubborn", "introvert", "extrovert", "agreeable", "passive", "creative",
        "unpredictable", "neurotic", "versatility", "regularity", "efficiency", "teamwork", "teamwork", "psa",
        "business",
        "management",
        "technical", "entrepreneur", "path_finding", "space", "data_handling")


admin.site.register(subject, SubjectAdmin)


class SuggestedSubjectAdmin(admin.ModelAdmin):
    list_display = ('student', 'suggested_subjects')


admin.site.register(suggested_subject, SuggestedSubjectAdmin)
