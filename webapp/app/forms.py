from django.forms import ModelForm, TextInput
from django.contrib.auth.models import User
from django import forms

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email','first_name']

        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
                'placeholder':'ФИО пользователя'
            }),
            'email': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'password': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Пароль'
            })
        }