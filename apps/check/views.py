from django.shortcuts import render
from rest_framework_mongoengine.viewsets import GenericAPIView, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser
#from .models import VPScore
import json
from .customResponse import CustomResponse
from django.http import JsonResponse
#from .serializer import VPSerializer, VPCreateSerializer
from apps.userinfo.models import vendor, UserInfo
#from apps.userinfo.serializer import VendorScoreSerializer
from django.conf import settings

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
#from django.template import Context

class checkAPI(ModelViewSet):
    def load(self, request, format=None):
        try:
            load_ = request.data.get('load', None)
            if not load_:
                raise TypeError('Load tidak boleh kosong')
            data_user = UserInfo.objects.filter(role='5f73fdfc28751d590d835266', status='verified')
            if not data_user:
                return CustomResponse().base(success=False, message='User Not Found', status=status.HTTP_404_NOT_FOUND)
            list_receipient=[]
            for dt in data_user:
                list_receipient.append(dt.email)
            #try:
            subject = 'Load Notification'
            text_content = 'Load Notification'
            #text_content = ''
            htmly     = get_template('email/check/webload.html')
            
            d = {'load': (load_/32)*100,
                    'message_top': '',
                    'message_bottom': '', 'media_url': settings.URL_MEDIA}
            html_content = htmly.render(d)
            sender = settings.EMAIL_ADMIN
            receipient = list_receipient
            msg = EmailMultiAlternatives(
                subject, text_content, sender, receipient)
            msg.attach_alternative(html_content, "text/html")
            respone = msg.send()
            #print('Send email success')
            #except:
            #    print('failed send email')
            #    pass
            return CustomResponse.ok(values=[])
        #except vendor.DoesNotExist:
        #    return CustomResponse().base(success=False, message='Id Not Found', status=status.HTTP_404_NOT_FOUND)
        except TypeError as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def network(self, request, format=None):
        try:
            status = request.data.get('status', None)
            if not status:
                raise TypeError('Status tidak boleh kosong')
            data_user = UserInfo.objects.filter(role='5f73fdfc28751d590d835266', status='verified')
            if not data_user:
                return CustomResponse().base(success=False, message='User Not Found', status=status.HTTP_404_NOT_FOUND)
            list_receipient=[]
            for dt in data_user:
                list_receipient.append(dt.email)
            try:
                subject = 'Network Notification'
                text_content = 'Network Notification'
                #text_content = ''
                htmly     = get_template('email/check/webnetworkdown.html')
                
                d = {'status': status,
                        'message_top': '',
                        'message_bottom': '', 'media_url': settings.URL_MEDIA}
                html_content = htmly.render(d)
                sender = settings.EMAIL_ADMIN
                receipient = list_receipient
                msg = EmailMultiAlternatives(
                    subject, text_content, sender, [receipient])
                msg.attach_alternative(html_content, "text/html")
                respone = msg.send()
                #print('Send email success')
            except:
            #    print('failed send email')
                pass
            return CustomResponse.ok(values=[])
        #except vendor.DoesNotExist:
        #    return CustomResponse().base(success=False, message='Id Not Found', status=status.HTTP_404_NOT_FOUND)
        except TypeError as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def database(self, request, format=None):
        try:
            status = request.data.get('status', None)
            if not status:
                raise TypeError('Status tidak boleh kosong')
            data_user = UserInfo.objects.filter(role='5f73fdfc28751d590d835266', status='verified')
            if not data_user:
                return CustomResponse().base(success=False, message='User Not Found', status=status.HTTP_404_NOT_FOUND)
            list_receipient=[]
            for dt in data_user:
                list_receipient.append(dt.email)
            try:
                subject = 'Database Notification'
                text_content = 'Database Notification'
                #text_content = ''
                htmly     = get_template('email/check/webdbdown.html')
                
                d = {'status': status,
                        'message_top': '',
                        'message_bottom': '', 'media_url': settings.URL_MEDIA}
                html_content = htmly.render(d)
                sender = settings.EMAIL_ADMIN
                receipient = list_receipient
                msg = EmailMultiAlternatives(
                    subject, text_content, sender, [receipient])
                msg.attach_alternative(html_content, "text/html")
                respone = msg.send()
                #print('Send email success')
            except:
            #    print('failed send email')
                pass
            return CustomResponse.ok(values=[])
        #except vendor.DoesNotExist:
        #    return CustomResponse().base(success=False, message='Id Not Found', status=status.HTTP_404_NOT_FOUND)
        except TypeError as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def bruteforce(self, request, format=None):
        try:
            attempt = request.data.get('attempt', None)
            if not attempt:
                raise TypeError('attempt tidak boleh kosong')
            threshold = request.data.get('threshold', None)
            if not threshold:
                raise TypeError('threshold tidak boleh kosong')
            data_user = UserInfo.objects.filter(role='5f73fdfc28751d590d835266', status='verified')
            if not data_user:
                return CustomResponse().base(success=False, message='User Not Found', status=status.HTTP_404_NOT_FOUND)
            list_receipient=[]
            for dt in data_user:
                list_receipient.append(dt.email)
            try:
                subject = 'Bruteforce Notification'
                text_content = 'Bruteforce Notification'
                #text_content = ''
                htmly     = get_template('email/check/webbruteforce.html')
                
                d = {'attempt': attempt, 'threshold': threshold,
                        'message_top': '',
                        'message_bottom': '', 'media_url': settings.URL_MEDIA}
                html_content = htmly.render(d)
                sender = settings.EMAIL_ADMIN
                receipient = list_receipient
                msg = EmailMultiAlternatives(
                    subject, text_content, sender, [receipient])
                msg.attach_alternative(html_content, "text/html")
                respone = msg.send()
                #print('Send email success')
            except:
            #    print('failed send email')
                pass
            return CustomResponse.ok(values=[])
        #except vendor.DoesNotExist:
        #    return CustomResponse().base(success=False, message='Id Not Found', status=status.HTTP_404_NOT_FOUND)
        except TypeError as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def disk(self, request, format=None):
        try:
            disk_ = request.data.get('disk', None)
            if not disk_:
                raise TypeError('disk tidak boleh kosong')
            
            data_user = UserInfo.objects.filter(role='5f73fdfc28751d590d835266', status='verified')
            if not data_user:
                return CustomResponse().base(success=False, message='User Not Found', status=status.HTTP_404_NOT_FOUND)
            list_receipient=[]
            for dt in data_user:
                list_receipient.append(dt.email)
            try:
                subject = 'Disk Storage Notification'
                text_content = 'Disk Storage Notification'
                #text_content = ''
                htmly     = get_template('email/check/webstoragelow.html')
                
                d = {'disk': disk_,
                        'message_top': '',
                        'message_bottom': '', 'media_url': settings.URL_MEDIA}
                html_content = htmly.render(d)
                sender = settings.EMAIL_ADMIN
                receipient = list_receipient
                msg = EmailMultiAlternatives(
                    subject, text_content, sender, [receipient])
                msg.attach_alternative(html_content, "text/html")
                respone = msg.send()
                #print('Send email success')
            except:
            #    print('failed send email')
                pass
            return CustomResponse.ok(values=[])
        #except vendor.DoesNotExist:
        #    return CustomResponse().base(success=False, message='Id Not Found', status=status.HTTP_404_NOT_FOUND)
        except TypeError as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)