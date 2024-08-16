from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Clases relacionadas con los códigos y dependencias

class CodigoPolicialUSH(models.Model):
    codigo = models.CharField(max_length=10)

    def __str__(self):
        return self.codigo

class CodigosSecundarios(models.Model):
    codigo = models.CharField(max_length=10)

    def __str__(self):
        return self.codigo

class DependenciasSecundarias(models.Model):
    dependencia = models.CharField(max_length=100)

    def __str__(self):
        return self.dependencia

class CuartoGuardiaUSH(models.Model):
    cuarto = models.CharField(max_length=1)

    def __str__(self):
        return self.cuarto

class SolicitanteCodigo(models.Model):
    codigo = models.CharField(max_length=100)

    def __str__(self):
        return self.codigo

# Nuevas clases ManyToMany para hospitales, dependencias y servicios

class InstitucionesHospitalarias(models.Model):
    nombre = models.CharField(max_length=60)

    def __str__(self):
        return self.nombre

class DependenciasMunicipales(models.Model):
    nombre = models.CharField(max_length=60)

    def __str__(self):
        return self.nombre

class DependenciasProvinciales(models.Model):
    nombre = models.CharField(max_length=60)

    def __str__(self):
        return self.nombre

class ServiciosEmergencia(models.Model):
    nombre = models.CharField(max_length=60)

    def __str__(self):
        return self.nombre

# Modelos de las comisarías específicos (concretos)

class BaseComisaria(models.Model):
    cuarto = models.ForeignKey(CuartoGuardiaUSH, null=True, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(default=timezone.now)
    codigo = models.ForeignKey(CodigoPolicialUSH, null=True, blank=True, on_delete=models.SET_NULL)
    solicitante_codigo = models.ForeignKey(SolicitanteCodigo, null=True, blank=True, on_delete=models.SET_NULL)
    codigos_secundarios = models.ManyToManyField(CodigosSecundarios, blank=True)
    dependencias_secundarias = models.ManyToManyField(DependenciasSecundarias, blank=True)
    movil_patrulla = models.CharField(max_length=255, null=True, blank=True)
    a_cargo = models.CharField(max_length=255, null=True, blank=True)
    secundante = models.CharField(max_length=255, null=True, blank=True)
    lugar_codigo = models.CharField(max_length=255, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    instituciones_intervinientes = models.TextField(null=True, blank=True)
    tareas_judiciales = models.TextField(null=True, blank=True)
    estado = models.BooleanField(default=True)
    firmas = models.TextField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='%(class)s_created_records')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='%(class)s_updated_records')

    # Nuevos campos ManyToMany
    instituciones_hospitalarias = models.ManyToManyField(InstitucionesHospitalarias, blank=True)
    dependencias_municipales = models.ManyToManyField(DependenciasMunicipales, blank=True)
    dependencias_provinciales = models.ManyToManyField(DependenciasProvinciales, blank=True)
    servicios_emergencia = models.ManyToManyField(ServiciosEmergencia, blank=True)

    class Meta:
        abstract = True

class ComisariaPrimera(BaseComisaria):
    pass

class ComisariaSegunda(BaseComisaria):
    pass

class ComisariaTercera(BaseComisaria):
    pass

class ComisariaCuarta(BaseComisaria):
    pass

class ComisariaQuinta(BaseComisaria):
    pass

# Clase para manejar los detalles adicionales de ServiciosEmergencia

class DetalleServicioEmergencia(models.Model):
    servicio_emergencia = models.ForeignKey(ServiciosEmergencia, on_delete=models.CASCADE)
    comisaria_primera = models.ForeignKey(ComisariaPrimera, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_servicio_emergencia')
    comisaria_segunda = models.ForeignKey(ComisariaSegunda, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_servicio_emergencia')
    comisaria_tercera = models.ForeignKey(ComisariaTercera, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_servicio_emergencia')
    comisaria_cuarta = models.ForeignKey(ComisariaCuarta, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_servicio_emergencia')
    comisaria_quinta = models.ForeignKey(ComisariaQuinta, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_servicio_emergencia')
    numero_movil_bomberos = models.CharField(max_length=20, null=True, blank=True)
    nombre_a_cargo_bomberos = models.CharField(max_length=255, null=True, blank=True)


# Clase para manejar los detalles adicionales de Instituciones Hospitalarias
class DetalleInstitucionHospitalaria(models.Model):
    institucion_hospitalaria = models.ForeignKey(InstitucionesHospitalarias, on_delete=models.CASCADE)
    comisaria_primera = models.ForeignKey(ComisariaPrimera, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_institucion_hospitalaria')
    comisaria_segunda = models.ForeignKey(ComisariaSegunda, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_institucion_hospitalaria')
    comisaria_tercera = models.ForeignKey(ComisariaTercera, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_institucion_hospitalaria')
    comisaria_cuarta = models.ForeignKey(ComisariaCuarta, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_institucion_hospitalaria')
    comisaria_quinta = models.ForeignKey(ComisariaQuinta, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_institucion_hospitalaria')
    numero_movil_hospital = models.CharField(max_length=20, null=True, blank=True)
    nombre_a_cargo_hospital = models.CharField(max_length=255, null=True, blank=True)

# Clase para manejar los detalles adicionales de Dependencias Municipales
class DetalleDependenciaMunicipal(models.Model):
    dependencia_municipal = models.ForeignKey(DependenciasMunicipales, on_delete=models.CASCADE)
    comisaria_primera = models.ForeignKey(ComisariaPrimera, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_municipal')
    comisaria_segunda = models.ForeignKey(ComisariaSegunda, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_municipal')
    comisaria_tercera = models.ForeignKey(ComisariaTercera, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_municipal')
    comisaria_cuarta = models.ForeignKey(ComisariaCuarta, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_municipal')
    comisaria_quinta = models.ForeignKey(ComisariaQuinta, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_municipal')
    numero_movil_municipal = models.CharField(max_length=20, null=True, blank=True)
    nombre_a_cargo_municipal = models.CharField(max_length=255, null=True, blank=True)

# Clase para manejar los detalles adicionales de Dependencias Provinciales
class DetalleDependenciaProvincial(models.Model):
    dependencia_provincial = models.ForeignKey(DependenciasProvinciales, on_delete=models.CASCADE)
    comisaria_primera = models.ForeignKey(ComisariaPrimera, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_provincial')
    comisaria_segunda = models.ForeignKey(ComisariaSegunda, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_provincial')
    comisaria_tercera = models.ForeignKey(ComisariaTercera, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_provincial')
    comisaria_cuarta = models.ForeignKey(ComisariaCuarta, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_provincial')
    comisaria_quinta = models.ForeignKey(ComisariaQuinta, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_provincial')
    numero_movil_provincial = models.CharField(max_length=20, null=True, blank=True)
    nombre_a_cargo_provincial = models.CharField(max_length=255, null=True, blank=True)


