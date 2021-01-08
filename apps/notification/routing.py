from django.urls import re_path, path
from .consumer import NotifConsumer

#websocket_urlpatterns = [
#    re_path("ws/(?P<id>\w+)", NotifConsumer.as_asgi()),
#]

websocket_urlpatterns = [
     path('ws/(?P<id>\w+)', NotifConsumer),
]