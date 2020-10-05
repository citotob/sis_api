
from django.shortcuts import render
from django.http import JsonResponse
from sites.models import *
#from vendor.models import *
#from userinfo.models import batch
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
#import datetime
from datetime import datetime, timedelta, timezone
from django.core.serializers import serialize
from django.core.files.storage import FileSystemStorage
import requests

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.core import serializers
from vendor.serializer import *

from itertools import groupby
from userinfo.utils.notification import Notification
import calendar
from math import radians, cos, sin, asin, sqrt


def respon(request):
    # token = request.META.get("HTTP_AUTHORIZATION").replace(" ", "")[6:]
    # ret, user = authenticate_credentials(token)
    # if False == ret or None == user:
    #    return JsonResponse({"state": "fail"})
    if request.method == "POST":  # Add
        #try:
        file = request.FILES['doc']
        if not file:
            return Response.badRequest(message='Doc tidak boleh kosong')
        fs = FileSystemStorage(
                location=f'{settings.MEDIA_ROOT}/site/rfi/',
                base_url=f'{settings.MEDIA_URL}/site/rfi/'
            )

        body_data = request.POST.dict()

        #vendor = body_data.get('company')
        userid = body_data.get('userid')
        batchid = body_data.get('batch')
        rfi_no = body_data.get('rfi_no')
        tanggal_mulai_sla = body_data.get('tanggal_mulai_sla')
        tanggal_selesai_sla = body_data.get('tanggal_selesai_sla')

        try:
            data_user = UserInfo.objects.get(id=ObjectId(userid))
        except UserInfo.DoesNotExist:
            return Response.ok(
                values=[],
                message='User tidak ada'
            )
        print(data_user.company.id)
        data_vp_score = vp_score.objects.filter(vendorid=data_user.company.id).first()
        print(data_vp_score)
        if not data_vp_score:
            return Response.ok(
                values=[],
                message='vp_score tidak ada'
            )
        data_vendor_application = vendor_application(
            users=userid,
            vendorid=data_user.company,
            batchid=ObjectId(batchid),
            vp_score_id = data_vp_score.id,
            rank = 1,
            rfi_no = rfi_no,
            tanggal_mulai_sla = tanggal_mulai_sla,
            tanggal_akhir_sla = tanggal_selesai_sla
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

        #data_smm = site_matchmaking.objects.(batch=batchid)

        data_result = vendor_application.objects.get(id=ObjectId(data_vendor_application.id))#.serialize()
        serializer = vendor_applicationResponSerializer(data_result)
        result = serializer.data
        return Response.ok(
            values=result,
            message='Berhasil'
        )
        #except Exception as e:
        #    return Response.badRequest(message=str(e))

    else:
        return Response.badRequest(message='Hanya POST')

def penawaran(request):
    # token = request.META.get("HTTP_AUTHORIZATION").replace(" ", "")[6:]
    # ret, user = authenticate_credentials(token)
    # if False == ret or None == user:
    #    return JsonResponse({"state": "fail"})
    if request.method == "POST":  # Add
        #try:
        body_data = json.loads(request.body)

        #vendor = body_data.get('company')
        #batchid = body_data.get('batch')

        siteid = body_data.get('siteid')
        batchid = body_data.get('batchid')
        vendorid = body_data.get('vendorid')

        rekomen_tek = body_data.get('teknologi')
        tanggal_mulai_material = datetime.strptime(body_data.get('tanggal_mulai_material'), '%Y-%m-%d 00:00:00')
        tanggal_selesai_material = datetime.strptime(body_data.get('tanggal_selesai_material'), '%Y-%m-%d 23:59:59')
        tanggal_mulai_installation = datetime.strptime(body_data.get('tanggal_mulai_installation'), '%Y-%m-%d 00:00:00')
        tanggal_selesai_installation = datetime.strptime(body_data.get('tanggal_selesai_installation'), '%Y-%m-%d 23:59:59')
        tanggal_mulai_onair = datetime.strptime(body_data.get('tanggal_mulai_onair'), '%Y-%m-%d 00:00:00')
        tanggal_selesai_onair = datetime.strptime(body_data.get('tanggal_selesai_onair'), '%Y-%m-%d 23:59:59')
        tanggal_mulai_ir = datetime.strptime(body_data.get('tanggal_mulai_ir'), '%Y-%m-%d 00:00:00')
        tanggal_selesai_ir = datetime.strptime(body_data.get('tanggal_selesai_ir'), '%Y-%m-%d 23:59:59')

        data_rfi_score = rfi_score(
                rekomendasi_teknologi=rekomen_tek,
                material_on_site = tanggal_mulai_material,
                installation = tanggal_mulai_installation,
                on_air = tanggal_mulai_onair,
                integration = tanggal_mulai_ir,
                days_material_on_site = (tanggal_selesai_material.date() - tanggal_mulai_material.date()).days,
                days_installation = (tanggal_selesai_installation.date() - tanggal_mulai_installation.date()).days,
                days_on_air = (tanggal_selesai_onair.date() - tanggal_mulai_onair.date()).days,
                days_on_integration = (tanggal_selesai_ir.date() - tanggal_mulai_ir.date()).days
            )

        data_rfi_score.save()

        try:
            data_vendor_application = vendor_application.objects.get(batchid=batchid,vendorid=vendorid)
        except vendor_application.DoesNotExist:
            return Response.ok(
                values=[],
                message='vendor_application tidak ada'
            )
        data_vendor_application.rfi_score_id = data_rfi_score.id
        data_vendor_application.save()

        try:
            data_smm = site_matchmaking.objects.get(batchid=batchid,siteid=siteid)
        except site_matchmaking.DoesNotExist:
            return Response.ok(
                values=[],
                message='Site_matchmaking tidak ada'
            )

        data_smm.applicants.append(data_vendor_application.id)
        data_smm.save()

        #result = site_vendor.objects.get(id=ObjectId(data_site_vendor.id)).serialize()
        serializer = rfi_scoreSerializer(data_rfi_score)
        result = serializer.data
        
        return Response.ok(
            values=result,
            message='Berhasil'
        )
        #except Exception as e:
        #    return Response.badRequest(message=str(e))

    else:
        return Response.badRequest(message='Hanya POST')


def getbatch(request):
    # token = request.META.get("HTTP_AUTHORIZATION").replace(" ", "")[6:]
    # ret, user = authenticate_credentials(token)
    # if False == ret or None == user:
    #    return JsonResponse({"state": "fail"})
    body_data = json.loads(request.body)
    #batch_id = body_data.get('batch')
    vendor_id = body_data.get('penyedia')

    #page = int(body_data.get('page', 0)) - 1
    #skip = []
    #if page >= 0:
    #    skip = [{'$skip': 20 * page},
    #            {'$limit': 20}]
    """
    pipeline = [
        {
            '$lookup': {
                'from': 'batch_vendor', 
                'localField': '_id', 
                'foreignField': 'batch_id', 
                'as': 'batchVendor'
            }
        }, {
            '$unwind': {
                'path': '$batchVendor'
            }
        }, {
            '$lookup': {
                'from': 'site_vendor', 
                'localField': 'batchVendor.batch_id', 
                'foreignField': 'batch_id', 
                'as': 'siteVendor'
            }
        }, {
            '$unwind': {
                'path': '$siteVendor'
            }
        }, {
            '$lookup': {
                'from': 'site_location', 
                'localField': 'siteVendor.site_id', 
                'foreignField': '_id', 
                'as': 'siteLocation'
            }
        }, {
            '$unwind': {
                'path': '$siteLocation'
            }
        }
    ]
    """
    pipeline = [
        {
            '$lookup': {
                'from': 'site_vendor', 
                'localField': '_id', 
                'foreignField': 'batch_id', 
                'as': 'site_vendor'
            }
        }, {
            '$unwind': {
                'path': '$site_vendor'
            }
        }, {
            '$match': {
                'site_vendor.vendor': ObjectId(vendor_id)
            }
        }, {
            '$project': {
                'judul': '$judul', 
                'rfiNo': '$rfi_no', 
                'tanggal_mulai_undangan': '$tanggal_mulai_undangan', 
                'tanggal_selesai_undangan': '$tanggal_selesai_undangan'
            }
        }, {
            '$group': {
                '_id': '$judul', 
                'rfi_no': {
                    '$first': '$rfiNo'
                }, 
                'tanggal_mulai_undangan': {
                    '$first': '$tanggal_mulai_undangan'
                }, 
                'tanggal_selesai_undangan': {
                    '$first': '$tanggal_selesai_undangan'
                }, 
                'jumlahTitik': {
                    '$sum': 1
                }
            }
        }
    ]
    pipe = pipeline #+ skip
    agg_cursor = batch.objects.aggregate(*pipe)

    batch_list = list(agg_cursor)

    #for btc in batch_list:

    if len(batch_list) > 0:
        return Response.ok(
            values=json.loads(json.dumps(batch_list, default=str)),
            message=f'{len(batch_list)} Data'
        )
    else:
        return Response.ok(
            values=[],
            message='Data tidak ada'
        )

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
    pipe = pipeline #+ skip
    agg_cursor = site_vendor.objects.aggregate(*pipe)

    site_list = list(agg_cursor)

    #for btc in batch_list:

    if len(site_list) > 0:
        return Response.ok(
            values=json.loads(json.dumps(site_list, default=str)),
            message=f'{len(site_list)} Data'
        )
    else:
        return Response.ok(
            values=[],
            message='Data tidak ada'
        )