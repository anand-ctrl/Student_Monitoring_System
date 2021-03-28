from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Users


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
