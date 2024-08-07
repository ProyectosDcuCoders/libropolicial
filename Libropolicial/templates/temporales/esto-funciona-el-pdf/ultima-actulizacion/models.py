from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Modelo para códigos policiales
class CodigoPolicialUSH(models.Model):
    codigo = models.CharField(max_length=10)  # Campo de texto para almacenar un código policial, con una longitud máxima de 3 caracteres

    def __str__(self):
        return self.codigo  # Método para devolver el código como una cadena

# Modelo para códigos secundarios
class CodigosSecundarios(models.Model):
    codigo = models.CharField(max_length=10)

    def __str__(self):
        return self.codigo

# Modelo para cuartos de guardia
class CuartoGuardiaUSH(models.Model):
    cuarto = models.CharField(max_length=1)  # Campo de texto para almacenar un cuarto de guardia, con una longitud máxima de 1 carácter

    def __str__(self):
        return self.cuarto  # Método para devolver el cuarto como una cadena

# Modelo base abstracto para las comisarías
class BaseComisaria(models.Model):
    cuarto = models.ForeignKey(CuartoGuardiaUSH, null=True, on_delete=models.CASCADE)  # Relación de clave foránea con CuartoGuardiaUSH, permite nulos, elimina en cascada
    fecha_hora = models.DateTimeField(default=timezone.now)  # Campo de fecha y hora con valor predeterminado de la hora actual
    codigo = models.ForeignKey(CodigoPolicialUSH, null=True, blank=True, on_delete=models.SET_NULL)  # Relación de clave foránea con CodigoPolicialUSH, permite nulos y valores en blanco, establece nulo en eliminación
    codigos_secundarios = models.ManyToManyField(CodigosSecundarios, blank=True)  # Nuevo campo ManyToMany
    movil_patrulla = models.CharField(max_length=255, null=True, blank=True)  # Campo de texto para móvil patrulla, permite nulos y valores en blanco
    a_cargo = models.CharField(max_length=255, null=True, blank=True)  # Campo de texto para responsable a cargo, permite nulos y valores en blanco
    secundante = models.CharField(max_length=255, null=True, blank=True)  # Campo de texto para el secundante, permite nulos y valores en blanco
    lugar_codigo = models.CharField(max_length=255, null=True, blank=True)  # Campo de texto para el lugar del código, permite nulos y valores en blanco
    descripcion = models.TextField(null=True, blank=True)  # Campo de texto largo para la descripción, permite nulos y valores en blanco
    instituciones_intervinientes = models.TextField(null=True, blank=True)  # Campo de texto largo para instituciones intervinientes, permite nulos y valores en blanco
    tareas_judiciales = models.TextField(null=True, blank=True)  # Campo de texto largo para tareas judiciales, permite nulos y valores en blanco
    estado = models.BooleanField(default=True)  # Campo booleano para el estado, valor predeterminado True
    created_at = models.DateTimeField(auto_now_add=True)  # Campo de fecha y hora de creación, se establece automáticamente al crear
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación de clave foránea con User, elimina en cascada
    updated_at = models.DateTimeField(auto_now=True)  # Campo de fecha y hora de actualización, se actualiza automáticamente
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación de clave foránea con User, elimina en cascada

    class Meta:
        abstract = True  # Define que este modelo es abstracto y no se creará una tabla en la base de datos

# Modelo específico para ComisariaPrimera, hereda de BaseComisaria
class ComisariaPrimera(BaseComisaria):
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='comisaria_primera_created_records')  # Clave foránea con User, permite nulos, elimina en cascada, nombre relacionado
    updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='comisaria_primera_updated_records')  # Clave foránea con User, permite nulos, elimina en cascada, nombre relacionado

# Modelo específico para ComisariaSegunda, hereda de BaseComisaria
class ComisariaSegunda(BaseComisaria):
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='comisaria_segunda_created_records')  # Clave foránea con User, permite nulos, elimina en cascada, nombre relacionado
    updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='comisaria_segunda_updated_records')  # Clave foránea con User, permite nulos, elimina en cascada, nombre relacionado

# Modelo específico para ComisariaTercera, hereda de BaseComisaria
class ComisariaTercera(BaseComisaria):
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='comisaria_tercera_created_records')  # Clave foránea con User, permite nulos, elimina en cascada, nombre relacionado
    updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='comisaria_tercera_updated_records')  # Clave foránea con User, permite nulos, elimina en cascada, nombre relacionado

# Modelo específico para ComisariaCuarta, hereda de BaseComisaria
class ComisariaCuarta(BaseComisaria):
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='comisaria_cuarta_created_records')  # Clave foránea con User, permite nulos, elimina en cascada, nombre relacionado
    updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='comisaria_cuarta_updated_records')  # Clave foránea con User, permite nulos, elimina en cascada, nombre relacionado

# Modelo específico para ComisariaQuinta, hereda de BaseComisaria
class ComisariaQuinta(BaseComisaria):
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='comisaria_quinta_created_records')  # Clave foránea con User, permite nulos, elimina en cascada, nombre relacionado
    updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='comisaria_quinta_updated_records')  # Clave foránea con User, permite nulos, elimina en cascada, nombre relacionado
