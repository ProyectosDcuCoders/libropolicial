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
from .models import ComisariaPrimera, ComisariaSegunda, ComisariaTercera, ComisariaCuarta, ComisariaQuinta, ResolucionCodigo
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

# views.py

class ComisariaPrimeraListView(LoginRequiredMixin, ListView):
    model = ComisariaPrimera
    template_name = 'comisarias/primera/comisaria_primera_list.html'
    context_object_name = 'records'

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



class ComisariaPrimeraCreateView(CreateView):
    model = ComisariaPrimera
    form_class = ComisariaPrimeraForm
    template_name = 'comisarias/primera/comisaria_primera_form.html'
    success_url = reverse_lazy('comisaria_primera_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        form.save_m2m()  # Para guardar los códigos secundarios
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

        # Verifica si la fecha del registro es el mismo día o si el estado es activo
        if obj.fecha_hora.date() != now.date() and not obj.estado:
            return redirect('comisaria_primera_list')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_by = self.request.user
        self.object.save()
        form.save_m2m()  # Para guardar los códigos secundarios
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

# views.py

import html2text

def generate_pdf_content(request, comisaria_model, add_signature=False):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    def draw_header(canvas):
        canvas.setFont("Helvetica-Bold", 12)
        title = f"Libro de Guardia {comisaria_model._meta.verbose_name.title()}"
        text_width = canvas.stringWidth(title, "Helvetica-Bold", 12)
        canvas.drawString((width - text_width) / 2, height - 30, title)

    p.setFont("Helvetica", 8)
    y = height - 50

    now = datetime.now()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    registros = comisaria_model.objects.filter(
        models.Q(created_at__range=(start_of_day, end_of_day)) |
        models.Q(updated_at__range=(start_of_day, end_of_day))
    )

    draw_header(p)

    if not registros.exists():
        p.drawString(100, y, "No hay registros para hoy.")
    else:
        y -= 20

    for registro in registros:
        p.setFillColorRGB(0.2, 0.2, 0.2)
        p.setFont("Helvetica-Bold", 9)

        p.drawString(50, y, "Fecha y hora:")
        p.setFont("Helvetica", 8)
        p.drawString(112, y, f"{registro.fecha_hora.strftime('%d-%m-%Y %H:%M:%S') if registro.fecha_hora else ''}")

        p.setFont("Helvetica-Bold", 9)
        p.drawString(230, y, "Código:")
        p.setFont("Helvetica", 8)
        p.drawString(267, y, f"{registro.codigo.codigo if registro.codigo else ''}")

        y -= 15

        p.setFont("Helvetica-Bold", 9)
        p.drawString(50, y, "Guardia:")
        p.setFont("Helvetica", 8)
        p.drawString(90, y, f"{registro.cuarto.cuarto if registro.cuarto else ''}")

        p.setFont("Helvetica-Bold", 9)
        p.drawString(230, y, "Móvil Patrulla:")
        p.setFont("Helvetica", 8)
        p.drawString(295, y, f"{registro.movil_patrulla if registro.movil_patrulla else ''}")

        p.setFont("Helvetica-Bold", 9)
        p.drawString(320, y, "A Cargo:")
        p.setFont("Helvetica", 8)
        p.drawString(362, y, f"{registro.a_cargo if registro.a_cargo else ''}")

        y -= 15

        p.setFont("Helvetica-Bold", 9)
        p.drawString(50, y, "Secundante:")
        p.setFont("Helvetica", 8)
        p.drawString(107, y, f"{registro.secundante if registro.secundante else ''}")

        p.setFont("Helvetica-Bold", 9)
        p.drawString(230, y, "Lugar del Código:")
        p.setFont("Helvetica", 8)
        p.drawString(310, y, f"{registro.lugar_codigo if registro.lugar_codigo else ''}")

        y -= 15

        # Convertir HTML a texto plano
        descripcion_text = html2text.html2text(registro.descripcion) if registro.descripcion else ''

        p.setFont("Helvetica-Bold", 9)
        p.drawString(50, y, "Descripción:")
        p.setFont("Helvetica", 8)
        y = split_text(p, descripcion_text.strip(), 108, y, 400, height, draw_header)
        y -= 10

        p.setFont("Helvetica-Bold", 9)
        p.drawString(50, y, "Instituciones Intervinientes:")
        p.setFont("Helvetica", 8)
        y = split_text(p, f"{registro.instituciones_intervinientes if registro.instituciones_intervinientes else ''}", 172, y, 400, height, draw_header)
        y -= 10

        p.setFont("Helvetica-Bold", 9)
        p.drawString(50, y, "Tareas Judiciales:")
        p.setFont("Helvetica", 8)
        y = split_text(p, f"{registro.tareas_judiciales if registro.tareas_judiciales else ''}", 130, y, 400, height, draw_header)
        y -= 20

        p.setFont("Helvetica-Bold", 9)
        p.drawString(50, y, "Firmas:")
        p.setFont("Helvetica", 8)
        p.drawString(95, y, f"{registro.firmas if registro.firmas else ''}")

        y -= 20

        p.line(50, y, width - 50, y)
        y -= 20

        if y < 100:
            p.showPage()
            draw_header(p)
            p.setFont("Helvetica", 8)
            y = height - 50

    if add_signature:
        draw_footer(p, request, now, comisaria_model, width)

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer



# Función para dividir el texto en múltiples líneas que se ajusten a un ancho dado
def split_text(canvas, text, x, y, max_width, height, draw_header):
    lines = []
    words = text.split()
    current_line = []
    current_width = 0
    for word in words:
        word_width = canvas.stringWidth(word, "Helvetica", 8)
        if current_width + word_width <= max_width:
            current_line.append(word)
            current_width += word_width + canvas.stringWidth(" ", "Helvetica", 8)
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_width = word_width + canvas.stringWidth(" ", "Helvetica", 8)
            y -= 0  # Mueve a la siguiente línea
        if y < 50:  # Verifica si se ha excedido la altura de la página
            canvas.showPage()
            draw_header(canvas)  # Dibuja el encabezado en una nueva página
            canvas.setFont("Helvetica", 8)
            y = height - 50
    if current_line:
        lines.append(" ".join(current_line))
    for line in lines:
        canvas.drawString(x, y, line)
        y -= 10
    return y

# Función para dibujar el pie de página en el PDF
def draw_footer(canvas, request, now, comisaria_model, width):
    username = request.user.first_name
    now_str = now.strftime('%d-%m-%Y %H:%M:%S')
    comisaria_name = comisaria_model._meta.verbose_name.title()

    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColorRGB(0.5, 0.5, 0.5, alpha=0.5)
    text = f"{comisaria_name}. Descargado por: {username}. Fecha y hora: {now_str}"
    text_width = canvas.stringWidth(text, "Helvetica-Bold", 8)
    canvas.drawString((width - text_width) / 2, 30, text)

# Función para generar el PDF y devolverlo en una respuesta HTTP
def generate_pdf(request, comisaria_model, filename, add_signature=False):
    buffer = generate_pdf_content(request, comisaria_model, add_signature)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response

# Función para ver el PDF en el navegador
def view_pdf(request, comisaria_model, template_name):
    return render(request, template_name, {'model_name': comisaria_model._meta.model_name})

# Función para generar el contenido del PDF y devolverlo en una respuesta de archivo
def view_pdf_content(request, comisaria_model):
    buffer = generate_pdf_content(request, comisaria_model)
    response = FileResponse(buffer, content_type='application/pdf')
    return response

# views.py
def generate_comisaria_primera_pdf_view(request):
    return view_pdf_content(request, ComisariaPrimera)

def generate_comisaria_primera_pdf_download(request):
    add_signature = 'signature' in request.GET
    now = datetime.now()
    filename = f"parte-diario-{now.strftime('%d-%m-%Y')}.pdf"
    return generate_pdf(request, ComisariaPrimera, filename, add_signature=add_signature)

# Repite para las demás comisarías
def generate_comisaria_segunda_pdf_view(request):
    return view_pdf_content(request, ComisariaSegunda)

def generate_comisaria_segunda_pdf_download(request):
    add_signature = 'signature' in request.GET
    now = datetime.now()
    filename = f"parte-diario-{now.strftime('%d-%m-%Y_%H-%M-%S')}.pdf"
    return generate_pdf(request, ComisariaSegunda, filename, add_signature=add_signature)

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
