from datetime import datetime
from io import BytesIO
from django.http import JsonResponse, HttpResponse, HttpRequest, FileResponse
from django.core.serializers import serialize
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.db import models
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

from Libropolicial.settings import MEDIA_ROOT
from .models import ComisariaPrimera, ComisariaSegunda, ComisariaTercera, ComisariaCuarta, ComisariaQuinta, DependenciasSecundarias, CodigoPolicialUSH, DetalleServicioEmergencia, DetalleInstitucionHospitalaria,DetalleDependenciaMunicipal, DetalleDependenciaProvincial
from .forms import ComisariaPrimeraForm, ComisariaSegundaForm, ComisariaTerceraForm, ComisariaCuartaForm, ComisariaQuintaForm, CustomLoginForm
from compartido.utils import user_is_in_group
import json
from django.core.serializers.json import DjangoJSONEncoder


@login_required
def sign_comisaria_primera(request, pk):
    comisaria = get_object_or_404(ComisariaPrimera, pk=pk)
    user_full_name = request.user.get_full_name() or request.user.username
    if comisaria.firmas:
        comisaria.firmas += f", {user_full_name}"
    else:
        comisaria.firmas = user_full_name
    comisaria.save(update_fields=['firmas'])  # Solo actualiza el campo firmas
    return redirect(reverse('comisaria_primera_list'))

# Función para firmar en Comisaria Segunda
@login_required
def sign_comisaria_segunda(request, pk):
    comisaria = get_object_or_404(ComisariaSegunda, pk=pk)
    user_full_name = request.user.get_full_name() or request.user.username
    if comisaria.firmas:
        comisaria.firmas += f", {user_full_name}"
    else:
        comisaria.firmas = user_full_name
    comisaria.save(update_fields=['firmas'])  # Solo actualiza el campo firmas
    return redirect(reverse('comisaria_segunda_list'))

# Función para firmar en Comisaria Tercera
@login_required
def sign_comisaria_tercera(request, pk):
    comisaria = get_object_or_404(ComisariaTercera, pk=pk)
    user_full_name = request.user.get_full_name() or request.user.username
    if comisaria.firmas:
        comisaria.firmas += f", {user_full_name}"
    else:
        comisaria.firmas = user_full_name
    comisaria.save(update_fields=['firmas'])  # Solo actualiza el campo firmas
    return redirect(reverse('comisaria_tercera_list'))

# Función para firmar en Comisaria Cuarta
@login_required
def sign_comisaria_cuarta(request, pk):
    comisaria = get_object_or_404(ComisariaCuarta, pk=pk)
    user_full_name = request.user.get_full_name() or request.user.username
    if comisaria.firmas:
        comisaria.firmas += f", {user_full_name}"
    else:
        comisaria.firmas = user_full_name
    comisaria.save(update_fields=['firmas'])  # Solo actualiza el campo firmas
    return redirect(reverse('comisaria_cuarta_list'))

# Función para firmar en Comisaria Quinta
@login_required
def sign_comisaria_quinta(request, pk):
    comisaria = get_object_or_404(ComisariaQuinta, pk=pk)
    user_full_name = request.user.get_full_name() or request.user.username
    if comisaria.firmas:
        comisaria.firmas += f", {user_full_name}"
    else:
        comisaria.firmas = user_full_name
    comisaria.save(update_fields=['firmas'])  # Solo actualiza el campo firmas
    return redirect(reverse('comisaria_quinta_list'))


# views.py

class ComisariaPrimeraListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ComisariaPrimera
    template_name = 'comisarias/primera/comisaria_primera_list.html'
    context_object_name = 'records'

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariaprimera')

    def handle_no_permission(self):
        return redirect('no_permission')

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-fecha_hora')
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(cuarto__cuarto__icontains=search_query)
        for comisaria in queryset:
            if timezone.is_naive(comisaria.fecha_hora):
                comisaria.fecha_hora = timezone.make_aware(comisaria.fecha_hora, timezone.get_current_timezone())
            comisaria.fecha_hora = timezone.localtime(comisaria.fecha_hora)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_jefessuperiores'] = self.request.user.groups.filter(name='jefessuperiores').exists()
        context['today'] = timezone.now().date()
        context['resolveId'] = None  # Inicializa resolveId en None
        return context

   


class ComisariaPrimeraCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ComisariaPrimera
    form_class = ComisariaPrimeraForm
    template_name = 'comisarias/primera/comisaria_primera_form.html'
    success_url = reverse_lazy('comisaria_primera_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariaprimera')

    def handle_no_permission(self):
        return redirect('no_permission')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['codigos_policiales'] = CodigoPolicialUSH.objects.all()
        context['dependencias_secundarias'] = DependenciasSecundarias.objects.all()

        # Inicializar detalles como listas vacías en el contexto
        context['detalle_servicios_emergencia'] = json.dumps([])  # Para vista de creación, siempre es una lista vacía
        context['detalle_instituciones_hospitalarias'] = json.dumps([])
        context['detalle_dependencias_municipales'] = json.dumps([])
        context['detalle_dependencias_provinciales'] = json.dumps([])

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.updated_by = None
        self.object.updated_at = None

        latitude = self.request.POST.get('latitude').replace(',', '.')
        longitude = self.request.POST.get('longitude').replace(',', '.')

        self.object.latitude = float(latitude) if latitude else None
        self.object.longitude = float(longitude) if longitude else None

        self.object.save()
        form.save_m2m()

        # Guardar los detalles adicionales para cada servicio de emergencia
        for servicio in form.cleaned_data['servicios_emergencia']:
            numero_movil_bomberos = self.request.POST.get(f'numero_movil_bomberos_{servicio.id}')
            nombre_a_cargo_bomberos = self.request.POST.get(f'nombre_a_cargo_bomberos_{servicio.id}')
            if numero_movil_bomberos or nombre_a_cargo_bomberos:
                DetalleServicioEmergencia.objects.create(
                    servicio_emergencia=servicio,
                    comisaria_primera=self.object,
                    numero_movil_bomberos=numero_movil_bomberos,
                    nombre_a_cargo_bomberos=nombre_a_cargo_bomberos
                )

        # Guardar los detalles adicionales para cada institución hospitalaria
        for institucion in form.cleaned_data['instituciones_hospitalarias']:
            numero_movil_hospital = self.request.POST.get(f'numero_movil_hospital_{institucion.id}')
            nombre_a_cargo_hospital = self.request.POST.get(f'nombre_a_cargo_hospital_{institucion.id}')
            if numero_movil_hospital or nombre_a_cargo_hospital:
                DetalleInstitucionHospitalaria.objects.create(
                    institucion_hospitalaria=institucion,
                    comisaria_primera=self.object,
                    numero_movil_hospital=numero_movil_hospital,
                    nombre_a_cargo_hospital=nombre_a_cargo_hospital
                )

        # Guardar los detalles adicionales para cada dependencia municipal
        for dependencia_municipal in form.cleaned_data['dependencias_municipales']:
            numero_movil_municipal = self.request.POST.get(f'numero_movil_municipal_{dependencia_municipal.id}')
            nombre_a_cargo_municipal = self.request.POST.get(f'nombre_a_cargo_municipal_{dependencia_municipal.id}')
            if numero_movil_municipal or nombre_a_cargo_municipal:
                DetalleDependenciaMunicipal.objects.create(
                    dependencia_municipal=dependencia_municipal,
                    comisaria_primera=self.object,
                    numero_movil_municipal=numero_movil_municipal,
                    nombre_a_cargo_municipal=nombre_a_cargo_municipal
                )

        # Guardar los detalles adicionales para cada dependencia provincial
        for dependencia_provincial in form.cleaned_data['dependencias_provinciales']:
            numero_movil_provincial = self.request.POST.get(f'numero_movil_provincial_{dependencia_provincial.id}')
            nombre_a_cargo_provincial = self.request.POST.get(f'nombre_a_cargo_provincial_{dependencia_provincial.id}')
            if numero_movil_provincial or nombre_a_cargo_provincial:
                DetalleDependenciaProvincial.objects.create(
                    dependencia_provincial=dependencia_provincial,
                    comisaria_primera=self.object,
                    numero_movil_provincial=numero_movil_provincial,
                    nombre_a_cargo_provincial=nombre_a_cargo_provincial
                )

        return super().form_valid(form)


class ComisariaPrimeraUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ComisariaPrimera
    form_class = ComisariaPrimeraForm
    template_name = 'comisarias/primera/comisaria_primera_form.html'
    success_url = reverse_lazy('comisaria_primera_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariaprimera')

    def handle_no_permission(self):
        return redirect('no_permission')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        now = timezone.now()

        if obj.fecha_hora.date() != now.date() and not obj.estado:
            return redirect('comisaria_primera_list')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['codigos_policiales'] = CodigoPolicialUSH.objects.all()
        context['dependencias_secundarias'] = DependenciasSecundarias.objects.all()

        # Convertir detalles en JSON para ser usados por Alpine.js
        context['detalle_servicios_emergencia'] = json.dumps(list(
            DetalleServicioEmergencia.objects.filter(comisaria_primera=self.object.pk).values('id', 'servicio_emergencia_id', 'numero_movil_bomberos', 'nombre_a_cargo_bomberos')
        ))

        context['detalle_instituciones_hospitalarias'] = json.dumps(list(
            DetalleInstitucionHospitalaria.objects.filter(comisaria_primera=self.object.pk).values('id', 'institucion_hospitalaria_id', 'numero_movil_hospital', 'nombre_a_cargo_hospital')
        ))

        context['detalle_dependencias_municipales'] = json.dumps(list(
            DetalleDependenciaMunicipal.objects.filter(comisaria_primera=self.object.pk).values('id', 'dependencia_municipal_id', 'numero_movil_municipal', 'nombre_a_cargo_municipal')
        ))

        context['detalle_dependencias_provinciales'] = json.dumps(list(
            DetalleDependenciaProvincial.objects.filter(comisaria_primera=self.object.pk).values('id', 'dependencia_provincial_id', 'numero_movil_provincial', 'nombre_a_cargo_provincial')
        ))

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_by = self.request.user
        self.object.updated_at = timezone.now()

        latitude = self.request.POST.get('latitude').replace(',', '.')
        longitude = self.request.POST.get('longitude').replace(',', '.')

        self.object.latitude = float(latitude) if latitude else None
        self.object.longitude = float(longitude) if longitude else None

        self.object.save()
        form.save_m2m()

        # Mantener un registro de los IDs seleccionados
        servicios_emergencia_ids = form.cleaned_data['servicios_emergencia'].values_list('id', flat=True)
        instituciones_hospitalarias_ids = form.cleaned_data['instituciones_hospitalarias'].values_list('id', flat=True)
        dependencias_municipales_ids = form.cleaned_data['dependencias_municipales'].values_list('id', flat=True)
        dependencias_provinciales_ids = form.cleaned_data['dependencias_provinciales'].values_list('id', flat=True)

        # Eliminar los detalles que ya no están seleccionados
        DetalleServicioEmergencia.objects.filter(comisaria_primera=self.object).exclude(servicio_emergencia_id__in=servicios_emergencia_ids).delete()
        DetalleInstitucionHospitalaria.objects.filter(comisaria_primera=self.object).exclude(institucion_hospitalaria_id__in=instituciones_hospitalarias_ids).delete()
        DetalleDependenciaMunicipal.objects.filter(comisaria_primera=self.object).exclude(dependencia_municipal_id__in=dependencias_municipales_ids).delete()
        DetalleDependenciaProvincial.objects.filter(comisaria_primera=self.object).exclude(dependencia_provincial_id__in=dependencias_provinciales_ids).delete()

        # Guardar los detalles adicionales para cada servicio de emergencia
        for servicio in form.cleaned_data['servicios_emergencia']:
            numero_movil_bomberos = self.request.POST.get(f'numero_movil_bomberos_{servicio.id}')
            nombre_a_cargo_bomberos = self.request.POST.get(f'nombre_a_cargo_bomberos_{servicio.id}')
            DetalleServicioEmergencia.objects.update_or_create(
                servicio_emergencia=servicio,
                comisaria_primera=self.object,
                defaults={
                    'numero_movil_bomberos': numero_movil_bomberos,
                    'nombre_a_cargo_bomberos': nombre_a_cargo_bomberos
                }
            )

        # Guardar los detalles adicionales para cada institución hospitalaria
        for institucion in form.cleaned_data['instituciones_hospitalarias']:
            numero_movil_hospital = self.request.POST.get(f'numero_movil_hospital_{institucion.id}')
            nombre_a_cargo_hospital = self.request.POST.get(f'nombre_a_cargo_hospital_{institucion.id}')
            DetalleInstitucionHospitalaria.objects.update_or_create(
                institucion_hospitalaria=institucion,
                comisaria_primera=self.object,
                defaults={
                    'numero_movil_hospital': numero_movil_hospital,
                    'nombre_a_cargo_hospital': nombre_a_cargo_hospital
                }
            )

        # Guardar los detalles adicionales para cada dependencia municipal
        for dependencia_municipal in form.cleaned_data['dependencias_municipales']:
            numero_movil_municipal = self.request.POST.get(f'numero_movil_municipal_{dependencia_municipal.id}')
            nombre_a_cargo_municipal = self.request.POST.get(f'nombre_a_cargo_municipal_{dependencia_municipal.id}')
            DetalleDependenciaMunicipal.objects.update_or_create(
                dependencia_municipal=dependencia_municipal,
                comisaria_primera=self.object,
                defaults={
                    'numero_movil_municipal': numero_movil_municipal,
                    'nombre_a_cargo_municipal': nombre_a_cargo_municipal
                }
            )

        # Guardar los detalles adicionales para cada dependencia provincial
        for dependencia_provincial in form.cleaned_data['dependencias_provinciales']:
            numero_movil_provincial = self.request.POST.get(f'numero_movil_provincial_{dependencia_provincial.id}')
            nombre_a_cargo_provincial = self.request.POST.get(f'nombre_a_cargo_provincial_{dependencia_provincial.id}')
            DetalleDependenciaProvincial.objects.update_or_create(
                dependencia_provincial=dependencia_provincial,
                comisaria_primera=self.object,
                defaults={
                    'numero_movil_provincial': numero_movil_provincial,
                    'nombre_a_cargo_provincial': nombre_a_cargo_provincial
                }
            )

        return super().form_valid(form)




# Vistas de listado y creación para ComisariaSegunda, ComisariaTercera, ComisariaCuarta, y ComisariaQuinta


class ComisariaSegundaListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ComisariaSegunda
    template_name = 'comisarias/segunda/comisaria_segunda_list.html'
    context_object_name = 'records'

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariasegunda')

    def handle_no_permission(self):
        return redirect('no_permission')
    

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-fecha_hora')
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(cuarto__cuarto__icontains=search_query)
        for comisaria in queryset:
            if timezone.is_naive(comisaria.fecha_hora):
                comisaria.fecha_hora = timezone.make_aware(comisaria.fecha_hora, timezone.get_current_timezone())
            comisaria.fecha_hora = timezone.localtime(comisaria.fecha_hora)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_jefessuperiores'] = self.request.user.groups.filter(name='jefessuperiores').exists()
        context['today'] = timezone.now().date()
        context['resolveId'] = None
        return context

   
    

class ComisariaSegundaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ComisariaSegunda
    form_class = ComisariaSegundaForm
    template_name = 'comisarias/segunda/comisaria_segunda_form.html'
    success_url = reverse_lazy('comisaria_segunda_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariasegunda')

    def handle_no_permission(self):
        return redirect('no_permission')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['codigos_policiales'] = CodigoPolicialUSH.objects.all()
        context['dependencias_secundarias'] = DependenciasSecundarias.objects.all()

        # Inicializar detalles como listas vacías en el contexto
        context['detalle_servicios_emergencia'] = json.dumps([])  # Para vista de creación, siempre es una lista vacía
        context['detalle_instituciones_hospitalarias'] = json.dumps([])
        context['detalle_dependencias_municipales'] = json.dumps([])
        context['detalle_dependencias_provinciales'] = json.dumps([])

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.updated_by = None
        self.object.updated_at = None

        latitude = self.request.POST.get('latitude').replace(',', '.')
        longitude = self.request.POST.get('longitude').replace(',', '.')

        self.object.latitude = float(latitude) if latitude else None
        self.object.longitude = float(longitude) if longitude else None

        self.object.save()
        form.save_m2m()

        # Guardar los detalles adicionales para cada servicio de emergencia
        for servicio in form.cleaned_data['servicios_emergencia']:
            numero_movil_bomberos = self.request.POST.get(f'numero_movil_bomberos_{servicio.id}')
            nombre_a_cargo_bomberos = self.request.POST.get(f'nombre_a_cargo_bomberos_{servicio.id}')
            if numero_movil_bomberos or nombre_a_cargo_bomberos:
                DetalleServicioEmergencia.objects.create(
                    servicio_emergencia=servicio,
                    comisaria_segunda=self.object,
                    numero_movil_bomberos=numero_movil_bomberos,
                    nombre_a_cargo_bomberos=nombre_a_cargo_bomberos
                )

        # Guardar los detalles adicionales para cada institución hospitalaria
        for institucion in form.cleaned_data['instituciones_hospitalarias']:
            numero_movil_hospital = self.request.POST.get(f'numero_movil_hospital_{institucion.id}')
            nombre_a_cargo_hospital = self.request.POST.get(f'nombre_a_cargo_hospital_{institucion.id}')
            if numero_movil_hospital or nombre_a_cargo_hospital:
                DetalleInstitucionHospitalaria.objects.create(
                    institucion_hospitalaria=institucion,
                    comisaria_segunda=self.object,
                    numero_movil_hospital=numero_movil_hospital,
                    nombre_a_cargo_hospital=nombre_a_cargo_hospital
                )

        # Guardar los detalles adicionales para cada dependencia municipal
        for dependencia_municipal in form.cleaned_data['dependencias_municipales']:
            numero_movil_municipal = self.request.POST.get(f'numero_movil_municipal_{dependencia_municipal.id}')
            nombre_a_cargo_municipal = self.request.POST.get(f'nombre_a_cargo_municipal_{dependencia_municipal.id}')
            if numero_movil_municipal or nombre_a_cargo_municipal:
                DetalleDependenciaMunicipal.objects.create(
                    dependencia_municipal=dependencia_municipal,
                    comisaria_segunda=self.object,
                    numero_movil_municipal=numero_movil_municipal,
                    nombre_a_cargo_municipal=nombre_a_cargo_municipal
                )

        # Guardar los detalles adicionales para cada dependencia provincial
        for dependencia_provincial in form.cleaned_data['dependencias_provinciales']:
            numero_movil_provincial = self.request.POST.get(f'numero_movil_provincial_{dependencia_provincial.id}')
            nombre_a_cargo_provincial = self.request.POST.get(f'nombre_a_cargo_provincial_{dependencia_provincial.id}')
            if numero_movil_provincial or nombre_a_cargo_provincial:
                DetalleDependenciaProvincial.objects.create(
                    dependencia_provincial=dependencia_provincial,
                    comisaria_segunda=self.object,
                    numero_movil_provincial=numero_movil_provincial,
                    nombre_a_cargo_provincial=nombre_a_cargo_provincial
                )

        return super().form_valid(form)





class ComisariaSegundaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ComisariaSegunda
    form_class = ComisariaSegundaForm
    template_name = 'comisarias/segunda/comisaria_segunda_form.html'
    success_url = reverse_lazy('comisaria_segunda_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariasegunda')

    def handle_no_permission(self):
        return redirect('no_permission')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        now = timezone.now()

        if obj.fecha_hora.date() != now.date() and not obj.estado:
            return redirect('comisaria_segunda_list')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['codigos_policiales'] = CodigoPolicialUSH.objects.all()
        context['dependencias_secundarias'] = DependenciasSecundarias.objects.all()

        # Convertir detalles en JSON para ser usados por Alpine.js
        context['detalle_servicios_emergencia'] = json.dumps(list(
            DetalleServicioEmergencia.objects.filter(comisaria_segunda=self.object.pk).values('id', 'servicio_emergencia_id', 'numero_movil_bomberos', 'nombre_a_cargo_bomberos')
        ))

        context['detalle_instituciones_hospitalarias'] = json.dumps(list(
            DetalleInstitucionHospitalaria.objects.filter(comisaria_segunda=self.object.pk).values('id', 'institucion_hospitalaria_id', 'numero_movil_hospital', 'nombre_a_cargo_hospital')
        ))

        context['detalle_dependencias_municipales'] = json.dumps(list(
            DetalleDependenciaMunicipal.objects.filter(comisaria_segunda=self.object.pk).values('id', 'dependencia_municipal_id', 'numero_movil_municipal', 'nombre_a_cargo_municipal')
        ))

        context['detalle_dependencias_provinciales'] = json.dumps(list(
            DetalleDependenciaProvincial.objects.filter(comisaria_segunda=self.object.pk).values('id', 'dependencia_provincial_id', 'numero_movil_provincial', 'nombre_a_cargo_provincial')
        ))

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_by = self.request.user
        self.object.updated_at = timezone.now()

        latitude = self.request.POST.get('latitude').replace(',', '.')
        longitude = self.request.POST.get('longitude').replace(',', '.')

        self.object.latitude = float(latitude) if latitude else None
        self.object.longitude = float(longitude) if longitude else None

        self.object.save()
        form.save_m2m()

        # Mantener un registro de los IDs seleccionados
        servicios_emergencia_ids = form.cleaned_data['servicios_emergencia'].values_list('id', flat=True)
        instituciones_hospitalarias_ids = form.cleaned_data['instituciones_hospitalarias'].values_list('id', flat=True)
        dependencias_municipales_ids = form.cleaned_data['dependencias_municipales'].values_list('id', flat=True)
        dependencias_provinciales_ids = form.cleaned_data['dependencias_provinciales'].values_list('id', flat=True)

        # Eliminar los detalles que ya no están seleccionados
        DetalleServicioEmergencia.objects.filter(comisaria_segunda=self.object).exclude(servicio_emergencia_id__in=servicios_emergencia_ids).delete()
        DetalleInstitucionHospitalaria.objects.filter(comisaria_segunda=self.object).exclude(institucion_hospitalaria_id__in=instituciones_hospitalarias_ids).delete()
        DetalleDependenciaMunicipal.objects.filter(comisaria_segunda=self.object).exclude(dependencia_municipal_id__in=dependencias_municipales_ids).delete()
        DetalleDependenciaProvincial.objects.filter(comisaria_segunda=self.object).exclude(dependencia_provincial_id__in=dependencias_provinciales_ids).delete()

        # Guardar los detalles adicionales para cada servicio de emergencia
        for servicio in form.cleaned_data['servicios_emergencia']:
            numero_movil_bomberos = self.request.POST.get(f'numero_movil_bomberos_{servicio.id}')
            nombre_a_cargo_bomberos = self.request.POST.get(f'nombre_a_cargo_bomberos_{servicio.id}')
            DetalleServicioEmergencia.objects.update_or_create(
                servicio_emergencia=servicio,
                comisaria_segunda=self.object,
                defaults={
                    'numero_movil_bomberos': numero_movil_bomberos,
                    'nombre_a_cargo_bomberos': nombre_a_cargo_bomberos
                }
            )

        # Guardar los detalles adicionales para cada institución hospitalaria
        for institucion in form.cleaned_data['instituciones_hospitalarias']:
            numero_movil_hospital = self.request.POST.get(f'numero_movil_hospital_{institucion.id}')
            nombre_a_cargo_hospital = self.request.POST.get(f'nombre_a_cargo_hospital_{institucion.id}')
            DetalleInstitucionHospitalaria.objects.update_or_create(
                institucion_hospitalaria=institucion,
                comisaria_segunda=self.object,
                defaults={
                    'numero_movil_hospital': numero_movil_hospital,
                    'nombre_a_cargo_hospital': nombre_a_cargo_hospital
                }
            )

        # Guardar los detalles adicionales para cada dependencia municipal
        for dependencia_municipal in form.cleaned_data['dependencias_municipales']:
            numero_movil_municipal = self.request.POST.get(f'numero_movil_municipal_{dependencia_municipal.id}')
            nombre_a_cargo_municipal = self.request.POST.get(f'nombre_a_cargo_municipal_{dependencia_municipal.id}')
            DetalleDependenciaMunicipal.objects.update_or_create(
                dependencia_municipal=dependencia_municipal,
                comisaria_segunda=self.object,
                defaults={
                    'numero_movil_municipal': numero_movil_municipal,
                    'nombre_a_cargo_municipal': nombre_a_cargo_municipal
                }
            )

        # Guardar los detalles adicionales para cada dependencia provincial
        for dependencia_provincial in form.cleaned_data['dependencias_provinciales']:
            numero_movil_provincial = self.request.POST.get(f'numero_movil_provincial_{dependencia_provincial.id}')
            nombre_a_cargo_provincial = self.request.POST.get(f'nombre_a_cargo_provincial_{dependencia_provincial.id}')
            DetalleDependenciaProvincial.objects.update_or_create(
                dependencia_provincial=dependencia_provincial,
                comisaria_segunda=self.object,
                defaults={
                    'numero_movil_provincial': numero_movil_provincial,
                    'nombre_a_cargo_provincial': nombre_a_cargo_provincial
                }
            )

        return super().form_valid(form)



    



class ComisariaTerceraListView(LoginRequiredMixin, ListView):
    model = ComisariaTercera
    template_name = 'comisarias/tercera/comisaria_tercera_list.html'

class ComisariaTerceraCreateView(LoginRequiredMixin, CreateView):
    model = ComisariaTercera
    form_class = ComisariaTerceraForm
    template_name = 'comisarias/tercera/comisaria_tercera_form.html'
    success_url = reverse_lazy('comisaria_tercera_list')

class ComisariaCuartaListView(LoginRequiredMixin, ListView):
    model = ComisariaCuarta
    template_name = 'comisarias/cuarta/comisaria_cuarta_list.html'

class ComisariaCuartaCreateView(LoginRequiredMixin, CreateView):
    model = ComisariaCuarta
    form_class = ComisariaCuartaForm
    template_name = 'comisarias/cuarta/comisaria_cuarta_form.html'
    success_url = reverse_lazy('comisaria_cuarta_list')

class ComisariaQuintaListView(LoginRequiredMixin, ListView):
    model = ComisariaQuinta
    template_name = 'comisarias/quinta/comisaria_quinta_list.html'

class ComisariaQuintaCreateView(LoginRequiredMixin, CreateView):
    model = ComisariaQuinta
    form_class = ComisariaQuintaForm
    template_name = 'comisarias/quinta/comisaria_quinta_form.html'
    success_url = reverse_lazy('comisaria_quinta_list')

# Vista para listar todas las comisarías
class ComisariasCompletaListView(LoginRequiredMixin, ListView):
    template_name = 'comisarias/comisarias_completa_list.html'
    context_object_name = 'comisarias'

    # Obtiene el conjunto de consultas combinado de todas las comisarías
    def get_queryset(self):

        query = self.request.GET.get('q', '')
    
        combined_list = []

        comisarias_primera = ComisariaPrimera.objects.select_related('cuarto').all()
        comisarias_segunda = ComisariaSegunda.objects.select_related('cuarto').all()
        comisarias_tercera = ComisariaTercera.objects.select_related('cuarto').all()
        comisarias_cuarta = ComisariaCuarta.objects.select_related('cuarto').all()
        comisarias_quinta = ComisariaQuinta.objects.select_related('cuarto').all()

        for comisaria in comisarias_primera:
            comisaria.comisaria_nombre = 'Comisaria Primera'
        for comisaria in comisarias_segunda:
            comisaria.comisaria_nombre = 'Comisaria Segunda'
        for comisaria in comisarias_tercera:
            comisaria.comisaria_nombre = 'Comisaria Tercera'
        for comisaria in comisarias_cuarta:
            comisaria.comisaria_nombre = 'Comisaria Cuarta'
        for comisaria in comisarias_quinta:
            comisaria.comisaria_nombre = 'Comisaria Quinta'

        combined_list = list(comisarias_primera) + list(comisarias_segunda) + \
                        list(comisarias_tercera) + list(comisarias_cuarta) + \
                        list(comisarias_quinta)

        if query:
            combined_list = [comisaria for comisaria in combined_list if self.query_in_comisaria(comisaria, query)]

        combined_list = sorted(combined_list, key=lambda x: x.created_at, reverse=True)

        return combined_list

    # Verifica si la consulta coincide con algún campo de la comisaría
    def query_in_comisaria(self, comisaria, query):
        query_lower = query.lower()
        return (
            (query_lower in comisaria.comisaria_nombre.lower() if comisaria.comisaria_nombre else False) or
            (query_lower in comisaria.cuarto.cuarto.lower() if comisaria.cuarto and comisaria.cuarto.cuarto else False) or
            (query_lower in comisaria.codigo.codigo.lower() if comisaria.codigo and comisaria.codigo.codigo else False) or
            (query_lower in comisaria.movil_patrulla.lower() if comisaria.movil_patrulla else False) or
            (query_lower in comisaria.a_cargo.lower() if comisaria.a_cargo else False) or
            (query_lower in comisaria.secundante.lower() if comisaria.secundante else False) or
            (query_lower in comisaria.lugar_codigo.lower() if comisaria.lugar_codigo else False) or
            (query_lower in comisaria.descripcion.lower() if comisaria.descripcion else False) or
            (query_lower in comisaria.instituciones_intervinientes.lower() if comisaria.instituciones_intervinientes else False) or
            (query_lower in comisaria.tareas_judiciales.lower() if comisaria.tareas_judiciales else False) or
            (query_lower in comisaria.fecha_hora.strftime('%Y-%m-%d %H:%M:%S').lower() if comisaria.fecha_hora else False)
        )

    # Añade información adicional al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['paginate_by'] = self.request.GET.get('items_per_page', 10)
        return context
    
    

from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.http import HttpResponse, FileResponse
from datetime import datetime, timedelta
from .models import ComisariaPrimera, ComisariaSegunda, ComisariaTercera, ComisariaCuarta, ComisariaQuinta
from django.db import models

def generate_pdf_content(request, comisaria_model, add_signature=False):
    now = datetime.now()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    registros = comisaria_model.objects.filter(
        models.Q(created_at__range=(start_of_day, end_of_day)) |
        models.Q(updated_at__range=(start_of_day, end_of_day))
    )

    template = get_template('comisarias/comisarias_pdf_template.html')
    context = {
        'registros': registros,
        'comisaria_name': comisaria_model._meta.verbose_name.title(),
        'add_signature': add_signature,
        'username': request.user.get_full_name(),
        'now': now
    }
    html = template.render(context)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
    if not pdf.err:
        return response.getvalue()
    else:
        return None

def generate_pdf(request, comisaria_model, filename, add_signature=False):
    pdf_content = generate_pdf_content(request, comisaria_model, add_signature)
    if pdf_content:
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{filename}"'
        return response
    else:
        return HttpResponse('Error al generar el PDF', status=500)

def view_pdf_content(request, comisaria_model):
    buffer = generate_pdf_content(request, comisaria_model)
    response = FileResponse(BytesIO(buffer), content_type='application/pdf')
    return response

def generate_comisaria_primera_pdf_view(request):
    return view_pdf_content(request, ComisariaPrimera)

def generate_comisaria_primera_pdf_download(request):
    add_signature = 'signature' in request.GET
    now = datetime.now()
    filename = f"parte-diario-{now.strftime('%d-%m-%Y')}.pdf"
    return generate_pdf(request, ComisariaPrimera, filename, add_signature=add_signature)

# Función para descargar el PDF del día anterior
def generate_comisaria_primera_pdf_download_previous_day(request):
    add_signature = 'signature' in request.GET
    now = datetime.now()
    previous_day = now - timedelta(days=1)
    filename = f"parte-diario-{previous_day.strftime('%d-%m-%Y')}.pdf"
    return generate_pdf_for_specific_date(request, ComisariaPrimera, previous_day, filename, add_signature=add_signature)

def generate_pdf_for_specific_date(request, comisaria_model, specific_date, filename, add_signature=False):
    start_of_day = specific_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = specific_date.replace(hour=23, minute=59, second=59, microsecond=999999)
    registros = comisaria_model.objects.filter(
        models.Q(created_at__range=(start_of_day, end_of_day)) |
        models.Q(updated_at__range=(start_of_day, end_of_day))
    )

    template = get_template('comisarias/comisarias_pdf_template.html')
    context = {
        'registros': registros,
        'comisaria_name': comisaria_model._meta.verbose_name.title(),
        'add_signature': add_signature,
        'username': request.user.get_full_name(),
        'now': specific_date
    }
    html = template.render(context)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
    if not pdf.err:
        return HttpResponse(response.getvalue(), content_type='application/pdf', headers={'Content-Disposition': f'inline; filename="{filename}"'})
    else:
        return HttpResponse('Error al generar el PDF', status=500)
    

from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import UploadedPDF
import os
import mimetypes

def subir_pdf(request):
    if request.method == 'POST':
        if 'pdf' in request.FILES:
            pdf = request.FILES['pdf']
            
            # Validar que el archivo sea un PDF
            mime_type, _ = mimetypes.guess_type(pdf.name)
            if mime_type != 'application/pdf':
                return JsonResponse({'error': 'El archivo seleccionado no es un PDF.'})
            
            try:
                # Especifica la ruta donde se guardarán los archivos
                folder = 'partespdf/'
                fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, folder))
                filename = fs.save(pdf.name, pdf)
                
                # Guardar en la base de datos solo el nombre del archivo
                new_pdf = UploadedPDF(file=os.path.join(folder, filename), uploaded_by=request.user)
                new_pdf.save()

                # Respuesta en formato JSON
                return JsonResponse({'success': 'El archivo PDF se ha subido correctamente.'})
            
            except Exception as e:
                # Manejar cualquier error durante la subida del archivo
                return JsonResponse({'error': f'Error al subir el archivo: {str(e)}'})
        
        else:
            return JsonResponse({'error': 'No se seleccionó ningún archivo.'})
    
    return render(request, 'comisarias/subir_pdf.html')




from django.shortcuts import render
from .models import UploadedPDF

def ver_pdfs(request):
    pdfs = UploadedPDF.objects.all()
    return render(request, 'comisarias/ver_pdfs.html', {'pdfs': pdfs})



# Repite las siguientes funciones para las demás comisarías...
def generate_comisaria_segunda_pdf_view(request):
    return view_pdf_content(request, ComisariaSegunda)

def generate_comisaria_segunda_pdf_download(request):
    add_signature = 'signature' in request.GET
    now = datetime.now()
    filename = f"parte-diario-{now.strftime('%d-%m-%Y_%H-%M-%S')}.pdf"
    return generate_pdf(request, ComisariaSegunda, filename, add_signature=add_signature)

# Continúa con las demás funciones para las comisarías tercera, cuarta y quinta.


def generate_comisaria_tercera_pdf_view(request):
    return view_pdf_content(request, ComisariaTercera)

def generate_comisaria_tercera_pdf_download(request):
    add_signature = 'signature' in request.GET
    now = datetime.now()
    filename = f"parte-diario-{now.strftime('%d-%m-%Y_%H-%M-%S')}.pdf"
    return generate_pdf(request, ComisariaTercera, filename, add_signature=add_signature)

def generate_comisaria_cuarta_pdf_view(request):
    return view_pdf_content(request, ComisariaCuarta)

def generate_comisaria_cuarta_pdf_download(request):
    add_signature = 'signature' in request.GET
    now = datetime.now()
    filename = f"parte-diario-{now.strftime('%d-%m-%Y_%H-%M-%S')}.pdf"
    return generate_pdf(request, ComisariaCuarta, filename, add_signature=add_signature)

def generate_comisaria_quinta_pdf_view(request):
    return view_pdf_content(request, ComisariaQuinta)

def generate_comisaria_quinta_pdf_download(request):
    add_signature = 'signature' in request.GET
    now = datetime.now()
    filename = f"parte-diario-{now.strftime('%d-%m-%Y_%H-%M-%S')}.pdf"
    return generate_pdf(request, ComisariaQuinta, filename, add_signature=add_signature)
