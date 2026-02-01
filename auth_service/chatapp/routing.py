from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    # Matches: ws://chat-app-be-b7cs.onrender.com/ws/chat/general/
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]




