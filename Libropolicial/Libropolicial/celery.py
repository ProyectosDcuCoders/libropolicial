from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Configura el entorno de Django para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Libropolicial.settings')

app = Celery('Libropolicial')

# Usa un string aquí para que los trabajadores no tengan que serializar el objeto de configuración
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubre automáticamente las tareas en todos los apps de Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
