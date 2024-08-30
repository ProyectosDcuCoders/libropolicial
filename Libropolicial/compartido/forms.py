# compartido/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese usuario',
        'class': 'form-control rounded-md pl-1'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese contraseña',
        'class': 'contra form-control rounded-md pl-1'
    }))
