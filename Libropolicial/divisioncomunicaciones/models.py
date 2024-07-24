from django.db import models
from django.utils import timezone

class EncargadoGuardia(models.Model):
    nombre_apellido = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre_apellido

class PersonalGuardia(models.Model):
    nombre_apellido = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre_apellido

class DivisionComunicaciones(models.Model):
    inicio_guardia = models.DateTimeField(default=timezone.now)
    finalizacion_guardia = models.DateTimeField()
    encargado_guardia = models.ForeignKey(EncargadoGuardia, on_delete=models.CASCADE)
    solicitante = models.CharField(max_length=255)
    nombre_apellido = models.CharField(max_length=255)
    dni = models.IntegerField()
    telefono = models.CharField(max_length=20)
    movil_patrulla = models.CharField(max_length=255)
    personal_cargo = models.CharField(max_length=255)
    descripcion = models.TextField()
    intervencion_comisaria = models.CharField(max_length=255)
    personal_guardia = models.ManyToManyField(PersonalGuardia)

    def __str__(self):
        return f"{self.nombre_apellido} - {self.inicio_guardia.strftime('%Y-%m-%d %H:%M')}"
