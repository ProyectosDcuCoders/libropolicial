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
    fecha_hora = models.DateTimeField()
    codigo = models.ForeignKey(CodigoPolicialUSH, null=True, blank=True, on_delete=models.SET_NULL)
    movil_patrulla = models.CharField(max_length=255)
    a_cargo = models.CharField(max_length=255)
    secundante = models.CharField(max_length=255)
    lugar_codigo = models.CharField(max_length=255, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    instituciones_intervinientes = models.TextField(null=True, blank=True)
    tareas_judiciales = models.TextField(null=True, blank=True)
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

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
