from django.urls import path
from .views import (
    generate_comisaria_primera_pdf, view_comisaria_primera_pdf,
    generate_comisaria_segunda_pdf, view_comisaria_segunda_pdf,
    generate_comisaria_tercera_pdf, view_comisaria_tercera_pdf,
    generate_comisaria_cuarta_pdf, view_comisaria_cuarta_pdf,
    generate_comisaria_quinta_pdf, view_comisaria_quinta_pdf,
    ComisariaPrimeraListView, ComisariaSegundaListView, ComisariaTerceraListView,
    ComisariaCuartaListView, ComisariaQuintaListView, ComisariaPrimeraCreateView,
    ComisariaSegundaCreateView, ComisariaTerceraCreateView, ComisariaCuartaCreateView,
    ComisariaQuintaCreateView, ComisariasCompletaListView, ComisariaPrimeraUpdateView,
    ComisariaSegundaUpdateView, no_permission
)

urlpatterns = [
    path('primera/', ComisariaPrimeraListView.as_view(), name='comisaria_primera_list'),
    path('primera/nuevo/', ComisariaPrimeraCreateView.as_view(), name='comisaria_primera_create'),
    path('primera/editar/<int:pk>/', ComisariaPrimeraUpdateView.as_view(), name='comisaria_primera_edit'),

    path('segunda/', ComisariaSegundaListView.as_view(), name='comisaria_segunda_list'),
    path('segunda/nuevo/', ComisariaSegundaCreateView.as_view(), name='comisaria_segunda_create'),
    path('segunda/editar/<int:pk>/', ComisariaSegundaUpdateView.as_view(), name='comisaria_segunda_edit'),

    path('tercera/', ComisariaTerceraListView.as_view(), name='comisaria_tercera_list'),
    path('cuarta/', ComisariaCuartaListView.as_view(), name='comisaria_cuarta_list'),
    path('quinta/', ComisariaQuintaListView.as_view(), name='comisaria_quinta_list'),
    
   
    path('tercera/nuevo/', ComisariaTerceraCreateView.as_view(), name='comisaria_tercera_create'),
    path('cuarta/nuevo/', ComisariaCuartaCreateView.as_view(), name='comisaria_cuarta_create'),
    path('quinta/nuevo/', ComisariaQuintaCreateView.as_view(), name='comisaria_quinta_create'),

    
    
    path('completas/', ComisariasCompletaListView.as_view(), name='comisarias_completa_list'),

    # Rutas para Comisaria Primera
    path('comisaria/primera/reporte/', view_comisaria_primera_pdf, name='view_comisaria_primera_pdf'),
    path('comisaria/primera/reporte/download/', generate_comisaria_primera_pdf, name='generate_comisaria_primera_pdf'),

    # Rutas para otras comisarias (similar a Comisaria Primera)
    path('comisaria/segunda/reporte/', view_comisaria_segunda_pdf, name='view_comisaria_segunda_pdf'),
    path('comisaria/segunda/reporte/download/', generate_comisaria_segunda_pdf, name='generate_comisaria_segunda_pdf'),

    path('comisaria/tercera/reporte/', view_comisaria_tercera_pdf, name='view_comisaria_tercera_pdf'),
    path('comisaria/tercera/reporte/download/', generate_comisaria_tercera_pdf, name='generate_comisaria_tercera_pdf'),

    path('comisaria/cuarta/reporte/', view_comisaria_cuarta_pdf, name='view_comisaria_cuarta_pdf'),
    path('comisaria/cuarta/reporte/download/', generate_comisaria_cuarta_pdf, name='generate_comisaria_cuarta_pdf'),

    path('comisaria/quinta/reporte/', view_comisaria_quinta_pdf, name='view_comisaria_quinta_pdf'),
    path('comisaria/quinta/reporte/download/', generate_comisaria_quinta_pdf, name='generate_comisaria_quinta_pdf'),
]
