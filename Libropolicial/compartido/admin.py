from django.contrib import admin
from .models import CodigoPolicialUSH, CodigosSecundarios, CuartoGuardiaUSH

# Register your models here.
# Admin para CuartoGuardiaUSH con opción de activar/desactivar
@admin.register(CuartoGuardiaUSH)
class CuartoGuardiaUSHAdmin(admin.ModelAdmin):
    list_display = ('cuarto', 'activo')  # Mostrar si está activo o no
    search_fields = ('cuarto',)
    list_filter = ('activo',)  # Agregar filtro por activos

# Admin para CodigoPolicialUSH con opción de activar/desactivar
@admin.register(CodigoPolicialUSH)
class CodigoPolicialUSHAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'activo')  # Mostrar si está activo o no
    search_fields = ('codigo',)
    list_filter = ('activo',)  # Agregar filtro por activos

# Admin para CodigosSecundarios con opción de activar/desactivar
@admin.register(CodigosSecundarios)
class CodigosSecundariosAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'activo')  # Mostrar si está activo o no
    search_fields = ('codigo',)
    list_filter = ('activo',)  # Agregar filtro por activos