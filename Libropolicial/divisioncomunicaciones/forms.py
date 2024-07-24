from django import forms
from .models import DivisionComunicaciones

class DivisionComunicacionesForm(forms.ModelForm):
    class Meta:
        model = DivisionComunicaciones
        fields = [
            'inicio_guardia',
            'finalizacion_guardia',
            'encargado_guardia',
            'solicitante',
            'nombre_apellido',
            'dni',
            'telefono',
            'movil_patrulla',
            'personal_cargo',
            'descripcion',
            'intervencion_comisaria',
            'personal_guardia'
        ]
        widgets = {
            'inicio_guardia': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'finalizacion_guardia': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'personal_guardia': forms.SelectMultiple(attrs={'class': 'select-multiple'}),
        }
