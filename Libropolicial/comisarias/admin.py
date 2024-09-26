from django.contrib import admin

from django.contrib import admin
from .models import (  
    DependenciasSecundarias, SolicitanteCodigo, ServiciosEmergencia, 
    InstitucionesHospitalarias, DependenciasMunicipales, DependenciasProvinciales
)


# Admin para DependenciasSecundarias con opción de activar/desactivar
@admin.register(DependenciasSecundarias)
class DependenciasSecundariasAdmin(admin.ModelAdmin):
    list_display = ('dependencia', 'activo')  # Mostrar si está activo o no
    search_fields = ('dependencia',)
    list_filter = ('activo',)  # Agregar filtro por activos

# Admin para SolicitanteCodigo con opción de activar/desactivar
@admin.register(SolicitanteCodigo)
class SolicitanteCodigoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'activo')  # Mostrar si está activo o no
    search_fields = ('codigo',)
    list_filter = ('activo',)  # Agregar filtro por activos

# Admin para ServiciosEmergencia con opción de activar/desactivar
@admin.register(ServiciosEmergencia)
class ServiciosEmergenciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')  # Mostrar si está activo o no
    search_fields = ('nombre',)
    list_filter = ('activo',)  # Agregar filtro por activos

# Admin para InstitucionesHospitalarias con opción de activar/desactivar
@admin.register(InstitucionesHospitalarias)
class InstitucionesHospitalariasAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')  # Mostrar si está activo o no
    search_fields = ('nombre',)
    list_filter = ('activo',)  # Agregar filtro por activos

# Admin para DependenciasMunicipales con opción de activar/desactivar
@admin.register(DependenciasMunicipales)
class DependenciasMunicipalesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')  # Mostrar si está activo o no
    search_fields = ('nombre',)
    list_filter = ('activo',)  # Agregar filtro por activos

# Admin para DependenciasProvinciales con opción de activar/desactivar
@admin.register(DependenciasProvinciales)
class DependenciasProvincialesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')  # Mostrar si está activo o no
    search_fields = ('nombre',)
    list_filter = ('activo',)  # Agregar filtro por activos
