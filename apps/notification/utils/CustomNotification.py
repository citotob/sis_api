from notification.models import Notification
from notification.serializer import NotificationCreateSerializer
from rest_framework.exceptions import ValidationError


class CustomNotification():

    def create(self, from_, to, type, title, message):
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
            return serializer.data

        raise ValidationError(serializer.errors)
