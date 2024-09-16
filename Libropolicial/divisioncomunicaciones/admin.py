from django.contrib import admin
from .models import EncargadoGuardia, PersonalGuardia, CuartoGuardiaUSH

# Admin para CuartoGuardiaUSH con opción de activar/desactivar
@admin.register(CuartoGuardiaUSH)
class CuartoGuardiaUSHAdmin(admin.ModelAdmin):
    list_display = ('cuarto', 'activo')  # Mostrar si está activo o no
    search_fields = ('cuarto',)
    list_filter = ('activo',)  # Agregar filtro por activos


@admin.register(EncargadoGuardia)
class EncargadoGuardiaAdmincomunucaciones(admin.ModelAdmin):
    list_display = ('nombre_apellido', 'activo')  # Mostrar si está activo o no en el admin
    search_fields = ('nombre_apellido',)
    list_filter = ('activo',)  # Agregar filtro por activos


@admin.register(PersonalGuardia)
class PersonalGuardiaAdmin(admin.ModelAdmin):
    list_display = ('nombre_apellido', 'activo')  # Mostrar si está activo o no
    search_fields = ('nombre_apellido',)
    list_filter = ('activo',)  # Agregar filtro por activos
