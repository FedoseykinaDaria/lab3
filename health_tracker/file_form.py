from django import forms
import json

class UploadFile(forms.Form):
    title = forms.CharField(label = "Ввведите имя файла:", max_length=100)
    file = forms.FileField(label = "Загрузите свой файл:")

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')

        if not file.name.lower().endswith('.json'):
            raise forms.ValidationError("Непозволительный формат. Файл должен иметь расширение .json")
        
        try:
            file_data = uploaded_file.read().decode('utf-8')
            data = json.loads(file_data)
            
            if not isinstance(data, dict):
                raise forms.ValidationError("JSON должен иметь тип 'dict'")
            
            if isinstance(json_data, dict):
                expected_fields = ['name', 'age', 'pressureUP', 'pressureDOWN', 'cholesterol', 'glucose', 'sleep_time', 'BMI']
                if not any(field in json_data for field in expected_fields):
                    raise forms.ValidationError("Нарушена структура загружаемого файла")
            
            file.seek(0)
            
        except json.JSONDecodeError as e:
            raise forms.ValidationError(f"Ошибка в формате JSON: {str(e)}")
        except Exception as e:
            raise forms.ValidationError(f"Ошибка при чтении файла: {str(e)}")
        
        return file