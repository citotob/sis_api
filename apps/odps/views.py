from django.shortcuts import render
from odps.models import Odp
from sites.models import kabupaten, kota
from userinfo.models import vendor
from odps.serializer import *
from .response import Response
import json
from operator import itemgetter

from geojson import Feature, Point
from turfpy.measurement import distance, rhumb_distance, boolean_point_in_polygon
from turfpy.transformation import circle

def uploadodp(request):
    if request.method == 'POST':
        import openpyxl
        lokasi_gagal = ''

        odp_file = request.FILES["odp_file"]

        # you may put validations here to check extension or file size

        wb = openpyxl.load_workbook(odp_file)

        # getting a particular sheet by name out of many sheets
        worksheet = wb["Sheet1"]

        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row

        for row in worksheet.iter_rows():
            #data_odp1 = Odp.objects.filter(latitude=str(row[6].value).replace(',','.'),
            #            longitude=str(row[5].value).replace(',','.'))
            #if data_odp1:
            #    continue
            vndr=str(row[7].value)
            if "TELKOM" in vndr:
                vndr = "TELKOM"
            try:
                data_vendor = vendor.objects.get(
                    name__iexact=str(row[7].value))
            except vendor.DoesNotExist:
                data_vendor = vendor(
                    name=str(row[7].value),
                    latitude='0',
                    longitude='0',
                    longlat=[0, 0],
                )
                data_vendor.save()

                #data_VPScore = VPScore(vendor=data_vendor.id)
                #data_VPScore.save()

            lanjut = True
            if str(row[1].value) == 'None':
                break
            if str(row[0].value) == 'NAMA LOKASI':
                continue
            tekno = str(row[9].value)
            if "VSAT" in str(row[9].value):
                tekno = "VSAT"

            try:
                data_odp = Odp(
                    latitude=str(row[6].value).replace(',','.'),
                    longitude=str(row[5].value).replace(',','.'),
                    longlat=[float(str(row[5].value).replace(',','.')), float(str(row[6].value).replace(',','.'))],
                    teknologi=tekno,
                    nama=str(row[0].value),
                    desa_kelurahan=ObjectId(str(row[4].value)),
                    kecamatan=ObjectId(str(row[3].value)),
                    provinsi=ObjectId(str(row[1].value)),
                    vendorid=data_vendor.id,
                )

                try:
                    data_kab_kot = kabupaten.objects.get(id=ObjectId(str(row[2].value)))
                    data_odp.kabupaten = data_kab_kot.id
                except kabupaten.DoesNotExist:
                    try:
                        data_kab_kot = kota.objects.get(id=ObjectId(str(row[2].value)))
                        data_odp.kota = data_kab_kot.id
                    except kota.DoesNotExist:
                        return Response.ok(
                            values=[],
                            message="kabkot " + str(row[2].value) +" tidak ada"
                        )
                
                data_odp.save()
            except:
                continue

        return Response.ok(
            values=[],
            message="OK"
        )

def getRecommendTech(request):

    try:

        if not request.body:
            return Response.badRequest(
                values=[],
                message="Need Json Body longitude & latitude"
            )
        body = json.loads(request.body)
        longitude = body.get('longitude', None)
        latitude = body.get('latitude', None)

        if not (longitude and latitude):
            return Response.badRequest(
                values=[],
                message="Need Json Body longitude & latitude"
            )

        coordinates = [float(longitude), float(latitude)]
        # print(getRecommendTechnologi(longitude, latitude))
        start = Feature(geometry=Point(coordinates=coordinates))
        # data = Odp.objects.aggregate([
        #     {
        #         '$match': {
        #             "longlat": {"$geoWithin":
        #                         {"$center": [[121.2866, 39.984], (116 / 111.32)]}}
        #         }
        #     }
        # ])
        data = Odp.objects(
            longlat__geo_within_sphere=[coordinates, (10 / 6378.1)])
        # data = Odp.objects(
        #     longlat__near=[122.2866, -1.14911], longlat__max_distance=115199)
        # radius = circle(center=end, radius=85, units='km')
        # print(boolean_point_in_polygon(start, radius))
        # print(rhumb_distance(start, end, units='km'))
        # print(distance(start, end, units='km'))
        # print(list(data))

        serializer = ODPSerializer(data, many=True)

        if len(serializer.data) > 0:
            results = []
            datas = serializer.data.copy()
            for x in datas:
                end = Feature(geometry=Point(x["longlat"]["coordinates"]))
                x['distance'] = f'{int(distance(start, end, units="km"))} km'
                results.append(x)
            results.sort(key=itemgetter('distance', 'created_at'))
            return Response.ok(
                values=json.loads(json.dumps(serializer.data, default=str)),
                message=f'{len(serializer.data)} Data'
            )
        else:
            return Response.ok(
                values=[],
                message='Data tidak ada'
            )

    except Exception as e:
        print(e)
        return Response.badRequest(message=str(e))