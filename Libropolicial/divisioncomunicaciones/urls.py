from django.urls import path
from .views import DivisionComunicacionesListView, DivisionComunicacionesCreateView, DivisionComunicacionesUpdateView

urlpatterns = [
    path('', DivisionComunicacionesListView.as_view(), name='divisioncomunicaciones_list'),
    path('nuevo/', DivisionComunicacionesCreateView.as_view(), name='divisioncomunicaciones_create'),
    path('<int:pk>/editar/', DivisionComunicacionesUpdateView.as_view(), name='divisioncomunicaciones_update'),
]

