from django.db import models
from django.utils import timezone
from compartido.models import CuartoGuardiaUSH


class EncargadoGuardia(models.Model):
    nombre_apellido = models.CharField(max_length=255, null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_apellido

    # Sobrescribir el método delete para realizar soft delete
    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()



from django.db import models

# Modelo para el personal de guardia
class PersonalGuardia(models.Model):
    nombre_apellido = models.CharField(max_length=255, null=True, blank=True)
    activo = models.BooleanField(default=True)  # Campo para activar/desactivar el personal de guardia

    def __str__(self):
        return self.nombre_apellido

    # Sobrescribir el método delete para realizar soft delete
    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

    

#class CuartoGuardiaUSH(models.Model):
 #   cuarto = models.CharField(max_length=1)
  #  activo = models.BooleanField(default=True)  # Ensure this field exists

   # def __str__(self):
    #    return self.cuarto
    
    #def delete(self, *args, **kwargs):
     #   self.activo = False
      #  self.save()  
    


class DivisionComunicaciones(models.Model):
    inicio_guardia = models.DateTimeField(null=True, blank=True)
    finalizacion_guardia = models.DateTimeField(null=True, blank=True)
    cuarto = models.ForeignKey(CuartoGuardiaUSH, null=True, blank=True, on_delete=models.CASCADE)
    #cuarto = models.ForeignKey(CuartoGuardiaUSH, null=True, blank=True, on_delete=models.CASCADE)
    oficial_servicio = models.CharField(max_length=100, null=True, blank=True)
    encargado_guardia = models.ForeignKey(EncargadoGuardia, null=True, blank=True, on_delete=models.SET_NULL)  # Cambiar a SET_NULL
    personal_guardia = models.ManyToManyField(PersonalGuardia, blank=True, related_name='comunicaciones_guardia')
    distribucion_personal_moviles = models.TextField(null=True, blank=True)
    novedades = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Guardia {self.inicio_guardia} - {self.finalizacion_guardia}"


# Modelo para los eventos de tipo "Guardia Bis"
class EventoGuardiaBis(models.Model):
    EVENTO_CHOICES = [
        ('ENCARGADO DE GUARDIA', 'Encargado de Guardia'),
        ('OPERADOR Y LIBRO DE GUARDIA', 'Operador y Librero'),
        ('CONSIGNA', 'Consigna'),
        ('PUESTO LLAVERO', 'Puesto llavero'),
    ]

    guardia = models.ForeignKey(DivisionComunicaciones, related_name='eventosbis', on_delete=models.CASCADE)
    tipo_eventobis = models.CharField(max_length=50, choices=EVENTO_CHOICES, null=True, blank=True)
    nombre_jerarquia = models.CharField(max_length=255, null=True, blank=True)
    #nombre_jerarquia_librero = models.CharField(max_length=255, null=True, blank=True)
    #hora_evento = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.tipo_eventobis} - {self.nombre_jerarquia}"


# Modelo para los eventos de tipo "Guardia Bis Uno"
class EventoGuardiaBisUno(models.Model):
    EVENTO_CHOICES = [
        ('MOVIL', 'Movil'),
        ('PATRULLA', 'Patrulla'),
    ]

    guardia = models.ForeignKey(DivisionComunicaciones, related_name='eventosbisuno', on_delete=models.CASCADE)
    tipo_eventobisuno = models.CharField(max_length=50, choices=EVENTO_CHOICES, null=True, blank=True)
    movil_patrulla = models.CharField(max_length=100, null=True, blank=True)
    nombre_jerarquia_movil_patrulla = models.TextField(null=True, blank=True)
    #hora_evento = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.tipo_eventobisuno} - {self.movil_patrulla} - {self.nombre_jerarquia_movil_patrulla}"


# Modelo original de eventos de guardia
class EventoGuardia(models.Model):
    EVENTO_CHOICES = [
        ('PRESENTE', 'Presente'),
        ('INICIA', 'Inicia'),
        ('FINALIZA', 'Finaliza'),
        ('SE_RETIRA', 'Se Retira'),
        ('CONSTANCIA', 'Constancia'),
    ]

    guardia = models.ForeignKey(DivisionComunicaciones, related_name='eventos', on_delete=models.CASCADE)
    tipo_evento = models.CharField(max_length=20, choices=EVENTO_CHOICES, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    hora_evento = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.tipo_evento} - {self.hora_evento} - Guardia {self.guardia.inicio_guardia}"
