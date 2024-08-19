# libropolicial/urls.py

from django.contrib import admin
from django.urls import path, include

# Define las rutas (URL patterns) principales para el proyecto
urlpatterns = [
    # Ruta para la interfaz de administración de Django
    path('admin/', admin.site.urls),

    # Incluye las rutas definidas en 'compartido.urls'
    path('', include('compartido.urls')),

    # Incluye las rutas definidas en 'comisarias.urls'
    path('comisarias/', include('comisarias.urls')),

    # Incluye las rutas definidas en 'comisariasriogrande.urls'
    path('comisarias/', include('comisariasriogrande.urls')),

    # Incluye las rutas definidas en 'divisioncomunicaciones.urls'
    path('divisioncomunicaciones/', include('divisioncomunicaciones.urls')),

    # Puedes incluir otras aplicaciones de la misma manera
]
