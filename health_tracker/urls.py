from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage, name = 'HomePage'),
    path('form/', views.HealthForm, name = 'HealthForm'),
    path('file/', views.UploadedFileForm, name = "UploadedFileForm")
]