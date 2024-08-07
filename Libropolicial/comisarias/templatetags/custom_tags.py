import datetime
from django import template

# Registra el filtro personalizado para que pueda ser utilizado en las plantillas
register = template.Library()

# Define un filtro de plantilla personalizado llamado 'is_today'
@register.filter
def is_today(value):
    if not value:
        return False
    # Obtiene la fecha y hora actual
    now = datetime.datetime.now()
    # Compara la fecha del valor proporcionado con la fecha actual
    return value.date() == now.date()
