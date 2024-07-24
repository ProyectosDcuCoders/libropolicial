from django.db import models
from django.utils import timezone

class CodigoPolicialRG(models.Model):
    codigo = models.CharField(max_length=3)

    def __str__(self):
        return self.codigo

class CuartoGuardiaRG(models.Model):
    cuarto = models.CharField(max_length=1)

    def __str__(self):
        return self.cuarto

class BaseComisariaRG(models.Model):
    codigo = models.ForeignKey(CodigoPolicialRG, null=True, on_delete=models.CASCADE)
    movil_patrulla = models.CharField(max_length=255)
    a_cargo = models.CharField(max_length=255)
    secundante = models.CharField(max_length=255)
    nombre_victima = models.CharField(max_length=255)
    dni = models.IntegerField()
    sexo = models.BooleanField()
    estado_civil = models.CharField(max_length=255)
    domicilio = models.CharField(max_length=255)
    trabajo = models.CharField(max_length=255)
    descripcion = models.TextField()
    cuarto = models.ForeignKey(CuartoGuardiaRG, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

class ComisariaPrimeraRG(BaseComisariaRG):
    pass

class ComisariaSegundaRG(BaseComisariaRG):
    pass

class ComisariaTerceraRG(BaseComisariaRG):
    pass

class ComisariaCuartaRG(BaseComisariaRG):
    pass

class ComisariaQuintaRG(BaseComisariaRG):
    pass
