# models.py
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class CodigoPolicialUSH(models.Model):
    codigo = models.CharField(max_length=10)

    def __str__(self):
        return self.codigo

class CodigosSecundarios(models.Model):
    codigo = models.CharField(max_length=10)

    def __str__(self):
        return self.codigo

class CuartoGuardiaUSH(models.Model):
    cuarto = models.CharField(max_length=1)

    def __str__(self):
        return self.cuarto

class BaseComisaria(models.Model):
    cuarto = models.ForeignKey(CuartoGuardiaUSH, null=True, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(default=timezone.now)
    codigo = models.ForeignKey(CodigoPolicialUSH, null=True, blank=True, on_delete=models.SET_NULL)
    codigos_secundarios = models.ManyToManyField(CodigosSecundarios,null=True, blank=True)
    movil_patrulla = models.CharField(max_length=255, null=True, blank=True)
    a_cargo = models.CharField(max_length=255, null=True, blank=True)
    secundante = models.CharField(max_length=255, null=True, blank=True)
    lugar_codigo = models.CharField(max_length=255, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    instituciones_intervinientes = models.TextField(null=True, blank=True)
    tareas_judiciales = models.TextField(null=True, blank=True)
    estado = models.BooleanField(default=True)
    firmas = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='%(class)s_created_records')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='%(class)s_updated_records')

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

class ResolucionCodigo(models.Model):
    comisaria_primera = models.ForeignKey(ComisariaPrimera, null=True, blank=True, on_delete=models.CASCADE, related_name='resoluciones')
    comisaria_segunda = models.ForeignKey(ComisariaSegunda, null=True, blank=True, on_delete=models.CASCADE, related_name='resoluciones')
    comisaria_tercera = models.ForeignKey(ComisariaTercera, null=True, blank=True, on_delete=models.CASCADE, related_name='resoluciones')
    comisaria_cuarta = models.ForeignKey(ComisariaCuarta, null=True, blank=True, on_delete=models.CASCADE, related_name='resoluciones')
    comisaria_quinta = models.ForeignKey(ComisariaQuinta, null=True, blank=True, on_delete=models.CASCADE, related_name='resoluciones')
    resolucion_codigo = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='resolucion_codigo_created')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='resolucion_codigo_updated')

    def __str__(self):
        return f"Resolucion {self.pk}"
