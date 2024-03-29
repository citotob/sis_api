
from django.shortcuts import render
from django.http import JsonResponse
from apps.sites.models import *
from apps.sites.serializer import VendorApplicationSerializer, CheckVendorApplicationSerializer
# from vendor.models import *
from userinfo.models import *
from userinfo.views import authenticate_credentials
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
import json
from django.core.exceptions import ObjectDoesNotExist
import pandas
from .response import Response
from bson import ObjectId, json_util
from django.http import HttpResponse
# import datetime
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
from django.core.serializers import serialize
from django.core.files.storage import FileSystemStorage
import requests
from apps.vendorperformance.models import VPScore
from apps.vendorperformance.serializer import VPSerializer
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.core import serializers
from vendor.serializer import *
from itertools import groupby
from userinfo.utils.notification import Notification
import calendar
from math import radians, cos, sin, asin, sqrt
from sites.serializer import *
from mongoengine.queryset.visitor import Q

from notification.utils.CustomNotification import CustomNotification

from odps.models import Odp

from notification.utils.CustomNotification import CustomNotification


def getallvendor(request):
    # token = request.META.get("HTTP_AUTHORIZATION").replace(" ", "")[6:]
    # ret, user = authenticate_credentials(token)
    # if False == ret or None == user:
    #    return JsonResponse({"state": "fail"})
    try:
        data = vendor.objects.all()

        serializer = vendorSerializer(data, many=True)
        return Response.ok(
            values=json.loads(json.dumps(serializer.data, default=str)),
            message=f'{len(serializer.data)} Data'
        )
    except Exception as e:
        return Response.badRequest(message=str(e))


def respon(request):
    # token = request.META.get("HTTP_AUTHORIZATION").replace(" ", "")[6:]
    # ret, user = authenticate_credentials(token)
    # if False == ret or None == user:
    #    return JsonResponse({"state": "fail"})
    if request.method == "POST":  # Add
        try:
            file = request.FILES['doc']
            if not file:
                return Response.badRequest(message='Doc tidak boleh kosong')
            fs = FileSystemStorage(
                location=f'{settings.MEDIA_ROOT}/site/rfi/',
                base_url=f'{settings.MEDIA_URL}/site/rfi/'
            )

            body_data = request.POST.dict()

            # vendor = body_data.get('company')
            userid = body_data.get('userid')
            batchid = body_data.get('batch')
            rfi_no = body_data.get('rfi_no')
            tanggal_mulai_sla = datetime.strptime(
                body_data.get('tanggal_mulai_sla'), '%Y-%m-%d 00:00:00')
            tanggal_selesai_sla = datetime.strptime(
                body_data.get('tanggal_selesai_sla'), '%Y-%m-%d 23:59:59')

            try:
                data_user = UserInfo.objects.get(id=ObjectId(userid))
            except UserInfo.DoesNotExist:
                # return Response.ok(
                #    values=[],
                #    message='User tidak ada'
                # )
                return Response().base(
                    success=False,
                    message='User tidak ada',
                    status=404
                )

            data_vp_score = VPScore.objects.filter(
                vendor=data_user.company.id).order_by('-created_at').first()
            if not data_vp_score:
                # return Response.ok(
                #    values=[],
                #    message='vp_score tidak ada'
                # )
                return Response().base(
                    success=False,
                    message='vp_score tidak ada',
                    status=404
                )
            data_vendor_application = vendor_application(
                users=userid,
                vendorid=data_user.company.id,
                batchid=ObjectId(batchid),
                vp_score_id=data_vp_score.id,
                rank=1,
                rfi_no=rfi_no,
                tanggal_mulai_sla=tanggal_mulai_sla,
                tanggal_akhir_sla=tanggal_selesai_sla,
                days_sla=(
                    tanggal_selesai_sla.date() - tanggal_mulai_sla.date()).days,
            )

            data_vendor_application.save()

            filename = fs.save(file.name, file)
            file_path = fs.url(filename)
            doc = rfi_doc(
                name=file.name,
                path=file_path
            )
            doc.save()

            data_vendor_application.rfi_doc = ObjectId(doc.id)
            data_vendor_application.save()

            # data_smm = site_matchmaking.objects.(batch=batchid)

            data_result = vendor_application.objects.get(
                id=ObjectId(data_vendor_application.id))  # .serialize()
            serializer = vendor_applicationResponSerializer(data_result)
            result = serializer.data
            return Response.ok(
                values=result,
                message='Berhasil'
            )
        except Exception as e:
            return Response.badRequest(message=str(e))

    else:
        return Response.badRequest(message='Hanya POST')


def penawaran_(request):
    # token = request.META.get("HTTP_AUTHORIZATION").replace(" ", "")[6:]
    # ret, user = authenticate_credentials(token)
    # if False == ret or None == user:
    #    return JsonResponse({"state": "fail"})
    if request.method == "POST":  # Add
        # try:
        file = request.FILES['doc']
        if not file:
            return Response.badRequest(message='Doc tidak boleh kosong')
        fs = FileSystemStorage(
            location=f'{settings.MEDIA_ROOT}/site/quotation/',
            base_url=f'{settings.MEDIA_URL}/site/quotation/'
        )

        body_data = request.POST.dict()

        siteid = body_data.get('siteid')
        batchid = body_data.get('batchid')
        vendorid = body_data.get('vendorid')
        biaya = body_data.get('biaya')

        rekomen_tek = body_data.get('teknologi')
        tanggal_mulai_material = datetime.strptime(
            body_data.get('tanggal_mulai_material'), '%Y-%m-%d 00:00:00')
        tanggal_selesai_material = datetime.strptime(
            body_data.get('tanggal_selesai_material'), '%Y-%m-%d 23:59:59')
        tanggal_mulai_installation = datetime.strptime(
            body_data.get('tanggal_mulai_installation'), '%Y-%m-%d 00:00:00')
        tanggal_selesai_installation = datetime.strptime(
            body_data.get('tanggal_selesai_installation'), '%Y-%m-%d 23:59:59')
        tanggal_mulai_onair = datetime.strptime(
            body_data.get('tanggal_mulai_onair'), '%Y-%m-%d 00:00:00')
        tanggal_selesai_onair = datetime.strptime(
            body_data.get('tanggal_selesai_onair'), '%Y-%m-%d 23:59:59')
        tanggal_mulai_ir = datetime.strptime(
            body_data.get('tanggal_mulai_ir'), '%Y-%m-%d 00:00:00')
        tanggal_selesai_ir = datetime.strptime(
            body_data.get('tanggal_selesai_ir'), '%Y-%m-%d 23:59:59')

        try:
            data_vendor_application = vendor_application.objects.get(
                batchid=batchid, vendorid=vendorid)
        except vendor_application.DoesNotExist:
            # return Response.ok(
            #    values=[],
            #    message='vendor_application tidak ada'
            # )
            return Response().base(
                success=False,
                message='vendor_application tidak ada',
                status=404
            )
        #data_vendor_application.rfi_score_id = data_rfi_score.id
        # data_vendor_application.save()

        data_rfi_score = rfi_score(
            vendor_app=data_vendor_application.id,
            rekomendasi_teknologi=rekomen_tek,
            material_on_site=tanggal_mulai_material,
            installation=tanggal_mulai_installation,
            on_air=tanggal_mulai_onair,
            integration=tanggal_mulai_ir,
            days_material_on_site=(
                tanggal_selesai_material.date() - tanggal_mulai_material.date()).days,
            days_installation=(tanggal_selesai_installation.date(
            ) - tanggal_mulai_installation.date()).days,
            days_on_air=(tanggal_selesai_onair.date() -
                         tanggal_mulai_onair.date()).days,
            days_on_integration=(
                tanggal_selesai_ir.date() - tanggal_mulai_ir.date()).days,
            biaya=biaya,
        )

        filename = fs.save(file.name, file)
        file_path = fs.url(filename)
        doc = doc_quotation(
            name=file.name,
            path=file_path
        )
        doc.save()

        data_rfi_score.doc_quotation = ObjectId(doc.id)
        data_rfi_score.save()

        data_rfi_score.save()

        try:
            data_smm = site_matchmaking.objects.get(
                batchid=batchid, siteid=siteid)
        except site_matchmaking.DoesNotExist:
            # return Response.ok(
            #    values=[],
            #    message='Site_matchmaking tidak ada'
            # )
            return Response().base(
                success=False,
                message='Site_matchmaking tidak ada',
                status=404
            )

        # data_smm.applicants.append(data_vendor_application.id)
        data_smm.rfi_score.append(data_rfi_score.id)
        data_smm.save()

        # result = site_vendor.objects.get(id=ObjectId(data_site_vendor.id)).serialize()
        serializer = rfi_scoreSerializer(data_rfi_score)
        #result = serializer.data

        return Response.ok(
            values=json.loads(json.dumps(serializer.data, default=str)),
            message='Berhasil'
        )
        # except Exception as e:
        #    return Response.badRequest(message=str(e))

    else:
        return Response.badRequest(message='Hanya POST')


def penawaran(request):
    # token = request.META.get("HTTP_AUTHORIZATION").replace(" ", "")[6:]
    # ret, user = authenticate_credentials(token)
    # if False == ret or None == user:
    #    return JsonResponse({"state": "fail"})
    if request.method == "POST":  # Add
        # try:
        body_data = json.loads(request.body)

        # vendor = body_data.get('company')
        # batchid = body_data.get('batch')

        siteid = body_data.get('siteid')
        batchid = body_data.get('batchid')
        vendorid = body_data.get('vendorid')
        userfrom = body_data.get('userfrom')

        rekomen_tek = body_data.get('teknologi')
        tanggal_mulai_material = datetime.strptime(
            body_data.get('tanggal_mulai_material'), '%Y-%m-%d 00:00:00')
        tanggal_selesai_material = datetime.strptime(
            body_data.get('tanggal_selesai_material'), '%Y-%m-%d 23:59:59')
        tanggal_mulai_installation = datetime.strptime(
            body_data.get('tanggal_mulai_installation'), '%Y-%m-%d 00:00:00')
        tanggal_selesai_installation = datetime.strptime(
            body_data.get('tanggal_selesai_installation'), '%Y-%m-%d 23:59:59')
        tanggal_mulai_onair = datetime.strptime(
            body_data.get('tanggal_mulai_onair'), '%Y-%m-%d 00:00:00')
        tanggal_selesai_onair = datetime.strptime(
            body_data.get('tanggal_selesai_onair'), '%Y-%m-%d 23:59:59')
        tanggal_mulai_ir = datetime.strptime(
            body_data.get('tanggal_mulai_ir'), '%Y-%m-%d 00:00:00')
        tanggal_selesai_ir = datetime.strptime(
            body_data.get('tanggal_selesai_ir'), '%Y-%m-%d 23:59:59')
        biaya = body_data.get('biaya')

        try:
            data_vendor_application = vendor_application.objects.get(
                batchid=batchid, vendorid=vendorid)
        except vendor_application.DoesNotExist:
            # return Response.ok(
            #    values=[],
            #    message='vendor_application tidak ada'
            # )
            return Response().base(
                success=False,
                message='vendor_application tidak ada',
                status=404
            )
        #data_vendor_application.rfi_score_id = data_rfi_score.id
        # data_vendor_application.save()

        data_rfi_score = rfi_score(
            vendor_app=data_vendor_application.id,
            rekomendasi_teknologi=rekomen_tek,
            material_on_site=tanggal_mulai_material,
            installation=tanggal_mulai_installation,
            on_air=tanggal_mulai_onair,
            integration=tanggal_mulai_ir,
            days_material_on_site=(
                tanggal_selesai_material.date() - tanggal_mulai_material.date()).days,
            days_installation=(tanggal_selesai_installation.date(
            ) - tanggal_mulai_installation.date()).days,
            days_on_air=(tanggal_selesai_onair.date() -
                         tanggal_mulai_onair.date()).days,
            days_on_integration=(
                tanggal_selesai_ir.date() - tanggal_mulai_ir.date()).days,
            biaya=biaya,
        )

        data_rfi_score.save()

        try:
            data_smm = site_matchmaking.objects.get(
                batchid=batchid, siteid=siteid)
        except site_matchmaking.DoesNotExist:
            # return Response.ok(
            #    values=[],
            #    message='Site_matchmaking tidak ada'
            # )
            return Response().base(
                success=False,
                message='Site_matchmaking tidak ada',
                status=404
            )

        # data_smm.applicants.append(data_vendor_application.id)
        data_smm.rfi_score.append(data_rfi_score.id)
        data_smm.save()

        # result = site_vendor.objects.get(id=ObjectId(data_site_vendor.id)).serialize()
        serializer = rfi_scoreSerializer(data_rfi_score)
        #result = serializer.data

        req_fields = ['id']
        admin_users = UserInfo.objects.filter(
            role='5f73fdfc28751d590d835266', status='Aktif').only(*req_fields)
        if admin_users:
            try:
                data_batch = batch.objects.get(id=ObjectId(batchid))
                list_admin_users = []
                for usr in admin_users:
                    list_admin_users.append(usr.id)
                notif = CustomNotification()
                notif.create(to=list_admin_users, from_=ObjectId(userfrom), type='batch offer submitted',
                             title='User telah mengajukan penawaran', message='penawaran batch '+data_batch.judul+' telah diajukan', push_message='Ada pesan baru')
            except batch.DoesNotExist:
                pass

        return Response.ok(
            values=json.loads(json.dumps(serializer.data, default=str)),
            message='Berhasil'
        )
        # except Exception as e:
        #    return Response.badRequest(message=str(e))

    else:
        return Response.badRequest(message='Hanya POST')


def getbatch(request):
    # token = request.META.get("HTTP_AUTHORIZATION").replace(" ", "")[6:]
    # ret, user = authenticate_credentials(token)
    # if False == ret or None == user:
    #    return JsonResponse({"state": "fail"})
    try:
        body_data = json.loads(request.body)
        vendor_id = body_data.get('penyedia')

        # data = batch.objects.filter(penyedia_undang=vendor_id, status__status='Dibuka',
        #                            tanggal_selesai_undangan__gte=datetime.utcnow() + timedelta(hours=7))
        data = batch.objects.filter(
            penyedia_undang=vendor_id, status__status='Dibuka')

        serializer = BatchSerializer(data, many=True)
        return Response.ok(
            values=json.loads(json.dumps(serializer.data, default=str)),
            message=f'{len(serializer.data)} Data'
        )
    except Exception as e:
        return Response.badRequest(message=str(e))


def getsite(request):
    # token = request.META.get("HTTP_AUTHORIZATION").replace(" ", "")[6:]
    # ret, user = authenticate_credentials(token)
    # if False == ret or None == user:
    #    return JsonResponse({"state": "fail"})
    body_data = json.loads(request.body)
    batch_id = body_data.get('batch')
    vendor_id = body_data.get('penyedia')

    pipeline = [
        {
            '$lookup': {
                'from': 'site_location',
                'localField': 'site_id',
                'foreignField': '_id',
                'as': 'site_location'
            }
        }, {
            '$unwind': {
                'path': '$site_location'
            }
        }, {
            '$match': {
                'vendor': ObjectId(vendor_id),
                'batch_id': ObjectId(batch_id)
            }
        }, {
            '$project': {
                'kodeTitik': '$site_location.kode_pos',
                'provinsi': '$site_location.provinsi',
                'kabupaten/kota': '$site_location.kabupaten',
                'kecamatan': '$site_location.kecamatan',
                'desa': '$site_location.desa',
                'longitude': '$site_location.longitude',
                'latitude': '$site_location.latitude'
            }
        }
    ]
    pipe = pipeline  # + skip
    agg_cursor = site_vendor.objects.aggregate(*pipe)

    site_list = list(agg_cursor)

    # for btc in batch_list:

    if len(site_list) > 0:
        return Response.ok(
            values=json.loads(json.dumps(site_list, default=str)),
            message=f'{len(site_list)} Data'
        )
    else:
        # return Response.ok(
        #    values=[],
        #    message='Data tidak ada'
        # )
        return Response().base(
            success=False,
            message='Data tidak ada',
            status=404
        )


def getVendorApp(request):
    try:
        batch = request.GET.get('batch')
        vendor = request.GET.get('vendor')
        if not vendor or not batch:
            return Response.badRequest(
                message="Need Param 'vendor' & 'batch'"
            )
        data = vendor_application.objects(batchid=batch, vendorid=vendor)
        serializer = CheckVendorApplicationSerializer(data, many=True)
        if len(serializer.data) > 0:
            return Response.ok(
                values=json.loads(json.dumps(serializer.data, default=str)),
                message=f'{len(serializer.data)} Data'
            )
        else:
            # return Response.ok(
            #    values=[],
            #    message='Data tidak ada'
            # )
            return Response().base(
                success=False,
                message='Data tidak ada',
                status=404
            )
    except Exception as e:
        print(e)


def getDashboardData(request):

    try:
        if request.method == "POST":
            if not request.body:
                raise Exception('Need Json Body')
            body_data = json.loads(request.body)
            vendorId = body_data.get('vendor', None)

            if not vendorId:
                raise Exception('Need Body `vendor`')

            try:
                vendorData = vendor.objects.get(id=vendorId)
            except vendor.DoesNotExist:
                raise Exception('Vendor not Found')

            vendorCount = vendor.objects.all().count()
            activeUserCount = UserInfo.objects(
                company=vendorData.id, status='Aktif').count()
            requestedUserCount = UserInfo.objects(
                company=vendorData.id, status='Belum Terverifikasi').count()
            listBatch = vendor_application.objects(vendorid=vendorData.id)
            batchCount = batch.objects(
                id__in=[x.id for x in listBatch.scalar('batchid')]).count()
            # siteCount = site_matchmaking.objects(
            #    batchid__exists=True, batchid__in=listBatch.scalar('id')).count()
            siteCount = site_matchmaking.objects(
                batchid__exists=True, batchid__in=listBatch.scalar('batchid')).count()
            rfiCount = listBatch.count()

            totallayananai = Odp.objects(vendorid=vendorData.id).count()
            totallayananaifo = Odp.objects(vendorid=vendorData.id, teknologi__in=[
                                           'FIBER OPTIK', 'FO']).count()
            totallayananairl = Odp.objects(vendorid=vendorData.id, teknologi__in=[
                                           'RADIO LINK', 'RL']).count()
            totallayananaivsat = Odp.objects(
                vendorid=vendorData.id, teknologi='VSAT').count()

            siteNonBatchCount = 0

            result = {
                "vendor": vendorCount,
                "active_user": activeUserCount,
                "requested_user": requestedUserCount,
                "batch": batchCount,
                "site": siteCount,
                "rfi": rfiCount,
                "site_not_batch": siteNonBatchCount,
                "totallayananai": totallayananai,
                "totallayananaifo": totallayananaifo,
                "totallayananairl": totallayananairl,
                "totallayananaivsat": totallayananaivsat,
            }

            return Response.ok(
                values=result
            )
        else:
            raise Exception('Method Post Only')

    except Exception as e:
        return Response.badRequest(
            values=[],
            message=str(e)
        )
