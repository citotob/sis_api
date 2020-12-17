from django.shortcuts import render

from datetime import datetime
import requests
import json

from .customResponse import CustomResponse
from rest_framework_mongoengine.viewsets import GenericAPIView, ModelViewSet
from rest_framework import status

from sklearn.preprocessing import minmax_scale

class publicServiceAPI(ModelViewSet):
    def clusterpenduduk(self, request, format=None):
        #try:
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
                    'potensi': 'high'
                })
            elif scaler[i] <= 2/3:
                #cluster['mid'].append({
                #    'provinsi': result[i][k],
                #    'jumlah_penduduk': result[i][v]
                #})
                cluster.append({
                    'provinsi': result[i][k],
                    'jumlah_penduduk': result[i][v],
                    'potensi': 'mid'
                })
            else:
                #cluster['low'].append({
                #    'provinsi': result[i][k],
                #    'jumlah_penduduk': result[i][v]
                #})
                cluster.append({
                    'provinsi': result[i][k],
                    'jumlah_penduduk': result[i][v],
                    'potensi': 'low'
                })
        """
        data_user = UserInfo.objects.filter(role='5f73fdfc28751d590d835266', status='Aktif')
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
        """
        return CustomResponse.ok(values=cluster)
        #except TypeError as e:
        #    return CustomResponse().base(success=False, message=str(e), status=status.HTTP_404_NOT_FOUND)
        #except Exception as e:
        #    return CustomResponse().base(success=False, message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def getDashboard(request):
        try:
            vendorCount = vendor.objects.all().count()
            activeUserCount = UserInfo.objects(status='Aktif').count()
            requestedUserCount = UserInfo.objects(status='Belum Terverifikasi').count()
            batchCount = batch.objects.all().count()
            siteCount = site_matchmaking.objects(batchid__exists=True).count()
            rfiCount = vendor_application.objects.all().count()
            #siteNonBatchCount = 0
            #vendorListQuery = vendor.objects.all()
            #vendorList = VendorScoreSerializer(vendorListQuery, many=True)

            aiCount = Odp.objects.filter(teknologi__in=['VSAT','FO','RL']).count()
            #aiTech = Odp.objects.only('teknologi').distinct('teknologi')
            #aiOperational = {
            #    "count": aiCount,
            #    "FO": 0,
            #    "VSAT": 0,
            #    "RL": 0
            #}
            #for x in list(aiTech):
            #    xx=x
            #    aiOperational.update({
            #        xx: Odp.objects(teknologi=x).count()
            #    })

            #recommendTech = rekomendasi_teknologi.objects.only(
            #    'teknologi').distinct('teknologi')
            #siteAICount = site.objects.all().count()
            #aiNew = {
            #    "count": siteAICount,
            #    "FO": 0,
            #    "VSAT": 0,
            #    "RL": 0
            #}
            #for x in list(recommendTech):
            #    query = rekomendasi_teknologi.objects(teknologi=x).scalar('id')
            #    aiNew.update({
            #        x: site.objects(rekomendasi_teknologi__in=query).count()
            #    })

            date = datetime.now()
            listMonth = calendar.month_abbr[1:13]
            #reportSite = {}
            #reportRFi = {}
            #for x in range(11, -1, -1):
            #    dateReport = date - relativedelta(months=x)
            #    year = dateReport.year
            #    month = dateReport.month
            #    lastDate = calendar.monthrange(year=year, month=month)[1]
            #    gte = datetime(year, month, 1, 00, 00, 00)
            #    lte = datetime(year, month, lastDate, 23, 59, 59)
            #    reportSite.update({
            #        f'{listMonth[month-1]} {year}': batch.objects(created_at__gte=gte, created_at__lte=lte).count()
            #    })
            #    reportRFi.update({
            #        f'{listMonth[month-1]} {year}': vendor_application.objects(created_at__gte=gte, created_at__lte=lte).count()
            #    })

            result = {
                "vendor": vendorCount,
                "active_user": activeUserCount,
                "requested_user": requestedUserCount,
                "batch": batchCount,
                "site": siteCount,
                "rfi": rfiCount,
                #"site_not_batch": siteNonBatchCount,
                #"vendor_list": json.loads(json.dumps(vendorList.data, default=str)),
                #"running_ai": aiOperational,
                #"new_ai": aiNew,
                #"report": {
                #    "site": reportSite,
                #    "rfi": reportRFi
                #}
            }

            return Response.ok(
                values=result
            )

        except Exception as e:
            return Response.badRequest(
                values=[],
                message=str(e)
            )

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
                                'lastStatus': {
                                    '$arrayElemAt': [
                                        '$status', 0
                                    ]
                                }
                            }
                        }, {
                            '$match': {
                                'lastStatus.tanggal_pembuatan': {
                                    '$gte': datetime(year, month, 1, 00, 00, 00, tzinfo=timezone.utc),
                                    '$lte': datetime(year, month, lastDay, 23, 59, 59, tzinfo=timezone.utc)
                                },
                                'nomorSurvey': '1'
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
                                #'status.status': status,
                            }
                        }, {
                            '$count': 'count'
                        }
                    ]

                def getPenugasanAISurvey():
                    hasil_survey = hasilSurvey.objects.filter(
                        status__status="Submitted", nomorSurvey='1').count()
                    return hasil_survey

                def getPenugasanBTSSurvey():
                    hasil_survey = hasilSurveybts.objects.filter(
                        status__status="Submitted", nomorSurvey='1').count()
                    return hasil_survey

                def getBTSSurvey(month, year):
                    lastDay = calendar.monthrange(year=year, month=month)[1]
                    from_ = datetime(year, month, 1, 00, 00, 00, tzinfo=timezone.utc)
                    to_ = datetime(year, month, lastDay, 23, 59, 59, tzinfo=timezone.utc)
                    hasil_survey = hasilSurveybts.objects.filter(status__status="Submitted", status__0__tanggal_pembuatan__gte=from_,
                                                        status__0__tanggal_pembuatan__lte=to_, nomorSurvey='1').count()
                    return hasil_survey

                penugasanAITotal = list(
                    Penugasan.objects.aggregate(pipelineTotal(jenis=ai, status='assigned')))[0]['count']
                penugasanBTSTotal = list(
                    Penugasan.objects.aggregate(pipelineTotal(jenis=bts, status='assigned')))[0]['count']

                penugasanAITotalFinish = getPenugasanAISurvey()
                penugasanBTSTotalFinish = getPenugasanBTSSurvey()

                penugasanPersentaseAI = (
                    penugasanAITotalFinish/penugasanAITotal) * 100
                penugasanPersentaseBTS = (
                    penugasanBTSTotalFinish / penugasanBTSTotal) * 100

                penugasanAISekarangList = list(
                    hasilSurvey.objects.aggregate(pipelineDate(jenis=ai, month=month, year=year)))
                penugasanBTSSekarangList = getBTSSurvey(month=month, year=year)
                
                penugasanAISebelumnyaList = list(
                    hasilSurvey.objects.aggregate(pipelineDate(jenis=ai, month=pastMonth, year=pastYear)))
                penugasanBTSSebelumnyaList = getBTSSurvey(month=pastMonth, year=pastYear)
                
                penugasanAISekarang = 0 if len(
                    penugasanAISekarangList) == 0 else penugasanAISekarangList[0]['count']

                penugasanBTSSekarang = 0 if penugasanBTSSekarangList == 0 else penugasanBTSSekarangList

                penugasanAISebelumnya = 0 if len(
                    penugasanAISebelumnyaList) == 0 else penugasanAISebelumnyaList[0]['count']
                penugasanBTSSebelumnya = 0 if penugasanBTSSebelumnyaList == 0 else penugasanBTSSebelumnyaList
                
                #persentasiKenaikanAI = ((
                #    abs(penugasanAISekarang - penugasanAISebelumnya)) / penugasanAISebelumnya) * 100 if penugasanAISebelumnya > 0 else 0
                persentasiKenaikanAI = ( penugasanAISekarang / penugasanAITotal) * 100 if penugasanAITotal > 0 else 0
                #persentasiKenaikanBTS = ((
                #    abs(penugasanBTSSekarang - penugasanBTSSebelumnya)) / penugasanBTSSebelumnya) * 100 if penugasanBTSSebelumnya > 0 else 0
                persentasiKenaikanBTS = ( penugasanBTSSekarang / penugasanBTSTotal) * 100 if penugasanBTSTotal > 0 else 0

                #try:
                subject = f'Monthly Report SMASLAB {bulan[month-1]} {year}'
                text_content = ''
                htmly = get_template('email/executive/executive.html')
                
                d = {
                    'bulan': f'{bulan[month-1]} {year}',

                    'ai_finish': penugasanAITotalFinish,
                    'ai_total': penugasanAITotal,

                    'bts_finish': penugasanBTSTotalFinish,
                    'bts_total': penugasanBTSTotal,

                    'ai_persentase': round(penugasanPersentaseAI, 2),
                    'ai_penambahan': round(persentasiKenaikanAI, 2),
                    'ai_bulan': penugasanAISekarang,

                    'bts_persentase': round(penugasanPersentaseBTS, 2),
                    'bts_penambahan': round(persentasiKenaikanBTS, 2),
                    'bts_bulan': penugasanBTSSekarang,

                    #'ai_perubahan': 'Kenaikan' if penugasanAISekarang > penugasanAISebelumnya else 'Penurunan' if penugasanAISekarang < penugasanAISebelumnya else 'Tidak ada Perubahan',
                    'ai_perubahan': 'Terdapat Kenaikan' if persentasiKenaikanAI > 0 else 'Tidak ada penambahan',
                    #'ai_persentase_penambahan': f'{round(persentasiKenaikanAI, 2)}%' if penugasanAISekarang != penugasanAISebelumnya else '',
                    'ai_persentase_penambahan': f'{round(persentasiKenaikanAI, 2)}%' if persentasiKenaikanAI > 0 else '',

                    #'bts_perubahan': 'Kenaikan' if penugasanBTSSekarang > penugasanBTSSebelumnya else 'Penurunan' if penugasanBTSSekarang < penugasanBTSSebelumnya else 'Tidak ada Perubahan',
                    #'bts_persentase_penambahan': f'{round(persentasiKenaikanBTS, 2)}%' if penugasanBTSSekarang != penugasanBTSSebelumnya else '',
                    'bts_perubahan': 'Terdapat Kenaikan' if persentasiKenaikanBTS > 0 else 'Tidak ada penambahan',
                    'bts_persentase_penambahan': f'{round(persentasiKenaikanBTS, 2)}%' if persentasiKenaikanBTS > 0 else '',

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
                #print('asdad', response)
                #except:
                #    pass

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
