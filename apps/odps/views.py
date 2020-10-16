from django.shortcuts import render
from odps.models import Odp
from sites.models import kabupaten, kota
from userinfo.models import vendor

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