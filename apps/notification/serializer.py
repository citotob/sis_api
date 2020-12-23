from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework_mongoengine.serializers import serializers
from .models import Notification
from userinfo.models import UserInfo


class NotifUserSerializer(DocumentSerializer):
    class Meta:
        model = UserInfo
        fields = '__all__'
        # exclude = ('password', )
        depth = 1


class NotificationSerializer(DocumentSerializer):
    # from_ = NotifUserSerializer(many=True, read_only=True)
    # to = NotifUserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'
        depth = 1


class NotificationCreateSerializer(DocumentSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        depth = 0
