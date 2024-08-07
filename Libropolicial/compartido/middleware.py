# Importa MiddlewareMixin para crear middlewares compatibles con versiones anteriores de Django
from django.utils.deprecation import MiddlewareMixin
# Importa redirect para redirigir a los usuarios a una URL específica
from django.shortcuts import redirect
# Importa timezone para trabajar con fechas y horas conscientes de la zona horaria
from django.utils import timezone
# Importa timedelta para trabajar con diferencias de tiempo
from datetime import timedelta

# Middleware que deshabilita la caché para todas las respuestas
class NoCacheMiddleware(MiddlewareMixin):
    # Método que procesa la respuesta para modificar las cabeceras HTTP relacionadas con la caché
    def process_response(self, request, response):
        # Establece las cabeceras HTTP para evitar el almacenamiento en caché
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        # Devuelve la respuesta modificada
        return response

# Middleware que redirige a los usuarios autenticados lejos de ciertas URLs restringidas
class RedirectAuthenticatedUserMiddleware(MiddlewareMixin):
    # Método que procesa la solicitud para comprobar si el usuario autenticado debe ser redirigido
    def process_request(self, request):
        # Define las URLs restringidas donde no deben estar los usuarios autenticados
        restricted_urls = ['/', '/login/', '/no-permission/']
        # Comprueba si el usuario está autenticado y si la solicitud es para una URL restringida
        if request.user.is_authenticated and request.path in restricted_urls:
            # Redirige al usuario a una vista específica según su grupo
            if request.user.groups.filter(name='comisariaprimera').exists():
                return redirect('comisaria_primera_list')
            elif request.user.groups.filter(name='comisariasegunda').exists():
                return redirect('comisaria_segunda_list')
            elif request.user.groups.filter(name='divisioncomunicaciones').exists():
                return redirect('divisioncomunicaciones_list')
            else:
                # Si el usuario no pertenece a ninguno de los grupos anteriores, redirige a 'no_permission'
                return redirect('no_permission')
        # Si no hay redirección, devuelve None para permitir que el proceso continúe
        return None

# Middleware que cierra la sesión de los usuarios después de un período de inactividad
class InactivityLogoutMiddleware(MiddlewareMixin):
    # Método que procesa la solicitud para comprobar la actividad del usuario
    def process_request(self, request):
        # Comprueba si el usuario está autenticado
        if request.user.is_authenticated:
            # Obtiene la última actividad del usuario desde la sesión
            last_activity = request.session.get('last_activity')
            if last_activity:
                # Convierte la última actividad en un objeto datetime
                last_activity = timezone.datetime.fromisoformat(last_activity)
                # Comprueba si el tiempo transcurrido desde la última actividad es mayor que una hora
                if timezone.now() - last_activity > timedelta(hours=1):
                    # Importa logout para cerrar la sesión del usuario
                    from django.contrib.auth import logout
                    # Cierra la sesión del usuario
                    logout(request)
                    # Redirige al usuario a la página de inicio de sesión
                    return redirect('login')
            # Actualiza la última actividad del usuario en la sesión con la hora actual
            request.session['last_activity'] = timezone.now().isoformat()
