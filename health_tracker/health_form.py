from django import form

class HealthNote(forms.Form):
    name = forms.CharField(label = 'Как вас зовут?', max_length = 200)
    age = forms.DecimalField(label = 'Сколько вам лет?', max_digits = 3)
    pressureUP = forms.DecimalField(label = 'Какое у вас сиастолическое (верхнее) артериальное давление?', max_digits = 3)
    pressureDOWN = forms.DecimalField(label = 'Какое у вас диастлическое (нижнее) артериальное давление?', max_digits = 3)
    cholesterol = forms.DecimalField(label = 'Какой у вас уровень холестерина? (ммоль-л)')
    glucose = forms.DecimalField(label = 'Какой у вас уровень глюкозы? (ммоль/л)')
    sleep_time = forms.DecimalField(label = 'Какая у вас средняя продолжительность сна?')
    BMI = forms.DecimalField(label = 'Какой у вас индекс массы тела?')