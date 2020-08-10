from django import forms
from .models import *


class StatusForm(forms.Form):
    name = forms.ChoiceField(choices=STATUS_CHOICES, required=True, label='Тип', initial=DEFAULT_STATUS)


class TaskForm(forms.Form):
    title = forms.CharField(max_length=200, required=True, label='Заголовок')
    description = forms.CharField(max_length=3000, required=False, label='Описание', widget=forms.Textarea)
    date = forms.DateField(required=False, label='дата выполнения', widget=forms.DateInput(attrs={'type': 'date'}))
    type = forms.ModelMultipleChoiceField(queryset=Type.objects.all(), required=True, label='Тип',
                                          widget=forms.CheckboxSelectMultiple)
    status = forms.ModelChoiceField(queryset=Status.objects.all(), required=True, label='Статус', initial=DEFAULT_STATUS)

