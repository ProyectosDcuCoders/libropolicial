from Libropolicial.forms import CustomLoginForm
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import (
    ComisariaPrimera, ComisariaSegunda, ComisariaTercera, 
    ComisariaCuarta, ComisariaQuinta, CodigoPolicialUSH, 
    CodigosSecundarios, ResolucionCodigo, CuartoGuardiaUSH  # Importa el modelo CuartoGuardiaUSH
)

class BaseComisariaForm(forms.ModelForm):
    # Campo para seleccionar el cuarto de guardia
    cuarto = forms.ModelChoiceField(
        queryset=CuartoGuardiaUSH.objects.all(),
        required=False,
        label='Cuarto',
        widget=forms.Select(
            attrs={
                'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3 appearance-none'
            }
        )
    )

    # Campo para seleccionar el código policial principal
    codigo = forms.ModelChoiceField(
        queryset=CodigoPolicialUSH.objects.all(),
        required=False,
        label='Código Principal',
        widget=forms.Select(
            attrs={
                'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3 appearance-none'
            }
        )
    )

    # Campo para seleccionar múltiples códigos secundarios
    codigos_secundarios = forms.ModelMultipleChoiceField(
        queryset=CodigosSecundarios.objects.all(),
        required=False,
        label='Códigos Secundarios',
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'
            }
        )
    )

    # Campo de texto para la descripción
    descripcion = forms.CharField(
        widget=CKEditorWidget(
            attrs={
                'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'
            }
        ),
        label='Descripción',
        required=False
    )

    class Meta:
        fields = [
            'cuarto', 'fecha_hora', 'codigo', 'codigos_secundarios', 
            'movil_patrulla', 'a_cargo', 'secundante', 'lugar_codigo', 
            'descripcion', 'instituciones_intervinientes', 'tareas_judiciales', 
            'estado'
        ]
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'estado': forms.CheckboxInput(attrs={'class': 'sr-only peer'}),
        }

class ComisariaPrimeraForm(BaseComisariaForm):
    class Meta(BaseComisariaForm.Meta):
        model = ComisariaPrimera

# El mismo patrón para las demás comisarías
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

class ResolucionCodigoForm(forms.ModelForm):
    class Meta:
        model = ResolucionCodigo
        fields = ['resolucion_codigo']
