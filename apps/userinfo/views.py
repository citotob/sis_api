
from django.shortcuts import render
from django.http import JsonResponse
from userinfo.models import UserInfo, UserRole, UserToken, DocumentUser, vendor, Message, ImageUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
#from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
import json
from django.core.files.storage import default_storage

import datetime
from django.core.files.storage import FileSystemStorage
import os
from datetime import timedelta
from urllib.parse import parse_qs
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
import secrets
from django.conf import settings
from .response import Response
from bson import ObjectId
from django.http import HttpResponse
import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from userinfo.utils.notification import Notification
#from userinfo.serializer import *
from django.core import serializers

import string
import random

from vendorperformance.models import VPScore

from publicservice.utils import send_mail

import requests

from notification.utils.CustomNotification import CustomNotification
from vendorperformance.models import VPScore


def test(request):
    try:
        Notification(
            users=['dXhXyAtRRkOB6nZTJyz2LC:APA91bGdcdTj6HrpaIX7GzAV_6CmBWRMrj8eo3TDUfpcffhxRiVbxaeS-F7qbPtZXTaI7NFpa3voy5DX40sC8xuq9XEyAu_YAckvwgKqZylWrEgnAcQEMRJG138zXLFS6ciIGyd2YLiD'],
            title='AAAAAAAAAA',
            message='BBBBBBBB',
            payload={"nilai": "00033333", "das": "laoalsososlos"},
            image='https://pm1.narvii.com/6117/551d7c8a7e56e4662896351e2645d298cb404040_hq.jpg'
        ).send_message()
    except Exception as e:
        print(e)
    return HttpResponse('asdas')


def login(request):
    if request.method == 'POST':
        try:
            req = request.body.decode("utf-8")
            data = json.loads(req)
            """
            secret_key = settings.RECAPTCHA_SECRET_KEY

            # captcha verification
            d = {
                'response': data.get('g-recaptcha-response'),
                'secret': secret_key
            }
            resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=d)
            result_json = resp.json()

            #print(result_json)

            if not result_json.get('success'):
                return Response.badRequest(
                    values=[],
                    message='recaptcha salah'
                )
            # end captcha verification
            """
            token = data.get('token', 'none')
            # print(data)
            try:
                user = UserInfo.objects.get(
                    username=data["username"], status="Aktif")
            except UserInfo.DoesNotExist:
                user = None
            if not user:
                # return Response.badRequest(
                #    values='null',
                #    message='User not found'
                # )
                return Response().base(
                    success=False,
                    message='User not found',
                    status=404
                )
            check = check_password(data['password'], user.password)
            if check:
                if token != 'none':
                    try:
                        user_token = UserToken.objects.get(key=token)
                        user_token.user = ObjectId(user.id)
                        user_token.updated = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
                        user_token.save()
                    except UserToken.DoesNotExist:
                        try:
                            user_token = UserToken.objects.get(
                                user=ObjectId(user.id))
                            user_token.key = token
                            user_token.updated = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
                            user_token.save()
                        except UserToken.DoesNotExist:
                            user_token = UserToken(
                                key=token,
                                user=ObjectId(user.id),
                                created=datetime.datetime.utcnow() + datetime.timedelta(hours=7),
                                updated=datetime.datetime.utcnow() + datetime.timedelta(hours=7)
                            )
                            user_token.save()

                return Response.ok(
                    values=user.serialize(),
                    message='Login Success'
                )
            else:
                return Response.badRequest(
                    values='null',
                    message='Wrong Password'
                )
        except Exception as e:
            # print(e)
            return HttpResponse(e)
    else:
        return HttpResponse('Post Only')


def getUserByRole(request):

    param = request.GET.get('role', None)

    switcher = {
        'admin': 'Admin',
        'staff': 'Staff Admin',
        'admins': 'Admin Surveyor',
        'staffs': 'Staff Surveyor'
    }

    role = switcher.get(param, None)

    if not role:
        return Response.badRequest(
            message='Wrong Param',
        )
    try:
        dataRole = UserRole.objects.get(name=role)
    except UserRole.DoesNotExist:
        # return Response.badRequest(
        #    message='Role not Found',
        # )
        return Response().base(
            success=False,
            message='Role not Found',
            status=404
        )

    try:
        data = UserInfo.objects.filter(role=dataRole.id)
    except UserInfo.DoesNotExist:
        # return Response.badRequest(
        #    message='User not Found',
        # )
        return Response().base(
            success=False,
            message='User not Found',
            status=404
        )

    result = []

    for x in data:
        result.append(x.serialize())

    return Response.ok(
        values=result,
        message=f'{len(result)} Data',
    )


def getUser(request):
    param = None
    page = -1
    try:
        body_data = json.loads(request.body)

        param = body_data.get('status', None)
        page = int(body_data.get('page', 0)) - 1
    except:
        pass
    skip = []
    if page >= 0:
        skip = [{'$skip': 20 * page},
                {'$limit': 20}]

    switcher = {
        "Belum Terverifikasi": "Belum Terverifikasi",
        "Aktif": "Aktif",
        "Ditolak": "Ditolak",
    }
    status = switcher.get(param, None)

    pipeline = [
        {
            '$lookup': {
                'from': 'document_user',
                'localField': 'doc',
                'foreignField': '_id',
                'as': 'doc'
            }
        }, {
            '$unwind': {
                'path': '$doc',
                'preserveNullAndEmptyArrays': True
            }
        }, {
            '$lookup': {
                'from': 'vendor',
                'localField': 'company',
                'foreignField': '_id',
                'as': 'company'
            }
        }, {
            '$unwind': {
                'path': '$company',
                'preserveNullAndEmptyArrays': True
            }
        }, {
            '$lookup': {
                'from': 'jenis_survey',
                'localField': 'company.jenissurvey',
                'foreignField': '_id',
                'as': 'company.jenissurvey'
            }
        }, {
            '$unwind': {
                'path': '$company.jenissurvey',
                'preserveNullAndEmptyArrays': True
            }
        }, {
            '$lookup': {
                'from': 'userrole',
                'localField': 'role',
                'foreignField': '_id',
                'as': 'role'
            }
        }, {
            '$unwind': {
                'path': '$role',
                'preserveNullAndEmptyArrays': True
            }
        },
        {
            '$sort': {
                'create_date': -1
            }
        }
    ]

    result = []
    if status:
        pp = [{
            '$match': {
                'status': status
            }
        }]
        pipe = pp + pipeline + skip
        agg_cursor = UserInfo.objects.aggregate(*pipe)

        result = list(agg_cursor)

        return Response.ok(
            values=json.loads(json.dumps(result, default=str)),
            message=f'{len(result)} Data'
        )
    else:
        pipe = pipeline + skip
        agg_cursor = UserInfo.objects.aggregate(*pipe)

        result = list(agg_cursor)

        return Response.ok(
            values=json.loads(json.dumps(result, default=str)),
            message=f'{len(result)} Data'
        )
    # except Exception as e:
    #     print(e)
    #     return HttpResponse(e)


def verifyUser(request):
    if request.method == 'POST':
        dateNow = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
        try:
            req = request.body.decode("utf-8")
            data = json.loads(req)
            userfrom = data.get("userfrom", None)
            try:
                user = UserInfo.objects.get(id=data["id"])
            except UserInfo.DoesNotExist:
                # return Response.ok(
                #    values=[],
                #    message='User not found'
                # )
                return Response().base(
                    success=False,
                    message='User not Found',
                    status=404
                )
            user.status = 'Aktif'
            user.update_date = dateNow
            user.save()
            print(user.id)
            subject = 'Verifikasi Akun Berhasil'
            text_content = 'Terimakasih telah mendaftar\n'+user.username+'\n' + \
                'Tim kami akan melakukan verifikasi terhadap data anda terlebih dahulu. Setelah verifikasi berhasil,\n' + \
                'anda akan menerima email konfirmasi untuk menginformasikan status pendaftaran akun anda.'
            template = 'email/webverifpengguna.html'
            d = {'username': user.username,
                 'media_url': settings.URL_MEDIA,
                 'url_login': settings.URL_LOGIN}
            email_sender = settings.EMAIL_ADMIN
            email_receipient = user.email
            send_mail(subject, text_content, template, d,
                      email_sender, [email_receipient])

            if not userfrom:
                userfrom = '6039e79e87394f7b466d9df9'

            notif = CustomNotification()
            notif.create(to=[user.id], from_=ObjectId(userfrom), type='user verified',
                         title='Verifikasi email berhasil', message='Verifikasi email berhasil', push_message='Ada pesan baru')

            return Response.ok(
                values=user.serialize(),
                message='Verify Success'
            )
        except Exception as e:
            print(e)
            # return HttpResponse(e)
            return Response.badRequest(
                values='null',
                message=str(e)
            )
    else:
        return HttpResponse('Post Only')


def declineUser(request):
    if request.method == 'POST':
        dateNow = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
        try:
            req = request.body.decode("utf-8")
            data = json.loads(req)
            userfrom = data.get("userfrom", None)

            try:
                user = UserInfo.objects.get(id=data["id"])
            except UserInfo.DoesNotExist:
                # return Response.ok(
                #    values=[],
                #    message='User not found'
                # )
                return Response().base(
                    success=False,
                    message='User not Found',
                    status=404
                )
            user.status = 'Ditolak'
            user.comment = data["comment"]
            user.update_date = dateNow
            user.save()
            """
            try:
                subject = 'Verifikasi Akun SMASLAB Gagal'
                text_content = 'Akun anda belum berhasil diverifikasi\n'+user.username+'\n'+user.company.name+'\n'+\
                    user.comment+'\n'\
                    'Silahkan untuk dapat melakukan registrasi kembali pada halaman \n'\
                    +settings.URL_LOGIN
                htmly     = get_template('email/decline-akun.html')
                d = {'username': user.username, 
                            'company': user.company.name,
                        'message_top': 'Akun anda belum berhasil diverifikasi',
                        'message_bottom': 'Silahkan untuk dapat melakukan registrasi kembali pada halaman '+settings.URL_REGISTER,
                        'comment': user.comment,
                        'media_url': settings.URL_MEDIA}
                html_content = htmly.render(d)
                sender = settings.EMAIL_ADMIN
                receipient = user.email
                msg = EmailMultiAlternatives(
                    subject, text_content, sender, [receipient])
                msg.attach_alternative(html_content, "text/html")
                respone = msg.send()
            except:
                pass
            """
            return Response.ok(
                values=user.serialize(),
                message='Decline Success'
            )
        except Exception as e:
            print(e)
            # return HttpResponse(e)
            return Response.badRequest(
                values='null',
                message=str(e)
            )
    else:
        return HttpResponse('Post Only')


def removeuser(request):
    if request.method == 'POST':
        try:
            req = request.body.decode("utf-8")
            data = json.loads(req)
            userfrom = data.get("userfrom", None)
            try:
                user = UserInfo.objects.get(id=data["id"])
            except UserInfo.DoesNotExist:
                # return Response.ok(
                #    values=[],
                #    message='User not found'
                # )
                return Response().base(
                    success=False,
                    message='User not Found',
                    status=404
                )
            user.delete()

            return Response.ok(
                values=user.serialize(),
                message='Remove user Success'
            )
        except Exception as e:
            print(e)
            return HttpResponse(e)
    else:
        return HttpResponse('Post Only')


def register(request):
    if request.method == 'POST':
        file = request.FILES['doc']
        if not file:
            return Response.badRequest(message='No File Upload')
        try:
            fs = FileSystemStorage(
                location=f'{settings.MEDIA_ROOT}/user/documents/',
                base_url=f'{settings.MEDIA_URL}/user/documents/'
            )

            try:
                data_vendor = vendor.objects.get(
                    name__iexact=request.POST.get('company'))
            except vendor.DoesNotExist:
                data_vendor = vendor(
                    name=request.POST.get('company'),
                    latitude='0',
                    longitude='0',
                    longlat=[0, 0],
                    created_at=datetime.datetime.utcnow() + datetime.timedelta(hours=7),
                    updated_at=datetime.datetime.utcnow() + datetime.timedelta(hours=7)
                )
                data_vendor.save()

                score = VPScore(
                    user=ObjectId('6039e79e87394f7b466d9df9'),
                    kecepatan=0,
                    kualitas=0,
                    ketepatan=0,
                    vendor=data_vendor.id,
                    doc=''
                )

                score.save()

                try:
                    data_role = UserRole.objects.get(
                        id=ObjectId(request.POST.get('role')))
                except UserRole.DoesNotExist:
                    # return Response.ok(
                    #    values=[],
                    #    message='Role tidak ada'
                    # )
                    return Response().base(
                        success=False,
                        message='Role tidak ada',
                        status=404
                    )
                #data_VPScore = VPScore(vendor=data_vendor.id)
                # data_VPScore.save()

            user = UserInfo(
                name=request.POST.get('name'),
                username=request.POST.get('username').lower(),
                password=make_password(
                    request.POST.get('password'), settings.SECRET_KEY, 'pbkdf2_sha256'),
                email=request.POST.get('email').lower(),
                phone=request.POST.get('phone'),
                company=ObjectId(data_vendor.id),
                role=ObjectId(request.POST.get('role')),
                create_date=datetime.datetime.utcnow() + datetime.timedelta(hours=7),
                update_date=datetime.datetime.utcnow() + datetime.timedelta(hours=7)
                # surveyor=request.POST.get('surveyor'),
            )
            user.save()
            filename = fs.save(file.name, file)
            file_path = fs.url(filename)
            doc = DocumentUser(
                name=file.name,
                path=file_path,
                create_date=datetime.datetime.utcnow() + datetime.timedelta(hours=7),
                update_date=datetime.datetime.utcnow() + datetime.timedelta(hours=7)
            )
            doc.save()

            user.doc = ObjectId(doc.id)
            user.save()

            try:
                file_image = request.FILES['image']

                fs = FileSystemStorage(
                    location=f'{settings.MEDIA_ROOT}/user/image/',
                    base_url=f'{settings.MEDIA_URL}/user/image/'
                )

                filename = fs.save(file_image.name, file_image)
                file_path = fs.url(filename)
                doc_image = ImageUser(
                    name=file_image.name,
                    path=file_path,
                    create_date=datetime.datetime.utcnow() + datetime.timedelta(hours=7),
                    update_date=datetime.datetime.utcnow() + datetime.timedelta(hours=7)
                )
                doc_image.save()
            except:
                doc_image = ImageUser(
                    name='user.jpg',
                    path='/media/user/image/user.jpg',
                    create_date=datetime.datetime.utcnow() + datetime.timedelta(hours=7),
                    update_date=datetime.datetime.utcnow() + datetime.timedelta(hours=7)
                )
                doc_image.save()
            user.image = ObjectId(doc_image.id)
            user.save()

            result = UserInfo.objects.get(id=user.id).serialize()
            """
            usersadmin = UserInfo.objects.filter(role__in=['5f13b1fa478ef95f4f0a83a7','5f13b353386bf295b4169efe'])
            #usersadmin = list(usersadmin['id'])
            userto_ = []
            for usr in usersadmin:
                userto_.append(usr.username)

            #usersadmin = UserInfo.objects.filter(role__in=['5f13b1fa478ef95f4f0a83a7','5f13b353386bf295b4169efe']).first()
            #userfrom = usersadmin.id
            notif = Message(
                title='Registrasi Akun SMASLAB',
                message='1 Permintaan verifikasi baru dari '+user.name,
                userfrom=user.username,
                userto=userto_,
                redirect='/admin',
                status='new',
                created=datetime.datetime.utcnow() + datetime.timedelta(hours=7),
                updated=datetime.datetime.utcnow() + datetime.timedelta(hours=7)
            )
            notif.save()
            """
            try:
                subject = 'Registrasi Akun'
                text_content = 'Terimakasih telah mendaftar\n'+user.username+'\n'+request.POST.get('company').upper()+'\n' + \
                    'Tim kami akan melakukan verifikasi terhadap data anda terlebih dahulu. Setelah verifikasi berhasil,\n' + \
                    'anda akan menerima email konfirmasi untuk menginformasikan status pendaftaran akun anda.'
                template = 'email/webpendaftaranberhasil.html'
                d = {'username': user.username,
                     'company': request.POST.get('company').upper(),
                     'media_url': settings.URL_MEDIA,
                     'url_login': settings.URL_LOGIN}
                email_sender = settings.EMAIL_ADMIN
                email_receipient = user.email
                send_mail(subject, text_content, template, d,
                          email_sender, [email_receipient])
            except:
                return Response().base(
                    success=False,
                    message='Format email salah',
                    status=400
                )
            req_fields = ['id']
            admin_users = UserInfo.objects.filter(
                role='5f73fdfc28751d590d835266', status='Aktif').only(*req_fields)
            if admin_users:
                list_admin_users = []
                for usr in admin_users:
                    list_admin_users.append(usr.id)
                notif = CustomNotification()
                notif.create(to=list_admin_users, from_=user.id, type='new user',
                             title='Pendaftaran berhasil', message='berhasil mendaftar', push_message='Ada pesan baru')

            return Response.ok(
                values=result,
                message='User Created'
            )
        except Exception as e:
            if "'code': 11000" in str(e):
                if "username" in str(e):
                    return Response.badRequest(message="username sudah ada")
                else:
                    return Response.badRequest(message="email sudah ada")
            else:
                return Response.badRequest(message=str(e))


def createRole(request):
    if request.method == 'POST':
        try:
            x = request.body.decode('utf-8')
            data = json.loads(x)
            try:
                data_role = UserRole.objects.get(name__iexact=data['name'])
                # return Response.ok(
                #    values=[],
                #    message='Data sudah ada'
                # )
                return Response().base(
                    success=False,
                    message='Data sudah ada',
                    status=409
                )
            except UserRole.DoesNotExist:
                pass
            role = UserRole(
                name=data['name'],
                create_date=datetime.datetime.utcnow() + datetime.timedelta(hours=7),
                update_date=datetime.datetime.utcnow() + datetime.timedelta(hours=7)
            )
            role.save()
            result = role.serialize()
            return Response.ok(
                values=result,
                message='Role Created Successfully'
            )
        except Exception as e:
            # Response.badRequest(message=str(e))
            return Response.badRequest(
                values=[],
                message=str(e)
            )
    else:
        return Response.badRequest(message='Only Post Request Accepted')


def getRole(request):
    roles = UserRole.objects.all()
    result = []
    for role in roles:
        result.append(role.serialize())
    if len(result) != 0:
        return Response.ok(
            values=result,
            message=f'{len(result)} Data Found'
        )
    else:
        # return Response.ok(
        #    values=result,
        #    message='No Data',
        # )
        return Response().base(
            success=False,
            message='No Data',
            status=404
        )
    return HttpResponse('Success')


def getstaffsurvey(request):
    result = []
    param = request.GET.get('adminsurvey', None)

    if param:
        try:
            data = UserInfo.objects.filter(company=param)
            for user in data:
                result.append(user.serialize())
            return Response.ok(
                values=result,
                message=f'{len(result)} Data'
            )

        except Exception as e:
            Response.badRequest(message=e)

    else:
        return Response.badRequest(
            message='no param detected'
        )


def getStaffSurvey(request):

    role = request.GET.get('role', None)
    company = request.GET.get('company', None)

    switcher = {
        'admin': 'Admin',
        'staff': 'Staff Admin',
        'admins': 'Admin Surveyor',
        'staffs': 'Staff Surveyor'
    }

    role = switcher.get(role, None)

    if not role:
        return Response.badRequest(
            message='Wrong Param',
        )

    try:
        datarole = UserRole.objects.get(name=role)
    except UserRole.DoesNotExist:
        # return Response.badRequest(
        #    message='UserRole not Found',
        # )
        return Response().base(
            success=False,
            message='UserRole not Found',
            status=404
        )
    try:
        datauser = UserInfo.objects.filter(role=ObjectId(
            datarole.id), company=ObjectId(company))
    except UserInfo.DoesNotExist:
        # return Response.badRequest(
        #    message='User not Found',
        # )
        return Response().base(
            success=False,
            message='User not Found',
            status=404
        )

    result = []
    for xx in datauser:
        result.append(xx.serialize())

    return Response.ok(
        values=result,
        message=f'{len(result)} Data',
    )


def changepassword(request):
    if request.method == 'POST':
        try:
            req = request.body.decode("utf-8")
            data = json.loads(req)
            if data['password'] == data['newpassword']:
                return Response.badRequest(
                    values=[],
                    message='Password baru tidak boleh sama'
                )
            try:
                user = UserInfo.objects.get(id=data["id"])
            except UserInfo.DoesNotExist:
                user = None
            if not user:
                # return Response.badRequest(
                #    values='null',
                #    message='User not found'
                # )
                return Response().base(
                    success=False,
                    message='User not Found',
                    status=404
                )
            check = check_password(data['password'], user.password)
            if check:
                user.password = make_password(
                    data['newpassword'], settings.SECRET_KEY, 'pbkdf2_sha256')
                user.update_date = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
                user.save()
                return Response.ok(
                    values=user.serialize(),
                    message='Change Password Success'
                )
            else:
                return Response.badRequest(
                    values='null',
                    message='Wrong Password'
                )
        except Exception as e:
            # print(e)
            return HttpResponse(e)
    else:
        return HttpResponse('Post Only')


def sendmail(request):
    '''send email via mailgun'''
    if request.method == 'POST':
        data = request.POST.dict()

        subject = data["subject"]
        text_content = data["content"]
        sender = "SMASLAB Admin<dev@dev.datasintesa.id>"
        receipient = data["receipient"]
        msg = EmailMultiAlternatives(
            subject, text_content, sender, [receipient])
        respone = msg.send()

        return Response.ok(
            message='Email sukses dikirim'
        )
    else:
        return HttpResponse('Post Only')


def sendnotif(request):
    if request.method == 'POST':
        dateNow = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
        try:
            req = request.body.decode("utf-8")
            data = json.loads(req)
            userfrom = data.get("userfrom", None)
            userto = data.get("userto", None)
            title = data.get("title", None)
            message = data.get("message", None)

            try:
                token = UserToken.objects.get(user=ObjectId(userto))
                Notification(
                    users=[token.key],
                    # users=['ef0D86AAQRG8Tu9ZXdEv2D:APA91bFmQDKHVjaTlRpUuHXEbXOVjywVyJuEoSrzjKLPqIrON4fviP9uJapeyZGQGFJ3WBODB_7xzFSeuNLpDZC0E_TMBH6jo8oJ5_QCF_qHCjBwxa7uQtacQGPgLgiI4DxoAKhJ1FcM'],
                    title=title,
                    message=message,
                ).send_message()
            except UserToken.DoesNotExist:
                # return Response.badRequest(
                #    values=[],
                #    message='User tidak ada'
                # )
                return Response().base(
                    success=False,
                    message='User tidak ada',
                    status=404
                )
            try:
                user = UserInfo.objects.get(id=userto)
            except UserInfo.DoesNotExist:
                # return Response.badRequest(
                #    values=[],
                #    message='User tujuan tidak ada'
                # )
                return Response().base(
                    success=False,
                    message='User tujuan tidak ada',
                    status=404
                )
            notif = Message(
                title=title,
                message=message,
                userfrom=userfrom,
                userto=[user.username],
                redirect='/',
                status='new'
            )
            notif.save()

            try:
                subject = title
                text_content = message
                sender = "SMASLAB Admin<dev@dev.datasintesa.id>"
                receipient = user.email
                msg = EmailMultiAlternatives(
                    subject, text_content, sender, [receipient])
                respone = msg.send()
            except:
                pass
            return Response.ok(
                values=user.serialize(),
                message='Send notif berhasil'
            )
        except Exception as e:
            print(e)
            return HttpResponse(e)
    else:
        return HttpResponse('Post Only')


def authenticate_credentials(key):
    # from rest_framework.authtoken.models import Token
    model = UserToken()
    # try:
    #    token = model.objects.select_related('user').get(key=key)
    # except model.DoesNotExist:
    #    raise exceptions.AuthenticationFailed(_('Invalid token.'))
    #    return False,None
    userinfo = UserToken.objects.filter(key=key)
    if len(userinfo) == 0:
        return False, None

    # if not token.user.is_active:
    #    raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))
    #    return False,None
    # userinfo = UserInfo.objects.get(id = token.user_id)
    return True, userinfo


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        password = instance.password
        if instance.username != "admin":
            instance.set_password(password)  # Password encryption method
        instance.save()


def getnotif(request):
    try:
        param = json.loads(request.body.decode("utf-8"))
        username = param.get('user', None)
        if username == None:
            return Response.badRequest(
                values=[],
                message='User tidak bisa kosong'
            )
        notifs = Message.objects.filter(
            userto=username).order_by('-updated')[:5]
        json_list = []
        for nf in notifs:
            json_dict = {}
            json_dict["id"] = str(nf.id)
            json_dict["title"] = nf.title
            json_dict["message"] = nf.message
            json_dict["tanggal"] = nf.updated
            json_list.append(json_dict)
        return Response.ok(
            values=json_list,
            message=f'{len(json_list)} Data'
        )
    except Exception as e:
        print(e)
        return HttpResponse(e)


def updatesurveyor(request):
    try:
        datauser = UserInfo.objects.filter(
            role=ObjectId('5f13b370386bf295b4169f00'))
    except UserInfo.DoesNotExist:
        # return Response.badRequest(
        #    message='User not Found',
        # )
        return Response().base(
            success=False,
            message='User not Found',
            status=404
        )
    for dt in datauser:
        dt.name = dt.username
        dt.save()

    return Response.ok(
        values=[],
        message=f'Update Data',
    )


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def forgotpassword(request):
    if request.method == 'POST':
        try:
            req = request.body.decode("utf-8")
            data = json.loads(req)
            try:
                user = UserInfo.objects.get(email=data["email"])
            except UserInfo.DoesNotExist:
                # return Response.ok(
                #    values=[],
                #    message='User not found'
                # )
                return Response().base(
                    success=False,
                    message='User not Found',
                    status=404
                )

            token = id_generator(10, str(user.id))

            user.token_reset = token
            dateNow = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
            user.expire_token = dateNow + datetime.timedelta(hours=1)
            user.update_date = dateNow
            user.save()
            subject = 'Forgot password'
            text_content = 'Atur Ulang Kata Sandi\Jika Anda tidak melakukan rekues reset Kata Sandi akun, silahkan abaikan email ini'
            #text_content = ''
            htmly = get_template('email/webforgotpassword.html')

            d = {'username': user.username,
                 'company': user.company.name,
                 'message_top': 'Atur Ulang Kata Sandi',
                 'message_bottom': 'Jika Anda tidak melakukan rekues reset Kata Sandi akun, silahkan abaikan email ini.\n'
                 + settings.URL_LOGIN, 'media_url': settings.URL_MEDIA,
                 'reset_url': settings.URL_RESETPASSWORD+'/'+user.token_reset}
            html_content = htmly.render(d)
            sender = settings.EMAIL_ADMIN
            receipient = user.email
            msg = EmailMultiAlternatives(
                subject, text_content, sender, [receipient])
            msg.attach_alternative(html_content, "text/html")

            respone = msg.send()
            return Response.ok(
                values=user.serialize(),
                message='Forgot Success'
            )
        except Exception as e:
            print(e)
            # return HttpResponse(e)
            return Response.badRequest(
                values='null',
                message=str(e)
            )
    else:
        return HttpResponse('Post Only')


def resetpassword(request):
    if request.method == 'POST':
        try:
            req = request.body.decode("utf-8")
            data = json.loads(req)
            try:
                user = UserInfo.objects.get(token_reset=data["token"])
            except UserInfo.DoesNotExist:
                # return Response.ok(
                #    values=[],
                #    message='User not found'
                # )
                return Response().base(
                    success=False,
                    message='User not Found',
                    status=404
                )

            user.password = make_password(
                data['newpassword'], settings.SECRET_KEY, 'pbkdf2_sha256')
            user.update_date = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
            user.token_reset = None
            user.expire_token = None
            user.save()

            subject = 'Reset password'
            text_content = 'Reset Password Telah Berhasil'
            #text_content = ''
            htmly = get_template('email/webresetpassword.html')

            d = {'username': user.username,
                 'company': user.company.name,
                 'message_top': 'Atur Ulang Kata Sandi',
                 'message_bottom': 'Reset Password Telah Berhasil',
                 'media_url': settings.URL_MEDIA,
                 'login_url': settings.URL_LOGIN}
            html_content = htmly.render(d)
            sender = settings.EMAIL_ADMIN
            receipient = user.email
            msg = EmailMultiAlternatives(
                subject, text_content, sender, [receipient])
            msg.attach_alternative(html_content, "text/html")

            respone = msg.send()

            return Response.ok(
                values=user.serialize(),
                message='Reset Success'
            )
        except Exception as e:
            print(e)
            # return HttpResponse(e)
            return Response.badRequest(
                values='null',
                message=str(e)
            )
    else:
        return HttpResponse('Post Only')


def changeimage(request):
    if request.method == 'POST':
        try:
            file = request.FILES['image']
            if not file:
                return Response.badRequest(message='No File Upload')
            fs = FileSystemStorage(
                location=f'{settings.MEDIA_ROOT}/user/image/',
                base_url=f'{settings.MEDIA_URL}/user/image/'
            )
            data = request.POST.dict()
            try:
                user = UserInfo.objects.get(id=data["userid"])
            except UserInfo.DoesNotExist:
                # return Response.ok(
                #    values=[],
                #    message='User not found'
                # )
                return Response().base(
                    success=False,
                    message='User not Found',
                    status=404
                )

            filename = fs.save(file.name, file)
            file_path = fs.url(filename)
            doc_image = ImageUser(
                name=file.name,
                path=file_path,
                create_date=datetime.datetime.utcnow() + datetime.timedelta(hours=7),
                update_date=datetime.datetime.utcnow() + datetime.timedelta(hours=7)
            )
            doc_image.save()

            user.image = ObjectId(doc_image.id)

            user.save()

            result = UserInfo.objects.get(id=user.id).serialize()
            """
            try:
                subject = 'Verifikasi Akun SMASLAB Berhasil'
                text_content = 'Akun anda telah berhasil diverifikasi\n'+user.username+'\n'+user.company.name+'\n'\
                        'Silahkan untuk dapat melakukan log in melalui aplikasi ataupun website SMASLAB.\nhttps://survejdev.datasintesa.id/login'
                #text_content = ''
                htmly     = get_template('email/verif-akun.html')
                
                d = {'username': user.username, 
                            'company': user.company.name,
                        'message_top': 'Akun anda telah berhasil diverifikasi',
                        'message_bottom': 'Silahkan untuk dapat melakukan log in melalui aplikasi ataupun website SMASLAB.\n'
                            +settings.URL_LOGIN, 'media_url': settings.URL_MEDIA}
                html_content = htmly.render(d)
                sender = settings.EMAIL_ADMIN
                receipient = user.email
                msg = EmailMultiAlternatives(
                    subject, text_content, sender, [receipient])
                msg.attach_alternative(html_content, "text/html")
                respone = msg.send()
            except:
                pass
            """
            return Response.ok(
                values=result,
                message='Success'
            )
        except Exception as e:
            print(e)
            # return HttpResponse(e)
            return Response.badRequest(
                values='null',
                message=str(e)
            )
    else:
        return HttpResponse('Post Only')
