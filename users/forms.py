from django import forms
from django.contrib.auth.forms import UserCreationForm
from main.models import CustomUser
import re


class UserRegistrationForm(UserCreationForm):
    fio = forms.CharField(
        max_length=255,
        label='ФИО',
        help_text='Только кириллические буквы, дефис и пробелы',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        label='Логин',
        help_text='Только латиница и дефис',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Повтор пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    consent = forms.BooleanField(
        required=True,
        label='Согласие на обработку персональных данных',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = CustomUser
        fields = ['fio', 'username', 'email', 'password1', 'password2', 'consent']

    def clean_fio(self):
        fio = self.cleaned_data['fio']
        if not re.match(r'^[а-яА-ЯёЁ\s-]+$', fio):
            raise forms.ValidationError('ФИО должно содержать только кириллические буквы, пробелы и дефис')
        return fio

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[a-zA-Z-]+$', username):
            raise forms.ValidationError('Логин должен содержать только латинские буквы и дефис')
        return username