from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError


class MyUserCreationForm(UserCreationForm):
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class': 'validate', }))

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2',
                  'first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data['first_name']
        last_name = cleaned_data['last_name']
        if not first_name and not last_name:
            raise ValidationError('Пожалуйста, укажите имя или фамилию! ')
        return cleaned_data
