#from rest_framework import serializers

from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework_mongoengine import fields
from rest_framework import serializers
from .models import Odp

class ODPSerializer(DocumentSerializer):
    class Meta:
        model = Odp
        fields = ['longlat','latitude', 'longitude', 'teknologi', 'provinsi_name', 'kabupaten_name', 'kecamatan_name', 
            'desa_kelurahan_name', 'nama','vendor_name', 'created_at','updated_at']
        depth = 2
        #exclude = ('vendorid.teknologi',)

class siteonairSerializer(DocumentSerializer):
    class Meta:
        model = Odp
        #fields = ['latitude', 'longitude', 'teknologi']
        fields = ['latitude', 'longitude', 'teknologi', 'provinsi_name', 'kabupaten_name', 'kecamatan_name', 
            'desa_kelurahan_name', 'nama','vendor_name']
        depth = 0

class siteprovinsiSerializer(DocumentSerializer):
    class Meta:
        model = Odp
        #fields = ['latitude', 'longitude', 'teknologi']
        depth = 0
