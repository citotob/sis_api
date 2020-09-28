from .models import Provinsi, Kabupaten, Kota, Kecamatan
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from .serializer import ProvinsiSerializer, KabupatenSerializer, KecamatanKabSerializer, KecamatanKotSerializer
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .response import Response
from rest_framework_mongoengine.viewsets import ModelViewSet, ReadOnlyModelViewSet
# Create your views here.


class ProvinsiViewSet(ReadOnlyModelViewSet):
    queryset = Provinsi.objects.all().order_by('name')
    serializer_class = ProvinsiSerializer
    lookup_field = 'name'
