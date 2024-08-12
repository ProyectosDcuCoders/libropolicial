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
from .models import ComisariaPrimera, ComisariaSegunda, ComisariaTercera, ComisariaCuarta, ComisariaQuinta, DependenciasSecundarias, ResolucionCodigo,CodigoPolicialUSH, DetalleServicioEmergencia, DetalleInstitucionHospitalaria,DetalleDependenciaMunicipal, DetalleDependenciaProvincial
from .forms import ComisariaPrimeraForm, ComisariaSegundaForm, ComisariaTerceraForm, ComisariaCuartaForm, ComisariaQuintaForm, ResolucionCodigoForm, CustomLoginForm
from compartido.utils import user_is_in_group



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
        return context

    #def test_func(self):
        #return self.request.user.is_authenticated and user_is_in_group(self.request.user, 'comisariaprimera')
    
    #def handle_no_permission(self):
        #return redirect('no_permission')

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
            numero_movil = self.request.POST.get(f'numero_movil_{servicio.id}')
            nombre_a_cargo = self.request.POST.get(f'nombre_a_cargo_{servicio.id}')
            DetalleServicioEmergencia.objects.create(
                servicio_emergencia=servicio,
                comisaria_primera=self.object,
                numero_movil=numero_movil,
                nombre_a_cargo=nombre_a_cargo
            )

        # Guardar los detalles adicionales para cada institución hospitalaria
        for institucion in form.cleaned_data['instituciones_hospitalarias']:
            numero_movil = self.request.POST.get(f'numero_movil_{institucion.id}')
            nombre_a_cargo = self.request.POST.get(f'nombre_a_cargo_{institucion.id}')
            DetalleInstitucionHospitalaria.objects.create(
                institucion_hospitalaria=institucion,
                comisaria_primera=self.object,
                numero_movil=numero_movil,
                nombre_a_cargo=nombre_a_cargo
            )

        # Guardar los detalles adicionales para cada dependencia municipal
        for dependencia_municipal in form.cleaned_data['dependencias_municipales']:
            numero_movil = self.request.POST.get(f'numero_movil_{dependencia_municipal.id}')
            nombre_a_cargo = self.request.POST.get(f'nombre_a_cargo_{dependencia_municipal.id}')
            DetalleDependenciaMunicipal.objects.create(
                dependencia_municipal=dependencia_municipal,
                comisaria_primera=self.object,
                numero_movil=numero_movil,
                nombre_a_cargo=nombre_a_cargo
            )

        # Guardar los detalles adicionales para cada dependencia provincial
        for dependencia_provincial in form.cleaned_data['dependencias_provinciales']:
            numero_movil = self.request.POST.get(f'numero_movil_{dependencia_provincial.id}')
            nombre_a_cargo = self.request.POST.get(f'nombre_a_cargo_{dependencia_provincial.id}')
            DetalleDependenciaProvincial.objects.create(
                dependencia_provincial=dependencia_provincial,
                comisaria_primera=self.object,
                numero_movil=numero_movil,
                nombre_a_cargo=nombre_a_cargo
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
        context['latitude'] = self.object.latitude
        context['longitude'] = self.object.longitude
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

        return super().form_valid(form)



class ComisariaPrimeraResolveView(UpdateView):
    model = ResolucionCodigo
    form_class = ResolucionCodigoForm
    template_name = 'comisarias/primera/comisaria_primera_resolve.html'
    success_url = reverse_lazy('comisaria_primera_list')

    def form_valid(self, form):
        resolucion = form.save(commit=False)
        resolucion.updated_by = self.request.user
        resolucion.updated_at = timezone.now()
        resolucion.comisaria_primera = ComisariaPrimera.objects.get(pk=self.kwargs['pk'])
        resolucion.save()

        comisaria = resolucion.comisaria_primera
        comisaria.estado = False
        comisaria.updated_by = self.request.user
        comisaria.updated_at = timezone.now()
        comisaria.save()

        return super().form_valid(form)


# Vistas de listado y creación para ComisariaSegunda, ComisariaTercera, ComisariaCuarta, y ComisariaQuinta
# Siguen el mismo patrón que ComisariaPrimera

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
        return context

    #def test_func(self):
       # return self.request.user.is_authenticated and user_is_in_group(self.request.user, 'comisariasegunda')

    #def handle_no_permission(self):
        #return redirect('no_permission')


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
            numero_movil = self.request.POST.get(f'numero_movil_{servicio.id}')
            nombre_a_cargo = self.request.POST.get(f'nombre_a_cargo_{servicio.id}')
            DetalleServicioEmergencia.objects.create(
                servicio_emergencia=servicio,
                comisaria_segunda=self.object,
                numero_movil=numero_movil,
                nombre_a_cargo=nombre_a_cargo
            )

        # Guardar los detalles adicionales para cada institución hospitalaria
        for institucion in form.cleaned_data['instituciones_hospitalarias']:
            numero_movil = self.request.POST.get(f'numero_movil_{institucion.id}')
            nombre_a_cargo = self.request.POST.get(f'nombre_a_cargo_{institucion.id}')
            DetalleInstitucionHospitalaria.objects.create(
                institucion_hospitalaria=institucion,
                comisaria_segunda=self.object,
                numero_movil=numero_movil,
                nombre_a_cargo=nombre_a_cargo
            )

        # Guardar los detalles adicionales para cada dependencia municipal
        for dependencia_municipal in form.cleaned_data['dependencias_municipales']:
            numero_movil = self.request.POST.get(f'numero_movil_{dependencia_municipal.id}')
            nombre_a_cargo = self.request.POST.get(f'nombre_a_cargo_{dependencia_municipal.id}')
            DetalleDependenciaMunicipal.objects.create(
                dependencia_municipal=dependencia_municipal,
                comisaria_segunda=self.object,
                numero_movil=numero_movil,
                nombre_a_cargo=nombre_a_cargo
            )

        # Guardar los detalles adicionales para cada dependencia provincial
        for dependencia_provincial in form.cleaned_data['dependencias_provinciales']:
            numero_movil = self.request.POST.get(f'numero_movil_{dependencia_provincial.id}')
            nombre_a_cargo = self.request.POST.get(f'nombre_a_cargo_{dependencia_provincial.id}')
            DetalleDependenciaProvincial.objects.create(
                dependencia_provincial=dependencia_provincial,
                comisaria_segunda=self.object,
                numero_movil=numero_movil,
                nombre_a_cargo=nombre_a_cargo
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
        context['latitude'] = self.object.latitude
        context['longitude'] = self.object.longitude
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

    # Obtiene el conjunto de consultas combinado de todas las comisarías, con paginación y búsqueda
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        items_per_page = self.request.GET.get('items_per_page', 10)
        
        try:
            items_per_page = int(items_per_page)
        except ValueError:
            items_per_page = 10
        
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

        paginator = Paginator(combined_list, items_per_page)
        page = self.request.GET.get('page')
        try:
            comisarias = paginator.page(page)
        except PageNotAnInteger:
            comisarias = paginator.page(1)
        except EmptyPage:
            comisarias = paginator.page(paginator.num_pages)

        return comisarias

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
from datetime import datetime
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
