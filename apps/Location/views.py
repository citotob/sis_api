from django.shortcuts import render
from .models import Provinsi, Kabupaten, Kota, Kecamatan, Desa
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from .serializer import ProvinsiSerializer, KabupatenSerializer, KecamatanKabSerializer, KecamatanKotSerializer, DesaSerializer
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .response import Response


def getAllProvinsi(request):
    try:
        data = Provinsi.objects.all()
        datas = ProvinsiSerializer(data, many=True)
        return Response.ok(
            data=datas.data,
            count=len(datas.data)
        )
    except Exception as e:
        print(e)


def getKabupaten(request):
    try:
        prov = request.GET.get('provinsi', None)
        try:
            provinsi = Provinsi.objects.get(id=prov)
        except Provinsi.DoesNotExist:
            provinsi = None

        if not provinsi:
            #return Response.badRequest(
            #    message='Province Does Not Exist'
            #)
            return Response.base(
                success=False,
                message='Province Does Not Exist',
                status=404
            )
        else:
            data = Kabupaten.objects(provinsi=provinsi.id)
            dataKota = Kota.objects(provinsi=provinsi.id)
            datas = KabupatenSerializer(list(data) + list(dataKota), many=True)
            return Response.ok(
                data=datas.data,
                count=len(datas.data)
            )
    except Exception as e:
        print(e)
        return Response.badRequest(
            message=str(e)
        )


def getKecamatan(request):
    kabkot = request.GET.get('kabupaten_kota', None)
    # kot = request.GET.get('kota', None)

    # try:
    #     if kabkot is not None:
    #         kabupaten = Kabupaten.objects.get(id=kabkot)
    #         kota = None
    #     elif kot is not None:
    #         kota = Kota.objects.get(id=kabkot)
    #         kabupaten = None
    #     else:
    #         return Response.badRequest(
    #             message='Need Parameter `kabupaten` or `kota`'
    #         )
    # except Kabupaten.DoesNotExist:
    #     return Response.badRequest(
    #         message='Kabupaten Does Not Exist'
    #     )
    # except Kota.DoesNotExist:
    #     return Response.badRequest(
    #         message='Kota Does Not Exist'
    #     )
    if kabkot is not None:
        try:
            kabupaten_kota = Kabupaten.objects.get(id=kabkot)
#           kota = None
        except Kabupaten.DoesNotExist:
            try:
                kabupaten_kota = Kota.objects.get(id=kabkot)
            except Kota.DoesNotExist:
                #return Response.badRequest(
                #    message='Kabupaten/Kota Does Not Exist'
                #)
                return Response.base(
                    success=False,
                    message='Province Does Not Exist',
                    status=404
                )
        try:
            data = Kecamatan.objects(kabupaten=kabupaten_kota.id)
            if (len(data) == 0):
                raise EOFError()
        except EOFError:
            data = Kecamatan.objects(kota=kabupaten_kota.id)
        datas = KecamatanKotSerializer(data, many=True)

        return Response.ok(
            data=[{k: v for k, v in x.items() if v}for x in datas.data],
            count=len(datas.data)
        )
    else:
        return Response.badRequest(
            message='Need Parameter kabupaten_kota'
        )
    # if kabupaten_kota:
    #     data = Kecamatan.objects(kabupaten=kabupaten_kota.id)
    #     datas = KecamatanKabSerializer(data, many=True)
    # else:
    #     data = Kecamatan.objects(kota=kabupaten_kota.id)
    #     datas = KecamatanKotSerializer(data, many=True)


def getDesa(request):
    kec = request.GET.get('kecamatan', None)

    if kec:
        try:
            kecamatan = Kecamatan.objects.get(id=kec)
        except Kecamatan.DoesNotExist:
            #return Response.badRequest(
            #    message='Kecamatan Does Not Exist'
            #)
            return Response.base(
                success=False,
                message='Province Does Not Exist',
                status=404
            )

        data = Desa.objects(kecamatan=kecamatan.id)
        datas = DesaSerializer(data, many=True)
        return Response.ok(
            data=datas.data,
            count=len(datas.data)
        )
    else:
        return Response.badRequest(
            message='Need Parameter kecamatan'
        )
