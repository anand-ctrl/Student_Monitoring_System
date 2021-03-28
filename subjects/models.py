from django.contrib.auth.models import User
from django.db import models
from jsonfield import JSONField


# Create your models here.

class subject(models.Model):
    subject_name = models.CharField(max_length=200)
    organised = models.BooleanField(default=False)
    stubborn = models.BooleanField(default=False)
    introvert = models.BooleanField(default=False)
    extrovert = models.BooleanField(default=False)
    agreeable = models.BooleanField(default=False)
    passive = models.BooleanField(default=False)
    creative = models.BooleanField(default=False)
    unpredictable = models.BooleanField(default=False)
    neurotic = models.BooleanField(default=False)
    versatility = models.BooleanField(default=False)
    regularity = models.BooleanField(default=False)
    efficiency = models.BooleanField(default=False)
    teamwork = models.BooleanField(default=False)
    memory = models.BooleanField(default=False)
    psa = models.BooleanField(default=False)
    business = models.BooleanField(default=False)
    management = models.BooleanField(default=False)
    technical = models.BooleanField(default=False)
    entrepreneur = models.BooleanField(default=False)
    path_finding = models.BooleanField(default=False)
    space = models.BooleanField(default=False)
    data_handling = models.BooleanField(default=False)


class suggested_subject(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    suggested_subjects = models.CharField(max_length=500)
