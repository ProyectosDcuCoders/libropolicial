from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import DivisionComunicaciones, EncargadoGuardia, PersonalGuardia
from .forms import DivisionComunicacionesForm

class DivisionComunicacionesListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = DivisionComunicaciones
    template_name = 'divisioncomunicaciones/divisioncomunicaciones_list.html'

    def test_func(self):
        return self.request.user.groups.filter(name='divisioncomunicaciones').exists()

    def handle_no_permission(self):
        return redirect('no_permission')

class DivisionComunicacionesCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = DivisionComunicaciones
    form_class = DivisionComunicacionesForm
    template_name = 'divisioncomunicaciones/divisioncomunicaciones_form.html'
    success_url = reverse_lazy('divisioncomunicaciones_list')

    def test_func(self):
        return self.request.user.groups.filter(name='divisioncomunicaciones').exists()

    def handle_no_permission(self):
        return redirect('no_permission')

    def form_valid(self, form):
        response = super().form_valid(form)
        description = form.instance.descripcion
        solicitante = form.instance.solicitante
        # Guardar mensaje en la sesión para comisarías
        self.request.session['comisarias_notification'] = {
            'description': description,
            'solicitante': solicitante
        }
        messages.success(self.request, f"Descripción: {description}, Solicitante: {solicitante}")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['encargados'] = EncargadoGuardia.objects.all()
        context['personales'] = PersonalGuardia.objects.all()
        return context

class DivisionComunicacionesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = DivisionComunicaciones
    form_class = DivisionComunicacionesForm
    template_name = 'divisioncomunicaciones/divisioncomunicaciones_form.html'
    success_url = reverse_lazy('divisioncomunicaciones_list')

    def test_func(self):
        return self.request.user.groups.filter(name='divisioncomunicaciones').exists()

    def handle_no_permission(self):
        return redirect('no_permission')

    def form_valid(self, form):
        response = super().form_valid(form)
        description = form.instance.descripcion
        solicitante = form.instance.solicitante
        # Guardar mensaje en la sesión para comisarías
        self.request.session['comisarias_notification'] = {
            'description': description,
            'solicitante': solicitante
        }
        messages.success(self.request, f"Descripción: {description}, Solicitante: {solicitante}")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['encargados'] = EncargadoGuardia.objects.all()
        context['personales'] = PersonalGuardia.objects.all()
        return context
