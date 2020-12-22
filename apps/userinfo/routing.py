# chat/routing.py


#from django.conf.urls import url
from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [

    re_path(r'ws/$', consumers.ChatConsumer.as_asgi()),
    #re_path(r'ws/$', consumers.ChatConsumer),
]

#websocket_urlpatterns = [
#    path('ws/', consumers.ChatConsumer),
#    #url(r'^ws/', consumers.ChatConsumer),
#]