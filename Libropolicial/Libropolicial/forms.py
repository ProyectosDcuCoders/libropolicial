# Libropolicial/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese usuario',
        'class': 'border rounded p-2 w-full'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese contraseña',
        'class': 'border rounded p-2 w-full'
    }))
