from django.contrib import admin
from .models import CuartoGuardiaUSH

# Register your models here.
# Admin para CuartoGuardiaUSH con opción de activar/desactivar
@admin.register(CuartoGuardiaUSH)
class CuartoGuardiaUSHAdmin(admin.ModelAdmin):
    list_display = ('cuarto', 'activo')  # Mostrar si está activo o no
    search_fields = ('cuarto',)
    list_filter = ('activo',)  # Agregar filtro por activos
