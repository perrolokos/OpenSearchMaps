import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import api.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'opensearchmaps.settings')

django_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_app,
        "websocket": AuthMiddlewareStack(
            URLRouter(api.routing.websocket_urlpatterns)
        ),
    }
)
