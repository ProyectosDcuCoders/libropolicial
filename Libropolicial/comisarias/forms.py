from Libropolicial.forms import CustomLoginForm
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import (
    ComisariaPrimera, ComisariaSegunda, ComisariaTercera, 
    ComisariaCuarta, ComisariaQuinta, CodigoPolicialUSH, 
    CodigosSecundarios, DependenciasSecundarias, CuartoGuardiaUSH, InstitucionesFederales,
    InstitucionesHospitalarias, DependenciasMunicipales, DependenciasProvinciales,
    ServiciosEmergencia, DetalleServicioEmergencia, DetalleInstitucionHospitalaria,
    DetalleDependenciaMunicipal, DetalleDependenciaProvincial, DetalleDependenciaSecundaria, DetalleInstitucionFederal, SolicitanteCodigo
)

# Formulario para DetalleDependenciaSecundaria
class DetalleDependenciaSecundariaForm(forms.ModelForm):
    class Meta:
        model = DetalleDependenciaSecundaria
        fields = ['dependencia_secundaria', 'numero_movil_secundaria', 'nombre_a_cargo_secundaria']
        widgets = {
            'dependencia_secundaria': forms.HiddenInput(),
            'numero_movil_secundaria': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
            'nombre_a_cargo_secundaria': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
        }

# Formulario para DetalleInstitucionFederal
class DetalleInstitucionFederalForm(forms.ModelForm):
    class Meta:
        model = DetalleInstitucionFederal
        fields = ['institucion_federal', 'numero_movil_federal', 'nombre_a_cargo_federal']
        widgets = {
            'institucion_federal': forms.HiddenInput(),
            'numero_movil_federal': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
            'nombre_a_cargo_federal': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
        }

# Formulario para DetalleServicioEmergencia
class DetalleServicioEmergenciaForm(forms.ModelForm):
    class Meta:
        model = DetalleServicioEmergencia
        fields = ['servicio_emergencia', 'numero_movil_bomberos', 'nombre_a_cargo_bomberos']
        widgets = {
            'servicio_emergencia': forms.HiddenInput(),
            'numero_movil_bomberos': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
            'nombre_a_cargo_bomberos': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
        }

# Formulario para DetalleInstitucionHospitalaria
class DetalleInstitucionHospitalariaForm(forms.ModelForm):
    class Meta:
        model = DetalleInstitucionHospitalaria
        fields = ['institucion_hospitalaria', 'numero_movil_hospital', 'nombre_a_cargo_hospital']
        widgets = {
            'institucion_hospitalaria': forms.HiddenInput(),
            'numero_movil_hospital': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
            'nombre_a_cargo_hospital': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
        }

# Formulario para DetalleDependenciaMunicipal
class DetalleDependenciaMunicipalForm(forms.ModelForm):
    class Meta:
        model = DetalleDependenciaMunicipal
        fields = ['dependencia_municipal', 'numero_movil_municipal', 'nombre_a_cargo_municipal']
        widgets = {
            'dependencia_municipal': forms.HiddenInput(),
            'numero_movil_municipal': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
            'nombre_a_cargo_municipal': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
        }

# Formulario para DetalleDependenciaProvincial
class DetalleDependenciaProvincialForm(forms.ModelForm):
    class Meta:
        model = DetalleDependenciaProvincial
        fields = ['dependencia_provincial', 'numero_movil_provincial', 'nombre_a_cargo_provincial']
        widgets = {
            'dependencia_provincial': forms.HiddenInput(),
            'numero_movil_provincial': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
            'nombre_a_cargo_provincial': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
        }

# Formulario base para las comisarías
class BaseComisariaForm(forms.ModelForm):
    # Campo para seleccionar el cuarto de guardia
    cuarto = forms.ModelChoiceField(
        queryset=CuartoGuardiaUSH.objects.all(),
        required=False,
        label='Cuarto',
        widget=forms.Select(attrs={'class': 'cursor-pointer bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3 appearance-none'})
    )

    # Campo para seleccionar el solicitante de código
    solicitante_codigo = forms.ModelChoiceField(
        queryset=SolicitanteCodigo.objects.all(),
        required=False,
        label='Solicitante del Código',
        widget=forms.Select(attrs={'class': 'cursor-pointer bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3 appearance-none'})
    )

    # Campo para seleccionar el código policial principal
    codigo = forms.ModelChoiceField(
        queryset=CodigoPolicialUSH.objects.all(),
        required=False,
        label='Código Principal',
        widget=forms.Select(attrs={'class': 'cursor-pointer bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3 appearance-none'})
    )

    # Campo para seleccionar las dependencias secundarias
    dependencias_secundarias = forms.ModelMultipleChoiceField(
        queryset=DependenciasSecundarias.objects.all(),
        required=False,
        label='Dependencias Policiales',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'})
    )

    # Campo para seleccionar múltiples códigos secundarios
    codigos_secundarios = forms.ModelMultipleChoiceField(
        queryset=CodigosSecundarios.objects.all(),
        required=False,
        label='Códigos Secundarios',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'})
    )

    # Campo para seleccionar múltiples instituciones federales
    instituciones_federales = forms.ModelMultipleChoiceField(
        queryset=InstitucionesFederales.objects.all(),
        required=False,
        label='Instituciones Federales',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'})
    )

    # Campo para seleccionar múltiples instituciones hospitalarias
    instituciones_hospitalarias = forms.ModelMultipleChoiceField(
        queryset=InstitucionesHospitalarias.objects.all(),
        required=False,
        label='Instituciones Hospitalarias',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'})
    )

    # Campo para seleccionar múltiples dependencias municipales
    dependencias_municipales = forms.ModelMultipleChoiceField(
        queryset=DependenciasMunicipales.objects.all(),
        required=False,
        label='Dependencias Municipales',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'})
    )

    # Campo para seleccionar múltiples dependencias provinciales
    dependencias_provinciales = forms.ModelMultipleChoiceField(
        queryset=DependenciasProvinciales.objects.all(),
        required=False,
        label='Dependencias Provinciales',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'})
    )

    # Campo para seleccionar múltiples servicios de emergencia
    servicios_emergencia = forms.ModelMultipleChoiceField(
        queryset=ServiciosEmergencia.objects.all(),
        required=False,
        label='Servicios de Emergencia Bomberil',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'})
    )

    # Campo de texto para la descripción
    descripcion = forms.CharField(
        widget=CKEditorWidget(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
        label='Descripción',
        required=False
    )

    class Meta:
        fields = [
            'cuarto', 'fecha_hora', 'codigo', 'solicitante_codigo', 'dependencias_secundarias', 'codigos_secundarios', 
            'movil_patrulla', 'a_cargo', 'secundante', 'lugar_codigo', 'descripcion', 
            'instituciones_intervinientes', 'tareas_judiciales', 'estado', 
            'instituciones_hospitalarias', 'dependencias_municipales', 'dependencias_provinciales', 'servicios_emergencia', 'instituciones_federales'
        ]
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'estado': forms.CheckboxInput(attrs={'class': 'sr-only peer'}),
        }

# Formulario específico para ComisariaPrimera, basado en BaseComisariaForm
class ComisariaPrimeraForm(BaseComisariaForm):
    class Meta(BaseComisariaForm.Meta):
        model = ComisariaPrimera

# Formulario específico para ComisariaSegunda, basado en BaseComisariaForm
class ComisariaSegundaForm(BaseComisariaForm):
    class Meta(BaseComisariaForm.Meta):
        model = ComisariaSegunda

# Formulario específico para ComisariaTercera, basado en BaseComisariaForm
class ComisariaTerceraForm(BaseComisariaForm):
    class Meta(BaseComisariaForm.Meta):
        model = ComisariaTercera

# Formulario específico para ComisariaCuarta, basado en BaseComisariaForm
class ComisariaCuartaForm(BaseComisariaForm):
    class Meta(BaseComisariaForm.Meta):
        model = ComisariaCuarta

# Formulario específico para ComisariaQuinta, basado en BaseComisariaForm
class ComisariaQuintaForm(BaseComisariaForm):
    class Meta(BaseComisariaForm.Meta):
        model = ComisariaQuinta
