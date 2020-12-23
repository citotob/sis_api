#websocket

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


from channels.generic.websocket import AsyncWebsocketConsumer
import json
from userinfo.models import UserInfo
import random

from channels.layers import get_channel_layer
channel_layer = get_channel_layer()
from asgiref.sync import async_to_sync

import json


class NotifConsumer(WebsocketConsumer):

    def connect(self):
        print('====connect ws====')
        async_to_sync(self.channel_layer.group_add)("sis", self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
