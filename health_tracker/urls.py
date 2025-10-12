from django.urls import path
from . import views

urlpatterns = [
    path('form/', views.HealthForm, name = 'HealthForm'),
    path('file/', views.UploadedFileForm, name = "UploadedFileForm")
]