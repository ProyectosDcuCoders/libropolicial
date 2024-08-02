# Libropolicial/comisarias/views.py
from django.http import JsonResponse
from django.core.serializers import serialize
from django.http import HttpResponse
from django.shortcuts import render, redirect
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.contrib.auth.views import LoginView
from .models import ComisariaPrimera, ComisariaSegunda, ComisariaTercera, ComisariaCuarta, ComisariaQuinta
from .forms import ComisariaPrimeraForm, ComisariaSegundaForm, ComisariaTerceraForm, ComisariaCuartaForm, ComisariaQuintaForm, CustomLoginForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.dateparse import parse_datetime
from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .utils import user_is_in_group


def user_is_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

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

class ComisariaPrimeraListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ComisariaPrimera
    template_name = 'comisarias/primera/comisaria_primera_list.html'
    context_object_name = 'records'

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariaprimera')

    def handle_no_permission(self):
        return redirect('no_permission')

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(cuarto__icontains=search_query)
        for comisaria in queryset:
            if timezone.is_naive(comisaria.fecha_hora):
                comisaria.fecha_hora = timezone.make_aware(comisaria.fecha_hora, timezone.get_current_timezone())
            comisaria.fecha_hora = timezone.localtime(comisaria.fecha_hora)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notification = self.request.session.pop('comisarias_notification', None)
        if notification:
            messages.add_message(self.request, messages.WARNING, f"Notificación: {notification['description']}, Solicitante: {notification['solicitante']}")
        context['messages'] = messages.get_messages(self.request)
        return context

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            self.object_list = self.get_queryset()
            paginator = Paginator(self.object_list, self.request.GET.get('paginate_by', 10))
            page = self.request.GET.get('page')
            page_obj = paginator.get_page(page)
            data = serialize('json', page_obj)
            return JsonResponse({
                'data': data,
                'page': page_obj.number,
                'num_pages': paginator.num_pages,
            }, safe=False)
        return super().get(request, *args, **kwargs)

class ComisariaPrimeraCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ComisariaPrimera
    form_class = ComisariaPrimeraForm
    template_name = 'comisarias/primera/comisaria_primera_form.html'
    success_url = reverse_lazy('comisaria_primera_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariaprimera')

    def handle_no_permission(self):
        return redirect('no_permission')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
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

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
    
    

class ComisariaSegundaListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ComisariaSegunda
    template_name = 'comisarias/segunda/comisaria_segunda_list.html'

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariasegunda')

    def handle_no_permission(self):
        return redirect('no_permission')

class ComisariaSegundaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ComisariaSegunda
    form_class = ComisariaSegundaForm
    template_name = 'comisarias/segunda/comisaria_segunda_form.html'
    success_url = reverse_lazy('comisaria_segunda_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariasegunda')

    def handle_no_permission(self):
        return redirect('no_permission')

class ComisariaSegundaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ComisariaSegunda
    form_class = ComisariaSegundaForm
    template_name = 'comisarias/segunda/comisaria_segunda_form.html'
    success_url = reverse_lazy('comisaria_segunda_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariasegunda')

    def handle_no_permission(self):
        return redirect('no_permission')

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

class ComisariasCompletaListView(LoginRequiredMixin, ListView):
    template_name = 'comisarias/comisarias_completa_list.html'
    context_object_name = 'comisarias'

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['paginate_by'] = self.request.GET.get('items_per_page', 10)
        return context

    
def generate_pdf(request, comisaria_model, filename, add_signature=False):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica", 8)
    y = height - 50

    now = timezone.now()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    registros = comisaria_model.objects.filter(created_at__range=(start_of_day, end_of_day))

    if not registros.exists():
        p.drawString(100, y, "No hay registros para hoy.")
    else:
        p.drawString(100, y, f"Registros de {comisaria_model._meta.verbose_name} - Hoy")
        y -= 20

        for registro in registros:
            p.drawString(50, y, f"Guardia: {registro.cuarto.cuarto if registro.cuarto else ''}")
            p.drawString(150, y, f"Código: {registro.codigo.codigo if registro.codigo else ''}")
            p.drawString(250, y, f"Móvil Patrulla: {registro.movil_patrulla if registro.movil_patrulla else ''}")
            p.drawString(350, y, f"A Cargo: {registro.a_cargo if registro.a_cargo else ''}")
            y -= 10
            p.drawString(50, y, f"Secundante: {registro.secundante if registro.secundante else ''}")
            p.drawString(150, y, f"Lugar del Código: {registro.lugar_codigo if registro.lugar_codigo else ''}")
            p.drawString(250, y, f"Descripción: {registro.descripcion if registro.descripcion else ''}")
            y -= 10
            p.drawString(50, y, f"Instituciones Intervinientes: {registro.instituciones_intervinientes if registro.instituciones_intervinientes else ''}")
            p.drawString(150, y, f"Tareas Judiciales: {registro.tareas_judiciales if registro.tareas_judiciales else ''}")
            y -= 20
            if y < 100:
                p.showPage()
                p.setFont("Helvetica", 8)
                y = height - 30

    if add_signature:
        username = request.user.username
        p.setFont("Helvetica-Bold", 14)
        p.setFillColorRGB(0.5, 0.5, 0.5, alpha=0.5)  # Gris claro, semi-transparente
        p.drawString(100, 50, f"Firmado electrónicamente por: {username}")

    p.showPage()
    p.save()
    return response


def view_pdf(request, comisaria_model, template_name):
    return render(request, template_name, {'pdf_url': request.path + 'download/'})

def generate_comisaria_primera_pdf(request):
    add_signature = 'signature' in request.GET
    return generate_pdf(request, ComisariaPrimera, 'comisaria_primera_registros.pdf', add_signature=add_signature)

def view_comisaria_primera_pdf(request):
    return view_pdf(request, ComisariaPrimera, 'comisarias/primera/view_pdf.html')

def generate_comisaria_segunda_pdf(request):
    add_signature = 'signature' in request.GET
    return generate_pdf(request, ComisariaSegunda, 'comisaria_segunda_registros.pdf', add_signature=add_signature)

def view_comisaria_segunda_pdf(request):
    return view_pdf(request, ComisariaSegunda, 'comisarias/segunda/view_pdf.html')

def generate_comisaria_tercera_pdf(request):
    add_signature = 'signature' in request.GET
    return generate_pdf(request, ComisariaTercera, 'comisaria_tercera_registros.pdf', add_signature=add_signature)

def view_comisaria_tercera_pdf(request):
    return view_pdf(request, ComisariaTercera, 'comisarias/tercera/view_pdf.html')

def generate_comisaria_cuarta_pdf(request):
    add_signature = 'signature' in request.GET
    return generate_pdf(request, ComisariaCuarta, 'comisaria_cuarta_registros.pdf', add_signature=add_signature)

def view_comisaria_cuarta_pdf(request):
    return view_pdf(request, ComisariaCuarta, 'comisarias/cuarta/view_pdf.html')

def generate_comisaria_quinta_pdf(request):
    add_signature = 'signature' in request.GET
    return generate_pdf(request, ComisariaQuinta, 'comisaria_quinta_registros.pdf', add_signature=add_signature)

def view_comisaria_quinta_pdf(request):
    return view_pdf(request, ComisariaQuinta, 'comisarias/quinta/view_pdf.html')
