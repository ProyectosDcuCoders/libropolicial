from django.urls import path
from .views import (
    generate_comisaria_primera_pdf_view, generate_comisaria_primera_pdf_download,
    generate_comisaria_segunda_pdf_view, generate_comisaria_segunda_pdf_download,
    generate_comisaria_tercera_pdf_view, generate_comisaria_tercera_pdf_download,
    generate_comisaria_cuarta_pdf_view, generate_comisaria_cuarta_pdf_download,
    generate_comisaria_quinta_pdf_view, generate_comisaria_quinta_pdf_download,
    ComisariaPrimeraListView, ComisariaSegundaListView, ComisariaTerceraListView,
    ComisariaCuartaListView, ComisariaQuintaListView, ComisariaPrimeraCreateView,
    ComisariaSegundaCreateView, ComisariaTerceraCreateView, ComisariaCuartaCreateView,
    ComisariaQuintaCreateView, ComisariasCompletaListView, ComisariaPrimeraUpdateView,
    ComisariaSegundaUpdateView
)

# Definición de las URL patterns para las vistas de las comisarías
urlpatterns = [
    # URL para listar registros de ComisariaPrimera
    path('primera/', ComisariaPrimeraListView.as_view(), name='comisaria_primera_list'),
    # URL para crear un nuevo registro en ComisariaPrimera
    path('primera/nuevo/', ComisariaPrimeraCreateView.as_view(), name='comisaria_primera_create'),
    # URL para editar un registro existente en ComisariaPrimera
    path('primera/editar/<int:pk>/', ComisariaPrimeraUpdateView.as_view(), name='comisaria_primera_edit'),
    # URL para ver el PDF de los registros de ComisariaPrimera
    path('primera/reporte/', generate_comisaria_primera_pdf_view, name='generate_comisaria_primera_pdf_view'),
    # URL para descargar el PDF de los registros de ComisariaPrimera
    path('primera/reporte/download/', generate_comisaria_primera_pdf_download, name='generate_comisaria_primera_pdf_download'),

    # URL para listar registros de ComisariaSegunda
    path('segunda/', ComisariaSegundaListView.as_view(), name='comisaria_segunda_list'),
    # URL para crear un nuevo registro en ComisariaSegunda
    path('segunda/nuevo/', ComisariaSegundaCreateView.as_view(), name='comisaria_segunda_create'),
    # URL para editar un registro existente en ComisariaSegunda
    path('segunda/editar/<int:pk>/', ComisariaSegundaUpdateView.as_view(), name='comisaria_segunda_edit'),
    # URL para ver el PDF de los registros de ComisariaSegunda
    path('segunda/reporte/', generate_comisaria_segunda_pdf_view, name='generate_comisaria_segunda_pdf_view'),
    # URL para descargar el PDF de los registros de ComisariaSegunda
    path('segunda/reporte/download/', generate_comisaria_segunda_pdf_download, name='generate_comisaria_segunda_pdf_download'),

    # URL para listar registros de ComisariaTercera
    path('tercera/', ComisariaTerceraListView.as_view(), name='comisaria_tercera_list'),
    # URL para crear un nuevo registro en ComisariaTercera
    path('tercera/nuevo/', ComisariaTerceraCreateView.as_view(), name='comisaria_tercera_create'),
    # URL para ver el PDF de los registros de ComisariaTercera
    path('tercera/reporte/', generate_comisaria_tercera_pdf_view, name='generate_comisaria_tercera_pdf_view'),
    # URL para descargar el PDF de los registros de ComisariaTercera
    path('tercera/reporte/download/', generate_comisaria_tercera_pdf_download, name='generate_comisaria_tercera_pdf_download'),

    # URL para listar registros de ComisariaCuarta
    path('cuarta/', ComisariaCuartaListView.as_view(), name='comisaria_cuarta_list'),
    # URL para crear un nuevo registro en ComisariaCuarta
    path('cuarta/nuevo/', ComisariaCuartaCreateView.as_view(), name='comisaria_cuarta_create'),
    # URL para ver el PDF de los registros de ComisariaCuarta
    path('cuarta/reporte/', generate_comisaria_cuarta_pdf_view, name='generate_comisaria_cuarta_pdf_view'),
    # URL para descargar el PDF de los registros de ComisariaCuarta
    path('cuarta/reporte/download/', generate_comisaria_cuarta_pdf_download, name='generate_comisaria_cuarta_pdf_download'),

    # URL para listar registros de ComisariaQuinta
    path('quinta/', ComisariaQuintaListView.as_view(), name='comisaria_quinta_list'),
    # URL para crear un nuevo registro en ComisariaQuinta
    path('quinta/nuevo/', ComisariaQuintaCreateView.as_view(), name='comisaria_quinta_create'),
    # URL para ver el PDF de los registros de ComisariaQuinta
    path('quinta/reporte/', generate_comisaria_quinta_pdf_view, name='generate_comisaria_quinta_pdf_view'),
    # URL para descargar el PDF de los registros de ComisariaQuinta
    path('quinta/reporte/download/', generate_comisaria_quinta_pdf_download, name='generate_comisaria_quinta_pdf_download'),

    # URL para listar registros combinados de todas las comisarías
    path('completas/', ComisariasCompletaListView.as_view(), name='comisarias_completa_list'),
]
