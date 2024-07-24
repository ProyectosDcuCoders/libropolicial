# asgi.py

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
import divisioncomunicaciones.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Libropolicial.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        SessionMiddlewareStack(
            URLRouter(
                divisioncomunicaciones.routing.websocket_urlpatterns
            )
        )
    ),
})
