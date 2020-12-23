from django.urls import re_path, path
from .consumer import NotifConsumer

#websocket_urlpatterns = [
#    re_path('', NotifConsumer.as_asgi()),
#]

websocket_urlpatterns = [
    path('socket.io/', NotifConsumer),
]