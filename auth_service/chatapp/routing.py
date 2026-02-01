from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    # Matches: ws://127.0.0.1:8000/ws/chat/general/
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]





