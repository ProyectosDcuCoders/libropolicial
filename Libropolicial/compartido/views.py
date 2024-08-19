# compartido/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .forms import CustomLoginForm

def no_permission(request):
    return render(request, 'no_permission.html', {})

class HomeView(TemplateView):
    template_name = 'home.html'

class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomLoginForm

    def get_success_url(self):
        if self.request.user.groups.filter(name='comisariaprimera').exists():
            return reverse_lazy('comisaria_primera_list')
        elif self.request.user.groups.filter(name='comisariasegunda').exists():
            return reverse_lazy('comisaria_segunda_list')
        elif self.request.user.groups.filter(name='divisioncomunicaciones').exists():
            return reverse_lazy('divisioncomunicaciones_list')
        else:
            return reverse_lazy('no_permission')