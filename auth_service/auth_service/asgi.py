import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chatapp.middleware import JWTAuthMiddleware
import chatapp.routing  # your chat app routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auth_service.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(
        URLRouter(
            chatapp.routing.websocket_urlpatterns
        )
    ),
})
