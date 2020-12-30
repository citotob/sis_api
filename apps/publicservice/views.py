from django.shortcuts import render
from django.db.models import Count

from datetime import datetime
import requests
import json

from .customResponse import CustomResponse
from rest_framework_mongoengine.viewsets import GenericAPIView, ModelViewSet
from rest_framework import status

from sklearn.preprocessing import minmax_scale

from odps.models import *
#from .serializer import *
from django.conf import settings

from .utils import send_mail
from userinfo.models import UserInfo
from sites.models import *

class publicServiceAPI(ModelViewSet):
    def clusterpenduduk(self, request, format=None):
        try:
            url = "https://www.bps.go.id/indikator/indikator/download_json/0000/api_pub/50/da_03/1"
            headers = {'Content-type': 'application/json'}
            #d = {"month":month, "year":year}
            res = requests.get(url).json()#, data=json.dumps(d)

            result = []
            dt_penduduk = []
            #print(max(res['data']))
            for dt in res['data']:
                if dt['label']!='Indonesia':
                    json_dict = {}
                    json_dict['provinsi'] = dt['label']
                    json_dict['jumlah_penduduk'] = float(dt['penduduk_jumlah_penduduk'].replace(' ','').replace(',','.'))
                    result.append(json_dict)
                    dt_penduduk.append(float(dt['penduduk_jumlah_penduduk'].replace(' ','').replace(',','.')))

            max_ = max(dt_penduduk)
            min_ = min(dt_penduduk)
            scaler = minmax_scale(dt_penduduk)
            #cluster = {
            #    'low': [],
            #    'mid': [],
            #    'high': [],
            #}
            cluster = []
            for i, (k, v) in enumerate(result):
            #for dt in result:
                #print(scaler[i])
                if scaler[i] <= 1/3:
                    #cluster['high'].append({
                    #    'provinsi': result[i][k],
                    #    'jumlah_penduduk': result[i][v]
                    #})
                    cluster.append({
                        'provinsi': result[i][k],
                        'jumlah_penduduk': result[i][v],
                        'potensi': 'high',
                        'nilai': scaler[i]
                    })
                elif scaler[i] <= 2/3:
                    #cluster['mid'].append({
                    #    'provinsi': result[i][k],
                    #    'jumlah_penduduk': result[i][v]
                    #})
                    cluster.append({
                        'provinsi': result[i][k],
                        'jumlah_penduduk': result[i][v],
                        'potensi': 'mid',
                        'nilai': scaler[i]
                    })
                else:
                    #cluster['low'].append({
                    #    'provinsi': result[i][k],
                    #    'jumlah_penduduk': result[i][v]
                    #})
                    cluster.append({
                        'provinsi': result[i][k],
                        'jumlah_penduduk': result[i][v],
                        'potensi': 'low',
                        'nilai': scaler[i]
                    })
            return CustomResponse.ok(values=cluster)
        except TypeError as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def clusteraionair(self, request, format=None):
        try:
            data_odp = Odp.objects.aggregate([
                {'$group' : {'_id':"$provinsi", 'total':{'$sum':1}}}
            ])
            result = []
            dt_odp = []
            
            for dt in list(data_odp):
                json_dict = {}
                json_dict['provinsi'] = dt['_id']
                json_dict['total'] = dt['total']
                result.append(json_dict)
                dt_odp.append(dt['total'])

            scaler = minmax_scale(dt_odp)
            cluster = []
            for i, (k, v) in enumerate(result):
                if scaler[i] <= 1/3:
                    cluster.append({
                        'provinsi': result[i][k],
                        'total': result[i][v],
                        'potensi': 'high',
                        'nilai': scaler[i]
                    })
                elif scaler[i] <= 2/3:
                    cluster.append({
                        'provinsi': result[i][k],
                        'total': result[i][v],
                        'potensi': 'mid',
                        'nilai': scaler[i]
                    })
                else:
                    cluster.append({
                        'provinsi': result[i][k],
                        'total': result[i][v],
                        'potensi': 'low',
                        'nilai': scaler[i]
                    })
            return CustomResponse.ok(values=cluster)
        except TypeError as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def clusterbtsonair(self, request, format=None):
        try:
            data_bts = bts_onair.objects.aggregate([
                {'$group' : {'_id':"$provinsi_name", 'total':{'$sum':1}}}
            ])
            result = []
            dt_bts = []
            
            for dt in list(data_bts):
                json_dict = {}
                json_dict['provinsi'] = dt['_id']
                json_dict['total'] = dt['total']
                result.append(json_dict)
                dt_bts.append(dt['total'])

            scaler = minmax_scale(dt_bts)
            cluster = []
            for i, (k, v) in enumerate(result):
                if scaler[i] <= 1/3:
                    cluster.append({
                        'provinsi': result[i][k],
                        'total': result[i][v],
                        'potensi': 'high',
                        'nilai': scaler[i]
                    })
                elif scaler[i] <= 2/3:
                    cluster.append({
                        'provinsi': result[i][k],
                        'total': result[i][v],
                        'potensi': 'mid',
                        'nilai': scaler[i]
                    })
                else:
                    cluster.append({
                        'provinsi': result[i][k],
                        'total': result[i][v],
                        'potensi': 'low',
                        'nilai': scaler[i]
                    })
            return CustomResponse.ok(values=cluster)
        except TypeError as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def getLaporan(self, request, format=None):
        try:
            #bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
            #        "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
            
            #req = request.body.decode("utf-8")
            #data = json.loads(req)
            #month = data['month']
            #year = data['year']

            #pastMonth = data['month'] - 1
            #pastYear = year

            #if pastMonth == 0:
            #    pastMonth = 12
            #    pastYear = year-1

            #if month is None or year is None:
            #    return CustomResponse.ok(message='Need Json Body "month" & "year"')

            vendorCount = vendor.objects.all().count()
            activeUserCount = UserInfo.objects(status='Aktif').count()
            requestedUserCount = UserInfo.objects(status='Belum Terverifikasi').count()
            batchCount = batch.objects.all().count()
            siteCount = site_matchmaking.objects(batchid__exists=True).count()
            rfiCount = vendor_application.objects.all().count()
            """
            siteNonBatchCount = 0
            vendorListQuery = vendor.objects.all()
            vendorList = VendorScoreSerializer(vendorListQuery, many=True)

            aiCount = Odp.objects.filter(teknologi__in=['VSAT','FO','RL']).count()
            aiTech = Odp.objects.only('teknologi').distinct('teknologi')
            aiOperational = {
                "count": aiCount,
                "FO": 0,
                "VSAT": 0,
                "RL": 0
            }
            
            for x in list(aiTech):
                xx=x
                aiOperational.update({
                    xx: Odp.objects(teknologi=x).count()
                })

            recommendTech = rekomendasi_teknologi.objects.only(
                'teknologi').distinct('teknologi')
            siteAICount = site.objects.all().count()
            aiNew = {
                "count": siteAICount,
                "FO": 0,
                "VSAT": 0,
                "RL": 0
            }
            for x in list(recommendTech):
                query = rekomendasi_teknologi.objects(teknologi=x).scalar('id')
                aiNew.update({
                    x: site.objects(rekomendasi_teknologi__in=query).count()
                })

            date = datetime.now()
            listMonth = calendar.month_abbr[1:13]
            reportSite = {}
            reportRFi = {}
            for x in range(11, -1, -1):
                dateReport = date - relativedelta(months=x)
                year = dateReport.year
                month = dateReport.month
                lastDate = calendar.monthrange(year=year, month=month)[1]
                gte = datetime(year, month, 1, 00, 00, 00)
                lte = datetime(year, month, lastDate, 23, 59, 59)
                reportSite.update({
                    f'{listMonth[month-1]} {year}': batch.objects(created_at__gte=gte, created_at__lte=lte).count()
                })
                reportRFi.update({
                    f'{listMonth[month-1]} {year}': vendor_application.objects(created_at__gte=gte, created_at__lte=lte).count()
                })
            
            result = {
                "vendor": vendorCount,
                "active_user": activeUserCount,
                "requested_user": requestedUserCount,
                "batch": batchCount,
                "site": siteCount,
                "rfi": rfiCount,
                "site_not_batch": siteNonBatchCount,
                "vendor_list": json.loads(json.dumps(vendorList.data, default=str)),
                "running_ai": aiOperational,
                "new_ai": aiNew,
                "report": {
                    "site": reportSite,
                    "rfi": reportRFi
                }
            }
            """
            executive = [x.email for x in UserInfo.objects.filter(
                role=ObjectId('5f73fe3428751d590d835267'))]

            subject = 'Laporan'
            text_content = ''
            template = 'email/executive/EmailLaporan.html'
            d = { 
                    'media_url': settings.URL_MEDIA,
                    'url_login': settings.URL_LOGIN,
                    'vendorCount': vendorCount,
                    'activeUserCount': activeUserCount,
                    'requestedUserCount': requestedUserCount,
                    'batchCount': batchCount,
                    'siteCount': siteCount,
                    'rfiCount': rfiCount
                }
            email_sender = settings.EMAIL_ADMIN
            email_receipient = executive
            send_mail(subject,text_content,template,d,email_sender,email_receipient)

            return CustomResponse.ok(message='Berhasil')
        except TypeError as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    