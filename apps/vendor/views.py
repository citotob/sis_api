
from django.shortcuts import render
from django.http import JsonResponse
from sites.models import *
from vendor.models import *
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
from sites.serializer import *

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
        try:
            file = request.FILES['doc']
            if not file:
                return Response.badRequest(message='Doc tidak boleh kosong')
            fs = FileSystemStorage(
                    location=f'{settings.MEDIA_ROOT}/site/rfi/',
                    base_url=f'{settings.MEDIA_URL}/site/rfi/'
                )

            body_data = request.POST.dict()

            vendor = body_data.get('company')
            batchid = body_data.get('batch')
            rfi_no = body_data.get('rfi_no')
            tanggal_mulai_sla = body_data.get('tanggal_mulai_sla')
            tanggal_selesai_sla = body_data.get('tanggal_selesai_sla')

            #if status_=='Selesai':
            #    return Response.ok(
            #        values=[],
            #        message='Status sudah selesai'
            #    )
            try:
                comp = company.objects.get(id=ObjectId(vendor))
            except company.DoesNotExist:
                return Response.ok(
                    values=[],
                    message='Penyedia tidak ada'
                )

            try:
                data_batch_vendor = batch_vendor.objects.get(batch_id=ObjectId(batchid), vendor=ObjectId(comp.id))
            except batch_vendor.DoesNotExist:
                return Response.ok(message='Batch tidak ada')

            cek_status = [i for i, x in enumerate(
                data_batch_vendor.status) if x['status'] == 'Respon']
            if cek_status:
                result = data_batch_vendor.serialize()
                return Response.ok(
                    values=result,
                    message='Berhasil'
                )
            data_batch_vendor.rfi_no = rfi_no
            data_batch_vendor.tanggal_mulai_sla = tanggal_mulai_sla
            data_batch_vendor.tanggal_selesai_sla = tanggal_selesai_sla
            
            cek_status = [i for i, x in enumerate(
                    data_batch_vendor.status) if x['status'] == 'Respon']
            if not cek_status:
                status_respon = {'status': 'Respon', 'tanggal_pembuatan': datetime.utcnow(
                        ) + timedelta(hours=7)}
                data_batch_vendor.status.append(status_respon)
            data_batch_vendor.save()

            filename = fs.save(file.name, file)
            file_path = fs.url(filename)
            doc = document_batch_vendor(
                name=file.name,
                path=file_path,
                create_date=datetime.utcnow() + timedelta(hours=7),
                update_date=datetime.utcnow() + timedelta(hours=7)
            )
            doc.save()

            data_batch_vendor.rfi_doc = ObjectId(doc.id)
            data_batch_vendor.updated_at = datetime.utcnow() + timedelta(hours=7)
            data_batch_vendor.save()

            result = batch_vendor.objects.get(id=ObjectId(data_batch_vendor.id)).serialize()
            
            return Response.ok(
                values=result,
                message='Berhasil'
            )
        except Exception as e:
            return Response.badRequest(message=str(e))

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

        id_ = body_data.get('id_site')

        rekomen_tek = body_data.get('teknologi')
        tanggal_mulai_material = body_data.get('tanggal_mulai_material')
        tanggal_selesai_material = body_data.get('tanggal_selesai_material')
        tanggal_mulai_installation = body_data.get('tanggal_mulai_installation')
        tanggal_selesai_installation = body_data.get('tanggal_selesai_installation')
        tanggal_mulai_onair = body_data.get('tanggal_mulai_onair')
        tanggal_selesai_onair = body_data.get('tanggal_selesai_onair')
        tanggal_mulai_ir = body_data.get('tanggal_mulai_ir')
        tanggal_selesai_ir = body_data.get('tanggal_selesai_ir')

        try:
            data_site_vendor = site_vendor.objects.get(id=ObjectId(id_))
        except site_vendor.DoesNotExist:
            return Response.ok(message='Site tidak ada')

        cek_status = [i for i, x in enumerate(
            data_site_vendor.status) if x['status'] == 'Penawaran']
        if cek_status:
            result = data_site_vendor.serialize()
            return Response.ok(
                values=result,
                message='Berhasil'
            )
        data_site_vendor.rekomen_teknologi = rekomen_tek
        data_site_vendor.tanggal_mulai_material = tanggal_mulai_material
        data_site_vendor.tanggal_selesai_material = tanggal_selesai_material
        data_site_vendor.tanggal_mulai_installation = tanggal_mulai_installation
        data_site_vendor.tanggal_selesai_installation = tanggal_selesai_installation
        data_site_vendor.tanggal_mulai_onair = tanggal_mulai_onair
        data_site_vendor.tanggal_selesai_onair = tanggal_selesai_onair
        data_site_vendor.tanggal_mulai_ir = tanggal_mulai_ir
        data_site_vendor.tanggal_selesai_ir = tanggal_selesai_ir
        
        #cek_status = [i for i, x in enumerate(
        #        data_batch_vendor.status) if x['status'] == 'Respon']
        #if not cek_status:
        status_ = {'status': 'Penawaran', 'tanggal_pembuatan': datetime.utcnow(
            ) + timedelta(hours=7)}
        data_site_vendor.status.append(status_)
        #data_site_vendor.save()

        data_site_vendor.updated_at = datetime.utcnow() + timedelta(hours=7)
        data_site_vendor.save()

        #try:
        #        data_batch_vendor = batch_vendor.objects.get(batch_id=ObjectId(batchid), vendor=ObjectId(comp.id))
        #    except batch_vendor.DoesNotExist:
        #        return Response.ok(message='Batch tidak ada')

        result = site_vendor.objects.get(id=ObjectId(data_site_vendor.id)).serialize()
        
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