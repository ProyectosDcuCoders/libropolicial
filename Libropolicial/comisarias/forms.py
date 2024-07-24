# Libropolicial/comisarias/forms.py
from Libropolicial.forms import CustomLoginForm

from django import forms
from .models import ComisariaPrimera, ComisariaSegunda, ComisariaTercera, ComisariaCuarta, ComisariaQuinta, CodigoPolicialUSH

class BaseComisariaForm(forms.ModelForm):
    codigo = forms.ModelChoiceField(
        queryset=CodigoPolicialUSH.objects.all(),
        required=False,
        label='Códigos Policiales',
        widget=forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'})
    )

    class Meta:
        fields = ['cuarto', 'fecha_hora', 'codigo', 'movil_patrulla', 'a_cargo', 'secundante', 'lugar_codigo', 'descripcion', 'instituciones_intervinientes', 'tareas_judiciales', 'estado']

class ComisariaPrimeraForm(BaseComisariaForm):
    class Meta(BaseComisariaForm.Meta):
        model = ComisariaPrimera

class ComisariaSegundaForm(BaseComisariaForm):
    class Meta(BaseComisariaForm.Meta):
        model = ComisariaSegunda

class ComisariaTerceraForm(BaseComisariaForm):
    class Meta(BaseComisariaForm.Meta):
        model = ComisariaTercera

class ComisariaCuartaForm(BaseComisariaForm):
    class Meta(BaseComisariaForm.Meta):
        model = ComisariaCuarta

class ComisariaQuintaForm(BaseComisariaForm):
    class Meta(BaseComisariaForm.Meta):
        model = ComisariaQuinta
