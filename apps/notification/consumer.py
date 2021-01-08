# websocket

from asgiref.sync import async_to_sync

from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
import json
from userinfo.models import UserInfo
import random

from channels.layers import get_channel_layer
channel_layer = get_channel_layer()


class NotifConsumer(WebsocketConsumer):

    def connect(self):
        ch_group_list = channel_layer.groups.copy()
        print(ch_group_list)
        id = self.scope['url_route']['kwargs']['id']
        print('====connect ws==== '+id)
        if not id:
            self.close()
        for x, y in ch_group_list.items():
            if self.channel_name in y.keys():
                async_to_sync(self.channel_layer.group_discard)(
                    x, self.channel_name)
        async_to_sync(self.channel_layer.group_add)(
            id, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        ch_group_list = channel_layer.groups.copy()
        for x, y in ch_group_list.items():
            if self.channel_name in y.keys():
                async_to_sync(self.channel_layer.group_discard)(
                    x, self.channel_name)
        print('====disconnect ws====')

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        async_to_sync(self.channel_layer.send)(
            self.channel_name,
            {"type": 'send_message_to_frontend', 'message': message}
        )

    def send_message(self, to, message):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            to,
            {"type": 'send_message_to_frontend', 'message': message}
        )

    def send_message_to_frontend(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))
