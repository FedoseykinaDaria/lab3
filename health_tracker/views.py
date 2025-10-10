from django.shortcuts import render, redirect
from django.conf import settings
from django.http import FileResponse, Http404
from django.views.static import serve
from .health_form import HealthNote
from datetime import datetime
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
            return render(request, 'health_tracker/success.html')
    
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

#Загрузка файла
def UploadFile(request):
    if request.method == 'POST':
        form = UploadedFileForm(request.POST, request.FIELS)
        if form.is_valid():
            title = form.cleaned_data['title']
            uploaded_file = form.cleaned_data['file']

            ext = os.path.splitext(uploaded_file.name)[1]
            unique_name = f"{uuid.uuid4()}{ext}"
            file_path = os.path.join(settings.MEDIA_ROOT, unique_name)

            with open(file_path, 'wb+') as dest:
                for chunk in uploaded_file.chunks():
                    dest.write(chunk)

            save_file_metadata(
                filename = unique_name,
                original_name = uploaded_file.name,
                title = title,
                size = uploaded_file.size
            )
            return redirect('ListFiles')
    
    else:
        form = UploadedFileForm()
    
    return render(request, 'health_tracker/health_files.html', {'form': form})

def ListFiles():
    files = get_file_metadata()
    return render(request, 'health_tracker/health_home.html', {'files': files})

def DownloadFile(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    if os.path.exists(file.path):
        return serve(request, os.path.basename(file_path), os.path.dirname(file_path))
    else:
        raise Http404("Файл не найден")