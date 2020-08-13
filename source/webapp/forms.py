from django import forms
from .models import *
from django.core.exceptions import ValidationError

RESTRICTED_SYMBOLS = ['#', '$', '%', '&', '/', '^', '`', '{', '|', '}', '~']


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']


class TaskForm(forms.ModelForm):
    date = forms.DateField(required=False, label='дата выполнения',
                           widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Task
        fields = ['title', 'description', 'types', 'status']
        widgets = {'description': forms.Textarea,
                   'types': forms.CheckboxSelectMultiple}

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data['title']
        description = cleaned_data['description']
        for symbol in RESTRICTED_SYMBOLS:
            if symbol in title:
                raise ValidationError('The title contains prohibited characters! ')
        if title and description and title == description:
            raise ValidationError("Description of the task should not duplicate it's title!")
        return cleaned_data

