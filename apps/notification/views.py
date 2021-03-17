from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_mongoengine.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound
from rest_framework import status
from .models import Notification
from userinfo.models import UserInfo
from rest_framework import status
from django.core.exceptions import SuspiciousOperation
from .customResponse import CustomResponse
from .serializer import NotificationSerializer, NotificationCreateSerializer
from .consumer import NotifConsumer
import json
from datetime import datetime
# Create your views here.


class NotificationView(APIView):

    def get_object(self, user):
        try:
            return Notification.objects(to=user).order_by('-created_at').limit(5)
        except Notification.DoesNotExist:
            raise Http404('Notif Not Found')

    def get(self, request, user):
        try:
            userId = user
            if not userId:
                raise SuspiciousOperation('Need Param User')
            user = UserInfo.objects.get(id=userId)
            if not user:
                raise NotFound('User Not Found')
            data = self.get_object(user.id)
            serializer = NotificationSerializer(data, many=True)
            return CustomResponse.ok(values=serializer.data)
        except NotFound as e:
            return CustomResponse().base(message=str(e), status=status.HTTP_404_NOT_FOUND)
        except SuspiciousOperation as e:
            return CustomResponse.badRequest(message=str(e))
        except Exception as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            id = request.data.get('id')
            # serializer = NotificationCreateSerializer(data=request.data)
            # if serializer.is_valid():
            #     serializer.save()
            #     return CustomResponse().base(values=serializer.data, status=status.HTTP_201_CREATED)
            # return CustomResponse.badRequest(serializer.errors)
            notif = NotifConsumer()
            notif.send_message(to=id, message='hai')
        except NotFound as e:
            return CustomResponse().base(message=str(e), status=status.HTTP_404_NOT_FOUND)
        except SuspiciousOperation as e:
            return CustomResponse.badRequest(message=str(e))
        except Exception as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        try:
            id = request.data.get('id')
            try:
                notif = Notification.objects.get(id=id)
            except Notification.DoesNotExist:
                raise Http404('Notif Not Found')

            notif.status = 'open'
            notif.updated_at = datetime.now
            notif.save()
            return CustomResponse().ok(message="Notif Success")
        except NotFound as e:
            return CustomResponse().base(message=str(e), status=status.HTTP_404_NOT_FOUND)
        except SuspiciousOperation as e:
            return CustomResponse.badRequest(message=str(e))
        except Exception as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
