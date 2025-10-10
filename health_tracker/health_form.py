from django import forms

class HealthNote(forms.Form):
    name = forms.CharField(label = 'Как вас зовут?', max_length = 200)
    age = forms.IntegerField(label = 'Сколько вам лет?', min_value = 1)
    pressureUP = forms.IntegerField(label = 'Какое у вас сиастолическое (верхнее) артериальное давление?', min_value = 0)
    pressureDOWN = forms.IntegerField(label = 'Какое у вас диастлическое (нижнее) артериальное давление?', min_value = 0)
    cholesterol = forms.IntegerField(label = 'Какой у вас уровень холестерина? (ммоль-л)', min_value = 0)
    glucose = forms.IntegerField(label = 'Какой у вас уровень глюкозы? (ммоль/л)', min_value = 0)
    sleep_time = forms.IntegerField(label = 'Какая у вас средняя продолжительность сна?', min_value = 0)
    BMI = forms.IntegerField(label = 'Какой у вас индекс массы тела?', min_value = 0)