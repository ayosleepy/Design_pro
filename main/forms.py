from django import forms
from django.contrib.auth.forms import UserCreationForm
from main.models import CustomUser, Application
import re

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    consent = forms.BooleanField(
        required=True,
        label='Согласие на обработку персональных данных'
    )

    class Meta:
        model = CustomUser
        fields = ('fio', 'username', 'email', 'password1', 'password2', 'consent')
        widgets = {
            'fio': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'fio': 'ФИО',
            'username': 'Логин',
            'email': 'Email',
        }

    def clean_fio(self):
        fio = self.cleaned_data.get('fio')
        if not re.match(r'^[а-яА-ЯёЁ\s-]+$', fio):
            raise forms.ValidationError('ФИО должно содержать только кириллические буквы, пробелы и дефисы')
        return fio

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z-]+$', username):
            raise forms.ValidationError('Логин должен содержать только латинские буквы и дефисы')
        return username

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['title', 'description', 'category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название вашего проекта'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Опишите ваше помещение и пожелания к дизайну'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Название заявки',
            'description': 'Описание',
            'category': 'Категория',
            'image': 'Фото помещения или план',
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Размер файла не должен превышать 2 МБ')
        return image