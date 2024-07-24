# Libropolicial/comisariasriogrande/urls.py
from django.urls import path
from .views import ComisariaPrimeraRGListView, ComisariaPrimeraRGCreateView, ComisariaPrimeraRGUpdateView, ComisariaSegundaRGListView, ComisariaSegundaRGCreateView, ComisariaSegundaRGUpdateView, ComisariaTerceraRGListView, ComisariaCuartaRGListView, ComisariaQuintaRGListView, no_permission

urlpatterns = [
   
    path('primera/', ComisariaPrimeraRGListView.as_view(), name='comisaria_primera_rg_list'),
    path('primera/nuevo/', ComisariaPrimeraRGCreateView.as_view(), name='comisaria_primera_rg_create'),
    path('primera/editar/<int:pk>/', ComisariaPrimeraRGUpdateView.as_view(), name='comisaria_primera_rg_edit'),
    path('segunda/', ComisariaSegundaRGListView.as_view(), name='comisaria_segunda_rg_list'),
    path('segunda/nuevo/', ComisariaSegundaRGCreateView.as_view(), name='comisaria_segunda_rg_create'),
    path('segunda/editar/<int:pk>/', ComisariaSegundaRGUpdateView.as_view(), name='comisaria_segunda_rg_edit'),
    path('tercera/', ComisariaTerceraRGListView.as_view(), name='comisaria_tercera_rg_list'),
    path('cuarta/', ComisariaCuartaRGListView.as_view(), name='comisaria_cuarta_rg_list'),
    path('quinta/', ComisariaQuintaRGListView.as_view(), name='comisaria_quinta_rg_list'),
    
]
