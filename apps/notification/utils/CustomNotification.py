from notification.models import Notification
from notification.serializer import NotificationCreateSerializer
from rest_framework.exceptions import ValidationError
from notification.consumer import NotifConsumer


class CustomNotification():

    def create(self, from_, to, type, title, message, push_message):
        data = {
            "from": from_,
            "to": to,
            "type": type,
            "title": title,
            "message": message
        }
        serializer = NotificationCreateSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            notif = NotifConsumer()
            for x in to:
                notif.send_message(x, push_message)
            return serializer.data

        raise ValidationError(serializer.errors)
