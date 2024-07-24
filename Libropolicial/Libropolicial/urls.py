from django.contrib import admin
from django.urls import path, include
from comisarias.views import CustomLoginView, HomeView, no_permission
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('comisarias/', include('comisarias.urls')),
    path('comisarias/', include('comisariasriogrande.urls')),
    path('divisioncomunicaciones/', include('divisioncomunicaciones.urls')),
    path('', HomeView.as_view(), name='home'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('no-permission/', no_permission, name='no_permission'),
]
