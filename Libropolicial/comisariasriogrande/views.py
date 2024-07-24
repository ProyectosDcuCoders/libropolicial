from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, TemplateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import LoginView
from Libropolicial.forms import CustomLoginForm  # Importar desde la ubicación común
from django.shortcuts import render, redirect
from .models import ComisariaPrimeraRG, ComisariaSegundaRG, ComisariaTerceraRG, ComisariaCuartaRG, ComisariaQuintaRG
from .forms import ComisariaPrimeraRGForm, ComisariaSegundaRGForm, ComisariaTerceraRGForm, ComisariaCuartaRGForm, ComisariaQuintaRGForm, CustomLoginForm
from django.urls import reverse_lazy

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
        if self.request.user.groups.filter(name='comisariaprimerarg').exists():
            return reverse_lazy('comisaria_primera_rg_list')
        elif self.request.user.groups.filter(name='comisariasegundarg').exists():
            return reverse_lazy('comisaria_segunda_rg_list')
        else:
            return reverse_lazy('no_permission')

class ComisariaPrimeraRGListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ComisariaPrimeraRG
    template_name = 'comisariasriogrande/primera/comisaria_primera_rg_list.html'

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariaprimera')

    def handle_no_permission(self):
        return redirect('no_permission')

class ComisariaSegundaRGListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ComisariaSegundaRG
    template_name = 'comisariasriogrande/segunda/comisaria_segunda_rg_list.html'

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariasegunda')

    def handle_no_permission(self):
        return redirect('no_permission')

class ComisariaTerceraRGListView(LoginRequiredMixin, ListView):
    model = ComisariaTerceraRG
    template_name = 'comisariasriogrande/comisaria_tercera_rg_list.html'

class ComisariaCuartaRGListView(LoginRequiredMixin, ListView):
    model = ComisariaCuartaRG
    template_name = 'comisariasriogrande/comisaria_cuarta_rg_list.html'

class ComisariaQuintaRGListView(LoginRequiredMixin, ListView):
    model = ComisariaQuintaRG
    template_name = 'comisariasriogrande/comisaria_quinta_rg_list.html'

class ComisariasRGCompletaListView(LoginRequiredMixin, ListView):
    template_name = 'comisariasriogrande/comisarias_rg_completa_list.html'
    context_object_name = 'comisarias'

    def get_queryset(self):
        comisarias_primera_rg = ComisariaPrimeraRG.objects.select_related('codigo', 'cuarto').all()
        comisarias_segunda_rg = ComisariaSegundaRG.objects.select_related('codigo', 'cuarto').all()
        comisarias_tercera_rg = ComisariaTerceraRG.objects.select_related('codigo', 'cuarto').all()
        comisarias_cuarta_rg = ComisariaCuartaRG.objects.select_related('codigo', 'cuarto').all()
        comisarias_quinta_rg = ComisariaQuintaRG.objects.select_related('codigo', 'cuarto').all()

        for comisaria in comisarias_primera_rg:
            comisaria.comisaria_nombre = 'Comisaria Primera'
        for comisaria in comisarias_segunda_rg:
            comisaria.comisaria_nombre = 'Comisaria Segunda'
        for comisaria in comisarias_tercera_rg:
            comisaria.comisaria_nombre = 'Comisaria Tercera'
        for comisaria in comisarias_cuarta_rg:
            comisaria.comisaria_nombre = 'Comisaria Cuarta'
        for comisaria in comisarias_quinta_rg:
            comisaria.comisaria_nombre = 'Comisaria Quinta'

        combined_list = list(comisarias_primera_rg) + list(comisarias_segunda_rg) + \
                        list(comisarias_tercera_rg) + list(comisarias_cuarta_rg) + \
                        list(comisarias_quinta_rg)
        return sorted(combined_list, key=lambda x: x.created_at)

class ComisariaPrimeraRGCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ComisariaPrimeraRG
    form_class = ComisariaPrimeraRGForm
    template_name = 'comisariasriogrande/primera/comisaria_primera_rg_form.html'
    success_url = reverse_lazy('comisaria_primera_rg_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariaprimera')

    def handle_no_permission(self):
        return redirect('no_permission')

class ComisariaPrimeraRGUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ComisariaPrimeraRG
    form_class = ComisariaPrimeraRGForm
    template_name = 'comisariasriogrande/primera/comisaria_primera_rg_form.html'
    success_url = reverse_lazy('comisaria_primera_rg_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariaprimera')

    def handle_no_permission(self):
        return redirect('no_permission')

class ComisariaSegundaRGCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ComisariaSegundaRG
    form_class = ComisariaSegundaRGForm
    template_name = 'comisariasriogrande/segunda/comisaria_segunda_rg_form.html'
    success_url = reverse_lazy('comisaria_segunda_rg_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariasegunda')

    def handle_no_permission(self):
        return redirect('no_permission')

class ComisariaSegundaRGUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ComisariaSegundaRG
    form_class = ComisariaSegundaRGForm
    template_name = 'comisariasriogrande/segunda/comisaria_segunda_rg_form.html'
    success_url = reverse_lazy('comisaria_segunda_rg_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariasegunda')

    def handle_no_permission(self):
        return redirect('no_permission')

class ComisariaTerceraRGCreateView(LoginRequiredMixin, CreateView):
    model = ComisariaTerceraRG
    form_class = ComisariaTerceraRGForm
    template_name = 'comisariasriogrande/comisaria_tercera_rg_form.html'
    success_url = reverse_lazy('comisaria_tercera_rg_list')

class ComisariaCuartaRGCreateView(LoginRequiredMixin, CreateView):
    model = ComisariaCuartaRG
    form_class = ComisariaCuartaRGForm
    template_name = 'comisariasriogrande/comisaria_cuarta_rg_form.html'
    success_url = reverse_lazy('comisaria_cuarta_rg_list')

class ComisariaQuintaRGCreateView(LoginRequiredMixin, CreateView):
    model = ComisariaQuintaRG
    form_class = ComisariaQuintaRGForm
    template_name = 'comisariasriogrande/comisaria_quinta_rg_form.html'
    success_url = reverse_lazy('comisaria_quinta_rg_list')
