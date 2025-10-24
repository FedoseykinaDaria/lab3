from django.shortcuts import render, redirect
from django.conf import settings
from django.http import FileResponse, HttpResponseRedirect
from django.views.static import serve

from .health_form import HealthNote
from .file_form import UploadFile

import os
import uuid
import json

folder_path = os.path.join(settings.BASE_DIR, 'Health')
file_names = {}

#Сохранение данных с формы пользователя
def SaveUserData(data):
    os.makedirs(folder_path, exist_ok = True)

    file_name = FileName('.json')

    file_path = os.path.join(folder_path, 'health.json')
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump({}, f)
    
    with open(file_path, 'r+', encoding='utf-8') as f:
        health = dict(json.load(f))
        data['title'] =  "HealthNote_" + data['name'] 
        health[file_name] = data
        f.seek(0, 0)
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

#Зарузка формы загрузки файла
def UploadedFileForm(request):
    if request.method == 'POST':
        form = UploadFile(request.POST, request.FILES)
        if form.is_valid():
            HandleUploadedFile(form.cleaned_data, request.FILES['file'])
            return HttpResponseRedirect('/')

    else:
        form = UploadFile()

    return render(request, 'health_tracker/health_files.html', {'form': form})

#Запись файла на сервер
def HandleUploadedFile(data, upload_file):
    upload_file.seek(0)
    upload_data = upload_file.read().decode('utf-8')
    
    new_data = json.loads(upload_data)

    file_path = os.path.join(folder_path, 'health.json')

    os.makedirs(folder_path, exist_ok = True)

    with open(file_path, 'r', encoding='utf-8') as f:
        existing_data = dict(json.load(f))

    if isinstance(new_data, dict):
        for key, value in new_data.items():
            unique_name = FileName('.json')
            existing_data[unique_name] = value
            value['title'] = data['user_title']
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii = False, indent = 4)

#Загрузка домашней страницы
def HomePage(request):
    file_path = os.path.join(folder_path, 'health.json')

    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump({}, f)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        health = dict(json.load(f))
        for key, value in health.items():
            file_names[key] = value['title']

    return render(request, 'health_tracker/health_home.html', {'file_names': file_names})

#Передача информации о файле
def JSONInfo(request, name):
    file_path = os.path.join(settings.BASE_DIR, 'Health', 'health.json')

    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return render(request, 'health_tracker/json_info.html', {'name': name, 'data': data, 'user_name':file_names[name]})
        except:
            return render(request, 'health_tracker/json_info.html', {'name': name, 'error': 'Ошибка чтения'})
    else:
        return render(request, 'health_tracker/json_info.html', {'name': name, 'error': 'Файл не найден'})

#Генерация уникального имения для файла
def FileName(file):
    if type(file) == str:
        ext = file
    else:
        filename = file.name
        ext = ''

        if '.' in filename:
            ext = filename[filename.rindex('.'):]

    unique_name = str(uuid.uuid4())
    
    return f"{unique_name}{ext}"
