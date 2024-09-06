#comisarial/urls.py
from django.urls import path
from .views import (
    generate_comisaria_primera_pdf_view, generate_comisaria_primera_pdf_download,
    generate_comisaria_segunda_pdf_view, generate_comisaria_segunda_pdf_download,
    generate_comisaria_tercera_pdf_view, generate_comisaria_tercera_pdf_download,
    generate_comisaria_cuarta_pdf_view, generate_comisaria_cuarta_pdf_download,
    generate_comisaria_quinta_pdf_view, generate_comisaria_quinta_pdf_download,
    sign_comisaria_primera, sign_comisaria_segunda,subir_pdf, ver_pdfs, mostrar_pdf,
    ComisariaPrimeraListView, ComisariaSegundaListView, ComisariaTerceraListView,
    ComisariaCuartaListView, ComisariaQuintaListView, ComisariaPrimeraCreateView,
    ComisariaSegundaCreateView, ComisariaTerceraCreateView, ComisariaCuartaCreateView,
    ComisariaQuintaCreateView, ComisariasCompletaListView, ComisariaPrimeraUpdateView,
    ComisariaSegundaUpdateView,ComisariaPrimeraDetailView,ComisariaSegundaDetailView,
    generate_comisaria_primera_pdf_download_previous_day, generate_comisaria_segunda_pdf_download_previous_day # <-- Asegúrate de incluir esta línea
)

urlpatterns = [
     path('primera/', ComisariaPrimeraListView.as_view(), name='comisaria_primera_list'),
    path('primera/create/', ComisariaPrimeraCreateView.as_view(), name='comisaria_primera_create'),
    path('primera/edit/<int:pk>/', ComisariaPrimeraUpdateView.as_view(), name='comisaria_primera_edit'),
    path('comisarias/primera/detalle/<int:pk>/', ComisariaPrimeraDetailView.as_view(), name='comisaria_primera_detail'),
    path('primera/reporte/view/', generate_comisaria_primera_pdf_view, name='generate_comisaria_primera_pdf_view'),
    path('primera/reporte/download/', generate_comisaria_primera_pdf_download, name='generate_comisaria_primera_pdf_download'),
    path('comisarias/primera/descargar-dia-anterior/', generate_comisaria_primera_pdf_download_previous_day, name='generate_comisaria_primera_pdf_download_previous_day'),  # <-- Esta es la ruta que debes agregar
    path('primera/firmar/<int:pk>/', sign_comisaria_primera, name='comisaria_primera_sign'),


    path('subir-pdf/', subir_pdf, name='subir_pdf'),
    path('ver-pdfs/', ver_pdfs, name='ver_pdfs'),  # Nueva URL para ver los PDFs
    path('mostrar-pdf/<int:pdf_id>/', mostrar_pdf, name='mostrar_pdf'),

    path('segunda/', ComisariaSegundaListView.as_view(), name='comisaria_segunda_list'),
    path('segunda/nuevo/', ComisariaSegundaCreateView.as_view(), name='comisaria_segunda_create'),
    path('segunda/editar/<int:pk>/', ComisariaSegundaUpdateView.as_view(), name='comisaria_segunda_edit'),
    path('comisarias/segunda/detalle/<int:pk>/', ComisariaSegundaDetailView.as_view(), name='comisaria_segunda_detail'),
    path('segunda/reporte/', generate_comisaria_segunda_pdf_view, name='generate_comisaria_segunda_pdf_view'),
    path('segunda/reporte/download/', generate_comisaria_segunda_pdf_download, name='generate_comisaria_segunda_pdf_download'),
    path('comisarias/segunda/descargar-dia-anterior/', generate_comisaria_segunda_pdf_download_previous_day, name='generate_comisaria_segunda_pdf_download_previous_day'),  # <-- Esta es la ruta que debes agregar
    path('segunda/firmar/<int:pk>/', sign_comisaria_segunda, name='comisaria_segunda_sign'),

    path('tercera/', ComisariaTerceraListView.as_view(), name='comisaria_tercera_list'),
    path('tercera/nuevo/', ComisariaTerceraCreateView.as_view(), name='comisaria_tercera_create'),
    path('tercera/reporte/', generate_comisaria_tercera_pdf_view, name='generate_comisaria_tercera_pdf_view'),
    path('tercera/reporte/download/', generate_comisaria_tercera_pdf_download, name='generate_comisaria_tercera_pdf_download'),

    path('cuarta/', ComisariaCuartaListView.as_view(), name='comisaria_cuarta_list'),
    path('cuarta/nuevo/', ComisariaCuartaCreateView.as_view(), name='comisaria_cuarta_create'),
    path('cuarta/reporte/', generate_comisaria_cuarta_pdf_view, name='generate_comisaria_cuarta_pdf_view'),
    path('cuarta/reporte/download/', generate_comisaria_cuarta_pdf_download, name='generate_comisaria_cuarta_pdf_download'),

    path('quinta/', ComisariaQuintaListView.as_view(), name='comisaria_quinta_list'),
    path('quinta/nuevo/', ComisariaQuintaCreateView.as_view(), name='comisaria_quinta_create'),
    path('quinta/reporte/', generate_comisaria_quinta_pdf_view, name='generate_comisaria_quinta_pdf_view'),
    path('quinta/reporte/download/', generate_comisaria_quinta_pdf_download, name='generate_comisaria_quinta_pdf_download'),

    path('completas/', ComisariasCompletaListView.as_view(), name='comisarias_completa_list'),
]
