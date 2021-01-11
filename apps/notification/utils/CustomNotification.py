from notification.models import Notification
from notification.serializer import NotificationCreateSerializer
from rest_framework.exceptions import ValidationError
from notification.consumer import NotifConsumer

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class CustomNotification():

    def create(self, from_, to, type, title, message, push_message):
        data = {
            "from_": from_,
            "to": to,
            "type": type,
            "title": title,
            "message": message
        }
        serializer = NotificationCreateSerializer(data=data)

        def send_message_to_frontend(self, event):
            message = event['message']
            self.send(text_data=json.dumps({
                'message': message
            }))

        if serializer.is_valid():
            serializer.save()

            channel_layer = get_channel_layer()
            for x in to:
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    str(x),
                    {"type": 'send_message_to_frontend', 'message': message}
                )

   
            return serializer.data

        raise ValidationError(serializer.errors)
