
from django.shortcuts import render
from django.http import JsonResponse
from sites.models import *
from vendor.models import *
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


def getLaporan(request):

    if request.method == "POST":

        bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
                 "Juli", "Agustus", "September", "Oktober", "November", "Desember"]

        try:
            req = request.body.decode("utf-8")
            data = json.loads(req)
            month = data['month']
            year = data['year']

            pastMonth = data['month'] - 1
            pastYear = year

            if pastMonth == 0:
                pastMonth = 12
                pastYear = year-1

            ai = '5f16b4ba149882a98fc6655e'
            bts = '5f1521524f9c6764c713d73c'

            if month is None or year is None:
                return Response.badRequest(message='Need Json Body "month" & "year"')

            def pipelineDate(month, year, jenis):

                lastDay = calendar.monthrange(year=year, month=month)[1]
                return [
                    {
                        '$addFields': {
                            'last': {
                                '$arrayElemAt': [
                                    '$status', -1
                                ]
                            }
                        }
                    }, {
                        '$match': {
                            'jenissurvey': ObjectId(jenis),
                            'last.status': 'finished',
                            'last.date': {
                                '$gte': datetime(year, month, 1, 00, 00, 00, tzinfo=timezone.utc),
                                '$lte': datetime(year, month, lastDay, 23, 59, 59, tzinfo=timezone.utc)
                            }
                        }
                    }, {
                        '$count': 'count'
                    }
                ]

            def pipelineTotal(jenis, status):
                return [
                    {
                        '$match': {
                            'jenissurvey': ObjectId(jenis),
                            'status.status': status,
                        }
                    }, {
                        '$count': 'count'
                    }
                ]

            penugasanAITotal = list(
                Penugasan.objects.aggregate(pipelineTotal(jenis=ai, status='assigned')))[0]['count']
            penugasanBTSTotal = list(
                Penugasan.objects.aggregate(pipelineTotal(jenis=bts, status='assigned')))[0]['count']

            penugasanAITotalFinish = list(
                Penugasan.objects.aggregate(pipelineTotal(jenis=ai, status='finished')))[0]['count']
            penugasanBTSTotalFinish = list(
                Penugasan.objects.aggregate(pipelineTotal(jenis=bts, status='finished')))[0]['count']

            penugasanPersentaseAI = (
                penugasanAITotalFinish/penugasanAITotal) * 100
            penugasanPersentaseBTS = (
                penugasanBTSTotalFinish / penugasanBTSTotal) * 100

            penugasanAISekarangList = list(
                Penugasan.objects.aggregate(pipelineDate(jenis=ai, month=month, year=year)))
            penugasanBTSSekarangList = list(
                Penugasan.objects.aggregate(pipelineDate(jenis=bts, month=month, year=year)))

            penugasanAISebelumnyaList = list(
                Penugasan.objects.aggregate(pipelineDate(jenis=ai, month=pastMonth, year=pastYear)))
            penugasanBTSSebelumnyaList = list(
                Penugasan.objects.aggregate(pipelineDate(jenis=bts, month=pastMonth, year=pastYear)))

            penugasanAISekarang = 0 if len(
                penugasanAISekarangList) == 0 else penugasanAISekarangList[0]['count']
            penugasanBTSSekarang = 0 if len(
                penugasanBTSSekarangList) == 0 else penugasanBTSSekarangList[0]['count']

            penugasanAISebelumnya = 0 if len(
                penugasanAISebelumnyaList) == 0 else penugasanAISebelumnyaList[0]['count']
            penugasanBTSSebelumnya = 0 if len(
                penugasanBTSSebelumnyaList) == 0 else penugasanBTSSebelumnyaList[0]['count']

            persentasiKenaikanAI = ((
                abs(penugasanAISekarang - penugasanAISebelumnya)) / penugasanAISebelumnya) * 100 if penugasanAISebelumnya > 0 else 0
            persentasiKenaikanBTS = ((
                abs(penugasanBTSSekarang - penugasanBTSSebelumnya)) / penugasanBTSSebelumnya) * 100 if penugasanAISebelumnya > 0 else 0

            try:
                subject = f'Monthly Report SMASLAB {bulan[month-1]} {year}'
                text_content = ''
                htmly = get_template('email/executive/executive.html')
                d = {
                    'bulan': f'{bulan[month-1]} {year}',

                    'ai_finish': penugasanAITotalFinish,
                    'ai_total': penugasanAITotal,

                    'bts_finish': penugasanAITotalFinish,
                    'bts_total': penugasanAITotal,

                    'ai_persentase': round(penugasanPersentaseAI, 2),
                    'ai_penambahan': persentasiKenaikanAI,
                    'ai_bulan': penugasanAISekarang,

                    'bts_persentase': round(penugasanPersentaseBTS, 2),
                    'bts_penambahan': persentasiKenaikanBTS,
                    'bts_bulan': penugasanBTSSekarang,

                    'ai_perubahan': 'Kenaikan' if penugasanAISekarang > penugasanAISebelumnya else 'Penurunan' if penugasanAISekarang < penugasanAISebelumnya else 'Tidak ada Perubahan',
                    'ai_persentase_penambahan': f'{round(persentasiKenaikanAI, 2)}%' if penugasanAISekarang != penugasanAISebelumnya else '',

                    'bts_perubahan': 'Kenaikan' if penugasanBTSSekarang > penugasanBTSSebelumnya else 'Penurunan' if penugasanBTSSekarang < penugasanBTSSebelumnya else 'Tidak ada Perubahan',
                    'bts_persentase_penambahan': f'{round(persentasiKenaikanBTS, 2)}%' if penugasanBTSSekarang != penugasanBTSSebelumnya else '',

                    'media_url': settings.URL_MEDIA,
                    'survej_url': settings.URL_LOGIN,

                    'message_bottom': 'silahkan login akun SMASLAB untuk melihat detil laporan melalui aplikasi mobile ataupun website '+settings.URL_LOGIN

                }

                executive = [x.email for x in UserInfo.objects.filter(
                    role=ObjectId('5f27f7a6ea250a01d2b99d7a'))]

                html_content = htmly.render(d)
                sender = settings.EMAIL_ADMIN

                msg = EmailMultiAlternatives(
                    subject, text_content, sender, executive)
                msg.attach_alternative(html_content, "text/html")
                response = msg.send()
                # print('asdad', response)
            except:
                pass

        except Exception as e:
            print(e)
        #return HttpResponse(f' & ')
        return Response.ok(
            values=[],
            message='Berhasil'
        )
    #return HttpResponse(f'asd')
    return Response.badRequest(
        values=[],
        message='Gagal'
    )


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def uploadlokasi(request):
    if request.method == 'POST':
        import openpyxl
        excel_file = request.FILES["excel_file"]

        # you may put validations here to check extension or file size

        wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets
        worksheet = wb["List Lokasi Survey"]
        print(worksheet)

        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
        lokasi_gagal = ''

        for row in worksheet.iter_rows():
            if str(row[1].value) == 'None':
                break
            if str(row[0].value) == 'NO':
                continue

            if str(row[1].value).upper() == 'PERMOHONAN AKSES INTERNET':
                jns = 'AI'
            else:
                jns = 'BTS'
            # try:
            data_provinsi = provinsi.objects.filter(
                name=str(row[2].value).upper()).first()
            # if len(data_provinsi) == 0:
            if data_provinsi is None:
                # continue
                data_provinsi = provinsi(
                    name=str(row[2].value).upper()
                )
                data_provinsi.save()
            if str(row[3].value)[0:3].upper() == 'KAB':
                kabupaten_ = kabupaten.objects.filter(
                    name=str(row[3].value).upper()).first()
                if kabupaten_ is None:
                    # continue
                    kabupaten_ = kabupaten(
                        name=str(row[3].value).upper(),
                        provinsi=ObjectId(data_provinsi.id)
                    )
                    kabupaten_.save()
            else:
                kota_ = kota.objects.filter(
                    name=str(row[3].value).upper()).first()
                if kota_ is None:
                    # continue
                    kota_ = kota(
                        name=str(row[3].value).upper(),
                        provinsi=ObjectId(data_provinsi.id)
                    )
                    kota_.save()
            data_kecamatan = kecamatan.objects.filter(
                name=str(row[4].value).upper()).first()
            if data_kecamatan is None:
                # continue
                try:
                    data_kecamatan = kecamatan(
                        name=str(row[4].value).upper(),
                        kabupaten=ObjectId(kabupaten_.id)
                    )
                    data_kecamatan.save()
                except:
                    data_kecamatan = kecamatan(
                        name=str(row[4].value).upper(),
                        kota=ObjectId(kota_.id)
                    )
                    data_kecamatan.save()
            data_desa = desa.objects.filter(
                name=str(row[5].value).upper()).first()

            if data_desa is None:
                # continue
                data_desa = desa(
                    name=str(row[5].value).upper(),
                    kecamatan=ObjectId(data_kecamatan.id)
                )
                data_desa.save()
            else:
                LokSurvey_ = LokasiSurvey.objects.filter(
                    desa=ObjectId(data_desa.id), jenis=jns)
                if len(LokSurvey_) > 0:
                    lokasi_gagal += str(row[5].value).upper()+', '
                    continue

            # if str(row[1].value).upper() == 'PERMOHONAN AKSES INTERNET':
            #    jns = 'AI'
            # else:
            #    jns = 'BTS'
            # try:
            # if str(row[3].value)[0:3].upper() == 'KAB':
            #    #LokasiSurvey_ = LokasiSurvey.objects.get(provinsi=ObjectId(data_provinsi["id"]), kabupaten=ObjectId(kabupaten_["id"]),
                #                                         kecamatan=ObjectId(data_kecamatan["id"]), desa=ObjectId(data_desa["id"]), jenis=jns)
            # else:
            #    LokasiSurvey_ = LokasiSurvey.objects.get(provinsi=ObjectId(data_provinsi["id"]), kota=ObjectId(kota_["id"]),
            #                                                kecamatan=ObjectId(data_kecamatan["id"]), desa=ObjectId(data_desa["id"]), jenis=jns)
                # return Response.badRequest(
                #    values='null',
                #    message='Data exists'
                # )
            # except LokasiSurvey.DoesNotExist:
            status = {'status': 'created', 'date': datetime.utcnow(
            ) + timedelta(hours=7)}
            LokasiSurvey_ = LokasiSurvey.objects.filter(latitude=str(
                row[6].value).upper(), longitude=str(row[7].value).upper())
            if len(LokasiSurvey_) == 0:
                LokasiSurvey_ = LokasiSurvey()
                #LokasiSurvey_.user = ObjectId("5f1aa3f07c33fe56ba294923")
                LokasiSurvey_.provinsi = ObjectId(data_provinsi["id"])
                try:
                    LokasiSurvey_.kabupaten = ObjectId(kabupaten_["id"])
                except:
                    LokasiSurvey_.kota = ObjectId(kota_["id"])
                LokasiSurvey_.kecamatan = ObjectId(data_kecamatan["id"])
                LokasiSurvey_.desa = ObjectId(data_desa["id"])
                LokasiSurvey_.jenis = jns
                LokasiSurvey_.latitude = str(row[6].value).upper()
                LokasiSurvey_.longitude = str(row[7].value).upper()
                LokasiSurvey_.status.append(status)

                LokasiSurvey_.save()
            else:
                lokasi_gagal += str(row[5].value).upper()+', '
                # return Response.badRequest(
                #    values=[str(row[5].value).upper()],
                #    message=lokasi_gagal
                # )

        # return Response.ok(
        #    values=[],
        #    message='Upload berhasil'
        # )
        if lokasi_gagal == 'Lokasi gagal : ':
            return Response.ok(
                values=[],
                message=''
            )
        else:
            return Response.ok(
                values=[],
                message=lokasi_gagal
            )
        #    return JsonResponse({"state": "success"})
        # return JsonResponse({"state": "success","gagal": lokasi_gagal})


def uploadsite(request):
    if request.method == 'POST':
        import openpyxl
        lokasi_gagal = ''
        body_data = request.POST.dict()

        judul = body_data.get('judul')
        tanggal_mulai_undangan = datetime.strptime(body_data.get('tanggal_mulai_undangan'), '%Y-%m-%d 00:00:00')
        tanggal_selesai_undangan = datetime.strptime(body_data.get('tanggal_selesai_undangan'), '%Y-%m-%d 23:59:59')
        if tanggal_selesai_undangan < tanggal_mulai_undangan:
            return Response.badRequest(
                values='null',
                message='tanggal_selesai_undangan harus lebih besar dari tanggal_mulai_undangan'
            )

        tanggal_mulai_kerja = datetime.strptime(body_data.get('tanggal_mulai_kerja'), '%Y-%m-%d 00:00:00')
        if tanggal_mulai_kerja < tanggal_selesai_undangan:
            return Response.badRequest(
                values='null',
                message='tanggal_mulai_kerja harus lebih besar dari tanggal_selesai_undangan'
            )
        tanggal_selesai_kerja = datetime.strptime(body_data.get('tanggal_selesai_kerja'), '%Y-%m-%d 23:59:59')
        if tanggal_selesai_kerja < tanggal_mulai_kerja:
            return Response.badRequest(
                values='null',
                message='tanggal_selesai_kerja harus lebih besar dari tanggal_mulai_kerja'
            )
        rfi = body_data.get('rfi')
        type = body_data.get('type')
        creator = body_data.get('creator')
        #penyedia_undang = body_data.get('penyedia_undang')

        status_ = {'status': 'Dibuka', 'tanggal_pembuatan': datetime.utcnow(
                ) + timedelta(hours=7)}

        try:
            #data_nomor_batch = batch.objects.latest('nomor')
            data_nomor_batch = batch.objects.order_by('-nomor').first()
            nomor_batch = int(data_nomor_batch.nomor) + 1
            nomor_batch = str(nomor_batch).zfill(5)
        #except:
        except Exception as e:
            print(e)
            nomor_batch = '1'.zfill(5)

        data_batch = batch(
            nomor = nomor_batch,
            judul = judul,
            type = type,
            sites = [],
            creator = creator,
            rfi_no = rfi,
            tanggal_mulai_undangan = tanggal_mulai_undangan,
            tanggal_selesai_undangan = tanggal_selesai_undangan,
            tanggal_mulai_kerja = tanggal_mulai_kerja,
            tanggal_selesai_kerja = tanggal_selesai_kerja,
            #penyedia_undang = penyedia_undang.split(","),
            created_at = datetime.utcnow() + timedelta(hours=7),
            updated_at = datetime.utcnow() + timedelta(hours=7)
        )
        data_batch.status.append(status_)
        data_batch.save()

        req_fields = ['latitude', 'longitude','kecamatan']
        data_site_lok = site_location.objects.all().only(*req_fields)
        radius = 1.00 # in kilometer

        new_data_site_lok = []
        excel_file = request.FILES["excel_file"]

        # you may put validations here to check extension or file size

        wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets
        worksheet = wb["List Lokasi Survey"]

        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row

        for row in worksheet.iter_rows():
            lanjut=True
            if str(row[1].value) == 'None':
                break
            if str(row[0].value) == 'NO':
                continue
            data_provinsi = provinsi.objects.filter(
                name=str(row[2].value).upper()).first()
            if data_provinsi is None:
                data_provinsi = provinsi(
                    name=str(row[2].value).upper()
                )
                data_provinsi.save()

            if str(row[3].value)[0:3].upper() == 'KAB':
                kabupaten_ = kabupaten.objects.filter(
                    name=str(row[3].value).upper()).first()
                if kabupaten_ is None:
                    kabupaten_ = kabupaten(
                        name=str(row[3].value).upper(),
                        provinsi=ObjectId(data_provinsi.id)
                    )
                    kabupaten_.save()
            else:
                kota_ = kota.objects.filter(
                    name=str(row[3].value).upper()).first()
                if kota_ is None:
                    kota_ = kota(
                        name=str(row[3].value).upper(),
                        provinsi=ObjectId(data_provinsi.id)
                    )
                    kota_.save()
            data_kecamatan = kecamatan.objects.filter(
                name=str(row[4].value).upper()).first()
            if data_kecamatan is None:
                try:
                    data_kecamatan = kecamatan(
                        name=str(row[4].value).upper(),
                        kabupaten=ObjectId(kabupaten_.id)
                    )
                    data_kecamatan.save()
                except:
                    data_kecamatan = kecamatan(
                        name=str(row[4].value).upper(),
                        kota=ObjectId(kota_.id)
                    )
                    data_kecamatan.save()
            data_desa = desa.objects.filter(
                name=str(row[5].value).upper()).first()
            if data_desa is None:
                data_desa = desa(
                    name=str(row[5].value).upper(),
                    kecamatan=ObjectId(data_kecamatan.id)
                )
                data_desa.save()
            if str(row[1].value).upper() == 'PERMOHONAN AKSES INTERNET':
                jns = 'AI'
            else:
                jns = 'AI'

            for dat in data_site_lok:
                if dat.kecamatan.id != data_kecamatan.id:
                    continue
                
                a = haversine(float(dat.longitude), float(dat.latitude), float(str(row[7].value)), float(str(row[6].value)))
                #print(a)
                if a <= radius:
                    lanjut=False
                    break
            if lanjut: 
                data_site = site_location(
                    latitude = str(row[6].value),
                    longitude = str(row[7].value),
                    nama = str(row[8].value),
                    desa = data_desa.id,
                    kecamatan = data_kecamatan.id,
                    provinsi = data_provinsi.id,
                    kode_pos = str(row[9].value),
                    created_at = datetime.utcnow() + timedelta(hours=7),
                    updated_at = datetime.utcnow() + timedelta(hours=7)
                )
                if str(row[3].value)[0:3].upper() == 'KAB':                 
                    data_site.kabupaten = kabupaten_.id
                else:
                    data_site.kota = kota_.id
                data_site.save()

                data_batch.sites.append(ObjectId(data_site.id))
                data_batch.save()
            else:
                lokasi_gagal += '{'+str(row[6].value)+', '+str(row[7].value)+'}, '

        return Response.ok(
            values=[],
            message=lokasi_gagal
        )


def addbatch(request):
    # token = request.META.get("HTTP_AUTHORIZATION").replace(" ", "")[6:]
    # ret, user = authenticate_credentials(token)
    # if False == ret or None == user:
    #    return JsonResponse({"state": "fail"})
    if request.method == "POST":  # Add
        try:
            #file = request.FILES['doc']
            #if not file:
            #    return Response.badRequest(message='No File Upload')

            body_data = request.POST.dict()

            judul = body_data.get('judul')
            tanggal_mulai_undangan = body_data.get('tanggal_mulai_undangan')
            tanggal_selesai_undangan = body_data.get('tanggal_selesai_undangan')
            if tanggal_selesai_undangan < tanggal_mulai_undangan:
                return Response.badRequest(
                    values='null',
                    message='tanggal_selesai_undangan harus lebih besar dari tanggal_mulai_undangan'
                )

            tanggal_mulai_kerja = body_data.get('tanggal_mulai_kerja')
            if tanggal_mulai_kerja < tanggal_selesai_undangan:
                return Response.badRequest(
                    values='null',
                    message='tanggal_mulai_kerja harus lebih besar dari tanggal_selesai_undangan'
                )
            tanggal_selesai_kerja = body_data.get('tanggal_selesai_kerja')
            if tanggal_selesai_kerja < tanggal_mulai_kerja:
                return Response.badRequest(
                    values='null',
                    message='tanggal_selesai_kerja harus lebih besar dari tanggal_mulai_kerja'
                )
            rfi = body_data.get('rfi')
            type = body_data.get('type')
            creator = body_data.get('creator')
            penyedia_undang = body_data.get('penyedia_undang')

            status_ = {'status': 'Dibuka', 'tanggal_pembuatan': datetime.utcnow(
                    ) + timedelta(hours=7)}

            try:
                #data_nomor_batch = batch.objects.latest('nomor')
                data_nomor_batch = batch.objects.order_by('-nomor').first()
                nomor_batch = int(data_nomor_batch.nomor) + 1
                nomor_batch = str(nomor_batch).zfill(5)
            #except:
            except Exception as e:
                print(e)
                nomor_batch = '1'.zfill(5)

            vendor_list = penyedia_undang.split(",")
            data_batch = batch(
                nomor = nomor_batch,
                judul = judul,
                type = type,
                sites = [],
                creator = creator,
                rfi_no = rfi,
                tanggal_mulai_undangan = tanggal_mulai_undangan,
                tanggal_selesai_undangan = tanggal_selesai_undangan,
                tanggal_mulai_kerja = tanggal_mulai_kerja,
                tanggal_selesai_kerja = tanggal_selesai_kerja,
                penyedia_undang = vendor_list,
                created_at = datetime.utcnow() + timedelta(hours=7),
                updated_at = datetime.utcnow() + timedelta(hours=7)
            )
            data_batch.status.append(status_)
            data_batch.save()
            
            for vn in vendor_list:
                try:
                    comp = company.objects.get(id=ObjectId(vn))
                except company.DoesNotExist:
                    return Response.ok(
                        values=[],
                        message='Penyedia tidak ada'
                    )
                data_batch_vendor = batch_vendor(
                    vendor = comp.id,
                    batch_id = data_batch.id,
                    created_at = datetime.utcnow() + timedelta(hours=7),
                    updated_at = datetime.utcnow() + timedelta(hours=7)
                )
                data_batch_vendor.status.append(status_)
                data_batch_vendor.save()
            #results = batch.objects.get(id=ObjectId(data_batch.id))
            serializer = BatchSerializer(data_batch)
            result = serializer.data
            
            return Response.ok(
                values=result,
                message='Berhasil'
            )
        except Exception as e:
            return Response.badRequest(message=str(e))

    else:
        return Response.badRequest(message='Hanya POST')


def addsite(request):
    # token = request.META.get("HTTP_AUTHORIZATION").replace(" ", "")[6:]
    # ret, user = authenticate_credentials(token)
    # if False == ret or None == user:
    #    return JsonResponse({"state": "fail"})
    if request.method == "POST":  # Add
        try:
            body_data = json.loads(request.body)

            batch_id = body_data.get('batch')
            nama = body_data.get('nama')
            provinsi = body_data.get('provinsi')
            kab_kota = body_data.get('kab_kota')
            kecamatan = body_data.get('kecamatan')
            desa = body_data.get('desa')
            longitude = body_data.get('longitude')
            latitude = body_data.get('latitude')
            kode_pos = body_data.get('kode_pos')

            #try:
            #data_site_lok = site_location.objects.filter(latitude=latitude, longitude=longitude)
            #data_site_lok = site_location.objects.all()
            #if len(data_site_lok)==0:
            #    return Response.badRequest(message='Data sudah ada')
            #except site_location.DoesNotExist:
            #    return Response.badRequest(message='Data sudah ada')
            req_fields = ['latitude', 'longitude','kecamatan']
            data_site_lok = site_location.objects.all().only(*req_fields)
            radius = 1.00 # in kilometer
            
            for dat in data_site_lok:
                if dat.kecamatan.id != ObjectId(kecamatan):
                    continue
                a = haversine(float(dat.longitude), float(dat.latitude), float(longitude), float(latitude))
                #print(a)
                if a <= radius:
                    return Response.ok(
                        values=[],
                        message='Data sudah ada'
                    )

            try:
                data_kabupaten = kabupaten.objects.get(id=kab_kota)
                data_kab_kota = 'kab'
            except kabupaten.DoesNotExist:
                data_kabupaten = kota.objects.get(id=kab_kota)
                data_kab_kota = 'kota'
            
            data_site = site_location(
                latitude = latitude,
                longitude = longitude,
                nama = nama,
                desa = ObjectId(desa),
                kecamatan = ObjectId(kecamatan),
                provinsi = ObjectId(provinsi),
                kode_pos = kode_pos,
                created_at = datetime.utcnow() + timedelta(hours=7),
                updated_at = datetime.utcnow() + timedelta(hours=7)
            )
            if data_kab_kota == 'kab':
                data_site.kabupaten = data_kabupaten.id
            else:
                data_site.kota = data_kabupaten.id
            data_site.save()

            try:
                data_batch = batch.objects.get(id=ObjectId(batch_id))
                data_batch.sites.append(ObjectId(data_site.id))
                data_batch.save()

                for vn in data_batch.penyedia_undang:
                    try:
                        comp = company.objects.get(id=vn.id)
                    except company.DoesNotExist:
                        return Response.ok(
                            values=[],
                            message='Penyedia tidak ada'
                        )
                    data_site_vendor = site_vendor(
                        vendor = comp.id,
                        batch_id = data_batch.id,
                        site_id = ObjectId(data_site.id),
                        created_at = datetime.utcnow() + timedelta(hours=7),
                        updated_at = datetime.utcnow() + timedelta(hours=7)
                    )
                    data_site_vendor.save()
            except batch.DoesNotExist:
                return Response.badRequest(message='Batch tidak ada')
            results = site_location.objects.get(id=ObjectId(data_site.id))
            
            result = results.serialize()
            
            return Response.ok(
                values=result,
                message='Berhasil'
            )
        except Exception as e:
            return Response.badRequest(message=str(e))

    else:
        return Response.badRequest(message='Hanya POST')

def editbatch(request):
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

        batch_id = body_data.get('batch')
        tanggal_mulai_undangan = body_data.get('tanggal_mulai_undangan')
        tanggal_selesai_undangan = body_data.get('tanggal_selesai_undangan')
        status_ = body_data.get('status')

        if status_=='Selesai':
            return Response.ok(
                values=[],
                message='Status sudah selesai'
            )
        
        try:
            data_batch = batch.objects.get(id=ObjectId(batch_id))
        except batch.DoesNotExist:
            return Response.ok(message='Batch tidak ada')

        data_batch.tanggal_mulai_undangan = tanggal_mulai_undangan
        data_batch.tanggal_selesai_undangan = tanggal_selesai_undangan
        if status_=='Dibuka':
            status__ = {'status': status_, 'tanggal_pembuatan': datetime.utcnow(
                    ) + timedelta(hours=7)}

            data_batch.status.clear()
            data_batch.status.append(status__)
        else:
            status_buka = {'status': 'Dibuka', 'tanggal_pembuatan': datetime.utcnow(
                    ) + timedelta(hours=7)}

            data_batch.status.clear()
            data_batch.status.append(status_buka)
            status_tunda = {'status': status_, 'tanggal_pembuatan': datetime.utcnow(
                    ) + timedelta(hours=7)}
            data_batch.status.append(status_tunda)
        data_batch.save()

        filename = fs.save(file.name, file)
        file_path = fs.url(filename)
        doc = document_batch(
            name=file.name,
            path=file_path,
            create_date=datetime.utcnow() + timedelta(hours=7),
            update_date=datetime.utcnow() + timedelta(hours=7)
        )
        doc.save()

        data_batch.rfi_doc = ObjectId(doc.id)
        data_batch.updated_at = datetime.utcnow() + timedelta(hours=7)
        data_batch.save()

        result = batch.objects.get(id=ObjectId(data_batch.id)).serialize()
        #result = data_batch.serialize()
        
        #serializer = BatchSerializer(result,many=True)
        #result = serializer.data
        
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
    batch_id = body_data.get('batch')

    page = int(body_data.get('page', 0)) - 1
    skip = []
    if page >= 0:
        skip = [{'$skip': 20 * page},
                {'$limit': 20}]

    pipeline = [
        {
            '$match': {
                '_id': ObjectId(batch_id)
            }
        }, 
        {
            '$lookup': {
                'from': 'site_location', 
                'localField': 'sites', 
                'foreignField': '_id', 
                'as': 'sitelist'
            }
        }#, {
        #    '$unwind': {
        #        'path': '$sitelist', 
        #        'preserveNullAndEmptyArrays': True
        #    }
        #}
    ]

    pipe = pipeline + skip
    agg_cursor = batch.objects.aggregate(*pipe)

    batch_list = list(agg_cursor)

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

def getallbatch(request):
    # token = request.META.get("HTTP_AUTHORIZATION").replace(" ", "")[6:]
    # ret, user = authenticate_credentials(token)
    # if False == ret or None == user:
    #    return JsonResponse({"state": "fail"})
    #body_data = json.loads(request.body)
    #batch_id = body_data.get('batch')

    #page = int(body_data.get('page', 0)) - 1
    #skip = []
    #if page >= 0:
    #    skip = [{'$skip': 20 * page},
    #            {'$limit': 20}]

    pipeline = [
        #{
        #    '$match': {
        #        '_id': ObjectId(batch_id)
        #    }
        #}, 
        {
            '$lookup': {
                'from': 'site_location', 
                'localField': 'sites', 
                'foreignField': '_id', 
                'as': 'sitelist'
            }
        }#, {
        #    '$unwind': {
        #        'path': '$sitelist', 
        #        'preserveNullAndEmptyArrays': True
        #    }
        #}
    ]

    pipe = pipeline #+ skip
    agg_cursor = batch.objects.aggregate(*pipe)

    batch_list = list(agg_cursor)

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