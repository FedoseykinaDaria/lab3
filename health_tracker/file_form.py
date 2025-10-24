from django import forms
import json

class UploadFile(forms.Form):
    user_title = forms.CharField(label = "Ввведите имя файла:", max_length=100)
    file = forms.FileField(label = "Загрузите свой файл:")

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')

        if not file.name.lower().endswith('.json'):
            raise forms.ValidationError("Непозволительный формат. Файл должен иметь расширение .json")
        
        try:
            file_data = file.read().decode('utf-8')
            data = json.loads(file_data)
            
            if not isinstance(data, dict):
                raise forms.ValidationError("Данные в файле должны иметь тип 'dict'")
            
            for key, value in data.items():
                if isinstance(value, dict):
                    fields = ["name", "age", "pressureUP", "pressureDOWN", "cholesterol", "glucose", "sleep_time", "BMI", "title"]
                    error = ""
                    for f in fields:
                        if f not in value:
                            error = error + ', ' + f
            if len(error) != 0:
                error = "В файле отсутствуют значения полей: " + error
                raise forms.ValidationError(error)
            
            file.seek(0)
            
        except json.JSONDecodeError as e:
            raise forms.ValidationError(f"Ошибка в формате JSON: {str(e)}")
        except Exception as e:
            raise forms.ValidationError(f"Ошибка при чтении файла: {str(e)}")