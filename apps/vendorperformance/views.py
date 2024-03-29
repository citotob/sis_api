from django.shortcuts import render
from rest_framework_mongoengine.viewsets import GenericAPIView, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from .models import VPScore
import json
from .customResponse import CustomResponse
from django.http import JsonResponse
from .serializer import VPSerializer, VPCreateSerializer
from apps.userinfo.models import vendor
from apps.userinfo.serializer import VendorScoreSerializer
# Create your views here.


# def asd(request):
#     try:
#         a = VendorPerformance.objects.all()
#         serializer = VendorPerformanceSerializer(a, many=True)
#         # print(serializer.data)
#         d = Response(serializer.data,
#                      content_type="application/json")
#         return d
#     except Exception as e:
#         print(e)


class VendorPerformanceAPI(ModelViewSet):
    # parser_classes = (FileUploadParser,)

    def getByVendor(self, request, format=None):
        try:
            vendorId = request.query_params.get('id')
            if not vendorId:
                raise TypeError('Need Param "id"')
            data = vendor.objects.get(id=vendorId)
            serializer = VendorScoreSerializer(data)
            return CustomResponse.ok(values=serializer.data)
        except vendor.DoesNotExist:
            return CustomResponse().base(success=False, message='Id Not Found', status=status.HTTP_404_NOT_FOUND)
        except TypeError as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def getAll(self, request, format=None):
    #     vp = VPScore.objects.all()
    #     serializer = VPSerializer(vp, many=True)
    #     return CustomResponse.ok(values=serializer.data)

    def getAll(self, request, format=None):
        try:
            vp = vendor.objects.order_by('-name')
            serializer = VendorScoreSerializer(vp, many=True)
            return CustomResponse.ok(values=serializer.data)
        except Exception as e:
            print(e)

    def create(self, request, format=None):
        try:
            serializer = VPCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return CustomResponse().base(values=serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, format=None):
        try:
            data = VPScore.objects.get(id=request.data.get('id', None))
            serializer = VPSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                newData = VPSerializer(
                    serializer.update(data, serializer.data))
                return CustomResponse().base(values=newData.data, status=status.HTTP_201_CREATED)
        except VPScore.DoesNotExist as e:
            return CustomResponse().base(success=False, message='Id Not Found', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
