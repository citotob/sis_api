
from django.shortcuts import render
from django.http import JsonResponse
from userinfo.models import UserInfo, UserRole, UserToken, DocumentUser, Surveyor, JenisSurvey, Message
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token
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
            data = request.POST.dict()
            token = data.get('token', 'none')
            print(data)
            try:
                user = UserInfo.objects.get(
                    username=data["username"], status="verified")
            except UserInfo.DoesNotExist:
                user = None
            if not user:
                return Response.badRequest(
                    values='null',
                    message='User not found'
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
        return Response.badRequest(
            message='Role not Found',
        )

    try:
        data = UserInfo.objects.filter(role=dataRole.id)
    except UserInfo.DoesNotExist:
        return Response.badRequest(
            message='User not Found',
        )

    result = []

    for x in data:
        result.append(x.serialize())

    return Response.ok(
        values=result,
        message=f'{len(result)} Data',
    )


def getUser(request):
    # try:
    param = request.GET.get('status', None)
    page = int(request.GET.get('page', 0)) - 1
    skip = []
    if page >= 0:
        skip = [{'$skip': 20 * page},
                {'$limit': 20}]

    switcher = {
        "requested": "requested",
        "verified": "verified",
        "declined": "declined",
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
                'from': 'surveyor',
                'localField': 'organization',
                'foreignField': '_id',
                'as': 'organization'
            }
        }, {
            '$unwind': {
                'path': '$organization',
                'preserveNullAndEmptyArrays': True
            }
        }, {
            '$lookup': {
                'from': 'jenis_survey',
                'localField': 'organization.jenissurvey',
                'foreignField': '_id',
                'as': 'organization.jenissurvey'
            }
        }, {
            '$unwind': {
                'path': '$organization.jenissurvey',
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
            userfrom = data.get("userfrom",None)
            user = UserInfo.objects.get(id=data["id"])
            if not user:
                return Response.badRequest(
                    values='null',
                    message='User not found'
                )
            user.status = 'verified'
            user.update_date = dateNow
            user.save()
            """
            if not userfrom:
                usersadmin = UserInfo.objects.filter(role__in=['5f13b1fa478ef95f4f0a83a7','5f13b353386bf295b4169efe']).first()
                #userto_ = []
                #for usr in usersadmin:
                #    userto_.append(usr.username)
                userfrom = usersadmin.id
            notif = Message(
                title='Verifikasi Akun SMASLAB Berhasil',
                message='Akun anda telah berhasil di verifikasi\n'+user.username+'\n'+user.organization.name+'\n'
                    'Silahkan untuk dapat melakukan log in melalui aplikasi ataupun website SMASLAB.',
                userfrom=userfrom,
                userto=[user.username],
                redirect='/',
                status='new'
            )
            notif.save()
            """
            try:
                subject = 'Verifikasi Akun SMASLAB Berhasil'
                text_content = 'Akun anda telah berhasil diverifikasi\n'+user.username+'\n'+user.organization.name+'\n'\
                        'Silahkan untuk dapat melakukan log in melalui aplikasi ataupun website SMASLAB.\nhttps://survejdev.datasintesa.id/login'
                #text_content = ''
                htmly     = get_template('email/verif-akun.html')
                
                d = {'username': user.username, 
                            'organization': user.organization.name,
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
            #except Exception as e:
            #    print(e)
            #    return HttpResponse(e)
            """
            try:
                subject = 'Verifikasi Akun SMASLAB Berhasil'
                text_content = 'Akun anda telah berhasil di verifikasi\n'+user.username+'\n'+user.organization.name+'\n'\
                        'Silahkan untuk dapat melakukan log in melalui aplikasi ataupun website SMASLAB.'
                sender = "Admin dev@dev.datasintesa.id"
                receipient = user.email
                msg = EmailMultiAlternatives(
                    subject, text_content, sender, [receipient])
                respone = msg.send()
            except:
                pass
            """
            return Response.ok(
                values=user.serialize(),
                message='Verify Success'
            )
        except Exception as e:
            print(e)
            #return HttpResponse(e)
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
            userfrom = data.get("userfrom",None)
            user = UserInfo.objects.get(id=data["id"])
            if not user:
                return Response.badRequest(
                    values='null',
                    message='User not found'
                )
            user.status = 'declined'
            user.comment = data["comment"]
            user.update_date = dateNow
            user.save()
            """
            if not userfrom:
                usersadmin = UserInfo.objects.filter(role__in=['5f13b1fa478ef95f4f0a83a7','5f13b353386bf295b4169efe']).first()
                userfrom = usersadmin.id
            notif = Message(
                title='Verifikasi Akun SMASLAB Gagal',
                message='Akun anda belum berhasil diverifikasi\n'+user.username+'\n'+user.organization.name+'\n'+
                    user.comment+'\n'+
                    'Silahkan untuk dapat melakukan registrasi kembali pada halaman \n'+
                    'http://202.182.55.252:6400/register',
                userfrom=userfrom,
                userto=[user.username],
                redirect='/',
                status='new'
            )
            notif.save()
            """
            """
            try:
                subject = 'Verifikasi Akun SMASLAB Gagal'
                text_content = 'Akun anda belum berhasil di verifikasi\n'+user.username+'\n'+user.organization.name+'\n'+\
                    user.comment+'\n'\
                    'Silahkan untuk dapat melakukan registrasi kembali pada halaman \n'\
                    'http://202.182.55.252:6400/register'
                sender = "SMASLAB Admin<dev@dev.datasintesa.id>"
                receipient = user.email
                msg = EmailMultiAlternatives(
                    subject, text_content, sender, [receipient])
                respone = msg.send()
            except:
                pass
            """
            try:
                subject = 'Verifikasi Akun SMASLAB Gagal'
                text_content = 'Akun anda belum berhasil diverifikasi\n'+user.username+'\n'+user.organization.name+'\n'+\
                    user.comment+'\n'\
                    'Silahkan untuk dapat melakukan registrasi kembali pada halaman \n'\
                    +settings.URL_LOGIN
                htmly     = get_template('email/decline-akun.html')
                d = {'username': user.username, 
                            'organization': user.organization.name,
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
            #except Exception as e:
            #    print(e)
            #    return HttpResponse(e)
            return Response.ok(
                values=user.serialize(),
                message='Decline Success'
            )
        except Exception as e:
            print(e)
            #return HttpResponse(e)
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
            userfrom = data.get("userfrom",None)
            user = UserInfo.objects.get(id=data["id"])
            if not user:
                return Response.badRequest(
                    values='null',
                    message='User not found'
                )
            user.delete()
            """
            try:
                subject = 'Verifikasi Akun SMASLAB Gagal'
                text_content = 'Akun anda belum berhasil diverifikasi\n'+user.username+'\n'+user.organization.name+'\n'+\
                    user.comment+'\n'\
                    'Silahkan untuk dapat melakukan registrasi kembali pada halaman \n'\
                    'http://202.182.55.252:6400/register'
                htmly     = get_template('email/verif-akun.html')
                d = {'username': user.username, 
                            'organization': user.organization.name,
                        'message_top': 'Akun anda belum berhasil diverifikasi',
                        'message_bottom': 'Silahkan untuk dapat melakukan registrasi kembali pada halaman http://202.182.55.252:5400/register'}
                html_content = htmly.render(d)
                sender = "SMASLAB Admin<dev@dev.datasintesa.id>"
                receipient = user.email
                msg = EmailMultiAlternatives(
                    subject, text_content, sender, [receipient])
                msg.attach_alternative(html_content, "text/html")
                respone = msg.send()
            except:
                pass
            """
            #except Exception as e:
            #    print(e)
            #    return HttpResponse(e)
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
            print(fs.url('asd'))
            try:
                data_surveyor = Surveyor.objects.get(
                    name__iexact=request.POST.get('organization'))
            except Surveyor.DoesNotExist:
                try:
                    data_jenis = JenisSurvey.objects.get(
                        jenis=request.POST.get('jenis').upper())
                except JenisSurvey.DoesNotExist:
                    return Response.badRequest(
                        values='null',
                        message='jenissurvey not found'
                    )
                data_surveyor = Surveyor(
                    name=request.POST.get('organization').upper(),
                    jenissurvey=ObjectId(data_jenis.id),
                )
                data_surveyor.save()
            user = UserInfo(
                name=request.POST.get('name'),
                username=request.POST.get('username').lower(),
                password=make_password(
                    request.POST.get('password'), settings.SECRET_KEY, 'pbkdf2_sha256'),
                email=request.POST.get('email').lower(),
                phone=request.POST.get('phone'),
                organization=ObjectId(data_surveyor.id),
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

            result = UserInfo.objects.get(id=user.id).serialize()
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
            try:
                subject = 'Registrasi Akun SMASLAB'
                text_content = 'Terimakasih telah mendaftar\n'+user.username+'\n'+request.POST.get('organization').upper()+'\n'+ \
                    'Tim kami akan melakukan verifikasi terhadap data anda terlebih dahulu. Setelah verifikasi berhasil,\n'+ \
                    'anda akan menerima email konfirmasi untuk menginformasikan status pendaftaran akun anda.'
                htmly     = get_template('email/register.html')
                d = {'username': user.username, 
                            'organization': request.POST.get('organization').upper(),
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
            #except Exception as e:
            #    return Response.badRequest(message=str(e))
            
            return Response.ok(
                values=result,
                message='User Created'
            )
        except Exception as e:
            return Response.badRequest(message=str(e))


def createRole(request):
    if request.method == 'POST':
        try:
            x = request.body.decode('utf-8')
            print(x)
            data = json.loads(x)
            data_role = UserRole.objects.get(name__iexact=data['name'])
            if data_role:
                return Response.ok(
                    values=[],
                    message='Data sudah ada'
                )
            role = UserRole(
                name=data['name'],
                create_date=datetime.datetime.utcnow() + datetime.timedelta(hours=7),
                update_date=datetime.datetime.utcnow() + datetime.timedelta(hours=7)
            )
            role.save()
            result = role.serialize()
            print(result)
            return Response.ok(
                values=result,
                message='Role Created Successfully'
            )
        except Exception as e:
            #Response.badRequest(message=str(e))
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
        return Response.ok(
            values=result,
            message='No Data',
        )
    return HttpResponse('Success')


def getstaffsurvey(request):
    result = []
    param = request.GET.get('adminsurvey', None)

    if param:
        try:
            data = UserInfo.objects.filter(organization=param)
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
    organization = request.GET.get('organization', None)

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
        return Response.badRequest(
            message='UserRole not Found',
        )
    try:
        datauser = UserInfo.objects.filter(role=ObjectId(
            datarole.id), organization=ObjectId(organization))
    except UserInfo.DoesNotExist:
        return Response.badRequest(
            message='User not Found',
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
            data = request.POST.dict()
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
                return Response.badRequest(
                    values='null',
                    message='User not found'
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
            userfrom = data.get("userfrom",None)
            userto = data.get("userto",None)
            title = data.get("title",None)
            message = data.get("message",None)
            
            try:
                token = UserToken.objects.get(user=ObjectId(userto))
                Notification(
                    users=[token.key],
                    #users=['ef0D86AAQRG8Tu9ZXdEv2D:APA91bFmQDKHVjaTlRpUuHXEbXOVjywVyJuEoSrzjKLPqIrON4fviP9uJapeyZGQGFJ3WBODB_7xzFSeuNLpDZC0E_TMBH6jo8oJ5_QCF_qHCjBwxa7uQtacQGPgLgiI4DxoAKhJ1FcM'],
                    title=title,
                    message=message,
                ).send_message()
            except UserToken.DoesNotExist:
                return Response.badRequest(
                    values=[],
                    message='User tidak ada'
                )
            try:
                user = UserInfo.objects.get(id=userto)
            except UserInfo.DoesNotExist:
                return Response.badRequest(
                    values=[],
                    message='User tujuan tidak ada'
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
        if username==None:
            return Response.badRequest(
                values=[],
                message='User tidak bisa kosong'
            )
        notifs = Message.objects.filter(userto=username).order_by('-updated')[:5]
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
        datauser = UserInfo.objects.filter(role=ObjectId('5f13b370386bf295b4169f00'))
    except UserInfo.DoesNotExist:
        return Response.badRequest(
            message='User not Found',
        )
    for dt in datauser:
        dt.name = dt.username
        dt.save()

    return Response.ok(
        values=[],
        message=f'Update Data',
    )