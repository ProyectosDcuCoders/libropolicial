from django.apps import AppConfig

# Define la configuración para la aplicación 'comisarias'
class ComisariasConfig(AppConfig):
    # Establece el tipo de campo automático predeterminado para los modelos en esta aplicación
    default_auto_field = 'django.db.models.BigAutoField'
    # Define el nombre de la aplicación
    name = 'comisarias'
