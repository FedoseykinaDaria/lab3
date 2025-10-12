from django.shortcuts import render, redirect
from django.conf import settings
from django.http import FileResponse, HttpResponseRedirect
from django.views.static import serve

from .health_form import HealthNote
from .file_form import UploadFile

import os
import uuid
import json

#Сохранение данных с формы пользователя
def SaveUserData(data):
    folder_path = os.path.join(settings.BASE_DIR, 'Health')
    os.makedirs(folder_path, exist_ok = True)

    file_path = os.path.join(folder_path, 'health.json')
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump([], f)
    
    with open(file_path, 'r+', encoding='utf') as f:
        health = json.load(f)
        health.append(data)
        f.seek(0)
        json.dump(health, f, ensure_ascii = False, indent = 4)

#Загрузка формы
def HealthForm(request):
    if request.method == 'POST':
        form = HealthNote(request.POST)
        if form.is_valid():
            SaveUserData(form.cleaned_data)
            return HttpResponseRedirect('/')
    
    else: 
        form = HealthNote()
    
    return render(request, 'health_tracker/health_form.html', {'form': form})

#Загрузка списка записей на домашнюю страницу
def HealthList(request):
    file_path = os.path.join(settings.BASE_DIR, 'Health', 'health.json')
    health_notes = []

    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            health_notes = json.load(f)
    
    return render(request, 'health_tracker/health_home.html', {'health_notes': health_notes})

#Зарузка формы загрузки файла
def UploadedFileForm(request):
    if request.method == 'POST':
        form = UploadFile(request.POST, request.FILES)
        if form.is_valid():
            HandleUploadedFile(form.cleaned_data['file'])
            return HttpResponseRedirect('/')

    else:
        form = UploadFile()

    return render(request, 'health_tracker/health_files.html', {'form': form})

#Запись файла на сервер
def HandleUploadedFile(f):
    name = f.name
    ext = ''

    if '.' in name:
        ext = name[name.rindex('.'):]
        name = name[:name.rindex('.')]

    unique_name = str(uuid.uuid4())
    with open(f"Health/{name}_{unique_name}{ext}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

#Загрузка домашней страницы
def HomePage(request):
    folder_path = os.path.join(settings.BASE_DIR, 'Health')

    files = []
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            files.append(file)

    return render(request, 'health_tracker/health_home.html', {'files': files})
