from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import DivisionComunicaciones, EncargadoGuardia, PersonalGuardia, EventoGuardia
from .forms import DivisionComunicacionesForm, EventoGuardiaFormSet, EventoGuardiaBisFormSet, EventoGuardiaBisUnoFormSet

# Vista de la lista
class DivisionComunicacionesListView(ListView):
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

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['eventos_formset'] = EventoGuardiaFormSet(self.request.POST)
            data['eventos_bis_formset'] = EventoGuardiaBisFormSet(self.request.POST)
            data['eventos_bis_uno_formset'] = EventoGuardiaBisUnoFormSet(self.request.POST)
        else:
            data['eventos_formset'] = EventoGuardiaFormSet()
            data['eventos_bis_formset'] = EventoGuardiaBisFormSet()
            data['eventos_bis_uno_formset'] = EventoGuardiaBisUnoFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        eventos_formset = context['eventos_formset']
        eventos_bis_formset = context['eventos_bis_formset']
        eventos_bis_uno_formset = context['eventos_bis_uno_formset']

        # Guardar el formulario principal
        self.object = form.save()

        # Asignar la guardia a los formsets
        eventos_formset.instance = self.object
        eventos_bis_formset.instance = self.object
        eventos_bis_uno_formset.instance = self.object

        # Validar y guardar todos los formsets
        if (eventos_formset.is_valid() and
            eventos_bis_formset.is_valid() and
            eventos_bis_uno_formset.is_valid()):

            eventos_formset.save()
            eventos_bis_formset.save()
            eventos_bis_uno_formset.save()

            messages.success(self.request, 'Guardia y eventos guardados correctamente.')
            return redirect(self.success_url)
        else:
            # Imprimir los errores en la consola para depurar
            print(eventos_formset.errors, eventos_bis_formset.errors, eventos_bis_uno_formset.errors)
            return self.form_invalid(form)


class DivisionComunicacionesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = DivisionComunicaciones
    form_class = DivisionComunicacionesForm
    template_name = 'divisioncomunicaciones/divisioncomunicaciones_form.html'
    success_url = reverse_lazy('divisioncomunicaciones_list')

    def test_func(self):
        return self.request.user.groups.filter(name='divisioncomunicaciones').exists()

    def handle_no_permission(self):
        return redirect('no_permission')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['eventos_formset'] = EventoGuardiaFormSet(self.request.POST, instance=self.object)
            data['eventos_bis_formset'] = EventoGuardiaBisFormSet(self.request.POST, instance=self.object)
            data['eventos_bis_uno_formset'] = EventoGuardiaBisUnoFormSet(self.request.POST, instance=self.object)
        else:
            data['eventos_formset'] = EventoGuardiaFormSet(instance=self.object)
            data['eventos_bis_formset'] = EventoGuardiaBisFormSet(instance=self.object)
            data['eventos_bis_uno_formset'] = EventoGuardiaBisUnoFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        eventos_formset = context['eventos_formset']
        eventos_bis_formset = context['eventos_bis_formset']
        eventos_bis_uno_formset = context['eventos_bis_uno_formset']

        self.object = form.save()

        eventos_formset.instance = self.object
        eventos_bis_formset.instance = self.object
        eventos_bis_uno_formset.instance = self.object

        if (eventos_formset.is_valid() and
            eventos_bis_formset.is_valid() and
            eventos_bis_uno_formset.is_valid()):
            eventos_formset.save()
            eventos_bis_formset.save()
            eventos_bis_uno_formset.save()
            messages.success(self.request, 'Guardia y eventos actualizados correctamente.')
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)
