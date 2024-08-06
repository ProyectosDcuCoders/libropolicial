
# libropolicial/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('compartido.urls')),  # Incluir las rutas de 'compartido'
    path('comisarias/', include('comisarias.urls')),
    path('comisarias/', include('comisariasriogrande.urls')),
    path('divisioncomunicaciones/', include('divisioncomunicaciones.urls')),
    # Incluye otras aplicaciones de la misma manera
]
