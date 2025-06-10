from django.contrib import admin
from django.urls import path
from .views import performance_analysis
from . import views

urlpatterns = [
    path('analysis/<int:student_id>/', performance_analysis),
]
