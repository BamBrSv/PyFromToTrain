from django import forms


class From_to_form(forms.Form):
    transport = forms.CharField(label='Тип заявки', max_length=255,)
    pointdep = forms.CharField(label='Дата', max_length=255,)
    pointdep1 = forms.CharField(label='Время', max_length=255, )
    pointdep2 = forms.CharField(label='ФИО заявителя', max_length=255, )
    pointdep3 = forms.CharField(label='Адресс', max_length=255, )
    pointarr = forms.CharField(label='Описание', max_length=255,)
