from pyfcm import FCMNotification
from django.conf import settings


class Notification:
    push_service = FCMNotification(api_key=settings.FCM_DJANGO_SETTINGS)

    def __init__(self, title="Title", message='Message', users=[], payload={}, image=''):
        self.title = title
        self.message = message
        self.users = users
        self.payload = payload
        self.image = image

    def send_message(self):
        if (len(self.users) == 0):
            raise ValueError('Minimum One User Needed')
        elif (len(self.users) == 1):
            return self.push_service.notify_single_device(
                registration_id=self.users[0],
                message_title=self.title,
                message_body=self.message,
                data_message=self.payload,
                extra_notification_kwargs={"image": self.image}
            )
        else:
            return self.push_service.notify_multiple_devices(
                registration_ids=self.users,
                message_title=self.title,
                message_body=self.message,
                data_message=self.payload,
                extra_notification_kwargs={"image": self.image}
            )
