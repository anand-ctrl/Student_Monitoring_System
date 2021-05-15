from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('submitproject/', views.submitproject, name="submitproject"),
    path('feedback/', views.feed, name="feed"),
    path('academics/', views.academics, name="academics"),
]
