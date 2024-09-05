from Libropolicial.forms import CustomLoginForm
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import (
    ComisariaPrimera, ComisariaSegunda, ComisariaTercera, 
    ComisariaCuarta, ComisariaQuinta, CodigoPolicialUSH, 
    CodigosSecundarios, DependenciasSecundarias, CuartoGuardiaUSH,
    InstitucionesHospitalarias, DependenciasMunicipales, DependenciasProvinciales,
    ServiciosEmergencia, DetalleServicioEmergencia, DetalleInstitucionHospitalaria,
    DetalleDependenciaMunicipal, DetalleDependenciaProvincial, SolicitanteCodigo
)

# Formulario para DetalleServicioEmergencia
class DetalleServicioEmergenciaForm(forms.ModelForm):
    class Meta:
        model = DetalleServicioEmergencia  # Asocia el formulario con el modelo DetalleServicioEmergencia
        fields = ['servicio_emergencia', 'numero_movil_bomberos', 'nombre_a_cargo_bomberos']  # Define los campos que serán incluidos en el formulario
        widgets = {
            'servicio_emergencia': forms.HiddenInput(),  # Campo oculto para el servicio de emergencia
            'numero_movil_bomberos': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),  # Campo de texto para el número móvil con estilos
            'nombre_a_cargo_bomberos': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),  # Campo de texto para el nombre a cargo con estilos
        }

# Formulario para DetalleInstitucionHospitalaria
class DetalleInstitucionHospitalariaForm(forms.ModelForm):
    class Meta:
        model = DetalleInstitucionHospitalaria  # Asocia el formulario con el modelo DetalleInstitucionHospitalaria
        fields = ['institucion_hospitalaria', 'numero_movil_hospital', 'nombre_a_cargo_hospital']  # Define los campos que serán incluidos en el formulario
        widgets = {
            'institucion_hospitalaria': forms.HiddenInput(),  # Campo oculto para la institución hospitalaria
            'numero_movil_hospital': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),  # Campo de texto para el número móvil con estilos
            'nombre_a_cargo_hospital': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),  # Campo de texto para el nombre a cargo con estilos
        }

# Formulario para DetalleDependenciaMunicipal
class DetalleDependenciaMunicipalForm(forms.ModelForm):
    class Meta:
        model = DetalleDependenciaMunicipal  # Asocia el formulario con el modelo DetalleDependenciaMunicipal
        fields = ['dependencia_municipal', 'numero_movil_municipal', 'nombre_a_cargo_municipal']  # Define los campos que serán incluidos en el formulario
        widgets = {
            'dependencia_municipal': forms.HiddenInput(),  # Campo oculto para la dependencia municipal
            'numero_movil_municipal': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),  # Campo de texto para el número móvil con estilos
            'nombre_a_cargo_municipal': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),  # Campo de texto para el nombre a cargo con estilos
        }

# Formulario para DetalleDependenciaProvincial
class DetalleDependenciaProvincialForm(forms.ModelForm):
    class Meta:
        model = DetalleDependenciaProvincial  # Asocia el formulario con el modelo DetalleDependenciaProvincial
        fields = ['dependencia_provincial', 'numero_movil_provincial', 'nombre_a_cargo_provincial']  # Define los campos que serán incluidos en el formulario
        widgets = {
            'dependencia_provincial': forms.HiddenInput(),  # Campo oculto para la dependencia provincial
            'numero_movil_provincial': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),  # Campo de texto para el número móvil con estilos
            'nombre_a_cargo_provincial': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),  # Campo de texto para el nombre a cargo con estilos
        }

# Formulario base para las comisarías
class BaseComisariaForm(forms.ModelForm):
    # Campo para seleccionar el cuarto de guardia
    cuarto = forms.ModelChoiceField(
        queryset=CuartoGuardiaUSH.objects.all(),  # Define el conjunto de opciones para el campo
        required=False,  # El campo no es obligatorio
        label='Cuarto',  # Etiqueta del campo
        widget=forms.Select(
            attrs={
                'class': 'cursor-pointer bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3 appearance-none'
            }
        )
    )

    # Campo para seleccionar el solicitante de código
    solicitante_codigo = forms.ModelChoiceField(
        queryset=SolicitanteCodigo.objects.all(),  # Define el conjunto de opciones para el campo
        required=False,  # El campo no es obligatorio
        label='Solicitante del Código',  # Etiqueta del campo
        widget=forms.Select(
            attrs={
                'class': 'cursor-pointer bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3 appearance-none'
            }
        )
    )

    # Campo para seleccionar el código policial principal
    codigo = forms.ModelChoiceField(
        queryset=CodigoPolicialUSH.objects.all(),  # Define el conjunto de opciones para el campo
        required=False,  # El campo no es obligatorio
        label='Código Principal',  # Etiqueta del campo
        widget=forms.Select(
            attrs={
                'class': 'cursor-pointer bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3 appearance-none',
                # 'style': 'font-size: 10px;'
            }
        )
    )

    # Campo para seleccionar las dependencias secundarias
    dependencias_secundarias = forms.ModelMultipleChoiceField(
        queryset=DependenciasSecundarias.objects.all(),  # Define el conjunto de opciones para el campo
        required=False,  # El campo no es obligatorio
        label='Dependencias Policiales',  # Etiqueta del campo
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'
            }
        )
    )

    # Campo para seleccionar múltiples códigos secundarios
    codigos_secundarios = forms.ModelMultipleChoiceField(
        queryset=CodigosSecundarios.objects.all(),  # Define el conjunto de opciones para el campo
        required=False,  # El campo no es obligatorio
        label='Códigos Secundarios',  # Etiqueta del campo
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'
            }
        )
    )

    # Campo para seleccionar múltiples instituciones hospitalarias
    instituciones_hospitalarias = forms.ModelMultipleChoiceField(
        queryset=InstitucionesHospitalarias.objects.all(),  # Define el conjunto de opciones para el campo
        required=False,  # El campo no es obligatorio
        label='Instituciones Hospitalarias',  # Etiqueta del campo
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'
            }
        )
    )

    # Campo para seleccionar múltiples dependencias municipales
    dependencias_municipales = forms.ModelMultipleChoiceField(
        queryset=DependenciasMunicipales.objects.all(),  # Define el conjunto de opciones para el campo
        required=False,  # El campo no es obligatorio
        label='Dependencias Municipales',  # Etiqueta del campo
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'
            }
        )
    )

    # Campo para seleccionar múltiples dependencias provinciales
    dependencias_provinciales = forms.ModelMultipleChoiceField(
        queryset=DependenciasProvinciales.objects.all(),  # Define el conjunto de opciones para el campo
        required=False,  # El campo no es obligatorio
        label='Dependencias Provinciales',  # Etiqueta del campo
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'
            }
        )
    )

    # Campo para seleccionar múltiples servicios de emergencia
    servicios_emergencia = forms.ModelMultipleChoiceField(
        queryset=ServiciosEmergencia.objects.all(),  # Define el conjunto de opciones para el campo
        required=False,  # El campo no es obligatorio
        label='Servicios de Emergencia Bomberil',  # Etiqueta del campo
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
        label='Descripción',  # Etiqueta del campo
        required=False  # El campo no es obligatorio
    )

    class Meta:
        fields = [
            'cuarto', 'fecha_hora', 'codigo', 'solicitante_codigo','dependencias_secundarias', 'codigos_secundarios', 
            'movil_patrulla', 'a_cargo', 'secundante', 'lugar_codigo', 
            'descripcion', 'instituciones_intervinientes', 'tareas_judiciales', 
            'estado', 'instituciones_hospitalarias', 'dependencias_municipales',
            'dependencias_provinciales', 'servicios_emergencia'
        ]  # Define los campos que serán incluidos en el formulario
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # Widget para seleccionar la fecha y hora
            'estado': forms.CheckboxInput(attrs={'class': 'sr-only peer'}),  # Widget para el checkbox del estado
        }

# Formulario específico para ComisariaPrimera, basado en BaseComisariaForm
class ComisariaPrimeraForm(BaseComisariaForm):
    class Meta(BaseComisariaForm.Meta):
        model = ComisariaPrimera  # Asocia el formulario con el modelo ComisariaPrimera

# Formulario específico para ComisariaSegunda, basado en BaseComisariaForm
class ComisariaSegundaForm(BaseComisariaForm):
    class Meta(BaseComisariaForm.Meta):
        model = ComisariaSegunda  # Asocia el formulario con el modelo ComisariaSegunda

# Formulario específico para ComisariaTercera, basado en BaseComisariaForm
class ComisariaTerceraForm(BaseComisariaForm):
    class Meta(BaseComisariaForm.Meta):
        model = ComisariaTercera  # Asocia el formulario con el modelo ComisariaTercera

# Formulario específico para ComisariaCuarta, basado en BaseComisariaForm
class ComisariaCuartaForm(BaseComisariaForm):
    class Meta(BaseComisariaForm.Meta):
        model = ComisariaCuarta  # Asocia el formulario con el modelo ComisariaCuarta

# Formulario específico para ComisariaQuinta, basado en BaseComisariaForm
class ComisariaQuintaForm(BaseComisariaForm):
    class Meta(BaseComisariaForm.Meta):
        model = ComisariaQuinta  # Asocia el formulario con el modelo ComisariaQuinta
