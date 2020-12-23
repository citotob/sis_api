from django.urls import re_path
from .consumer import NotifConsumer

websocket_urlpatterns = [
    re_path(r'', NotifConsumer.as_asgi()),
]
