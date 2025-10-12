from django import forms

class UploadFile(forms.Form):
    title = forms.CharField(label = "Ввведите имя файла:", max_length=100)
    file = forms.FileField(label = "Загрузите свой файл:")

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')

        name = file.name
        if name[name.rindex('.'):] != '.json':
            raise forms.ValidationError("Непозволительное разрешение файла. Проверьте, что загуржаемый вами файл имеет разрешение .json")