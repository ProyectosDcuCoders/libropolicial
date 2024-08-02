from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class CodigoPolicialUSH(models.Model):
    codigo = models.CharField(max_length=3)

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
    movil_patrulla = models.CharField(max_length=255, null=True, blank=True)
    a_cargo = models.CharField(max_length=255, null=True, blank=True)
    secundante = models.CharField(max_length=255, null=True, blank=True)
    lugar_codigo = models.CharField(max_length=255, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    instituciones_intervinientes = models.TextField(null=True, blank=True)
    tareas_judiciales = models.TextField(null=True, blank=True)
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class ComisariaPrimera(BaseComisaria):
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='comisaria_primera_created_records')
    updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='comisaria_primera_updated_records')

class ComisariaSegunda(BaseComisaria):
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='comisaria_segunda_created_records')
    updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='comisaria_segunda_updated_records')

class ComisariaTercera(BaseComisaria):
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='comisaria_tercera_created_records')
    updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='comisaria_tercera_updated_records')

class ComisariaCuarta(BaseComisaria):
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='comisaria_cuarta_created_records')
    updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='comisaria_cuarta_updated_records')

class ComisariaQuinta(BaseComisaria):
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='comisaria_quinta_created_records')
    updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='comisaria_quinta_updated_records')
