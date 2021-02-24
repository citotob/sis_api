from rest_framework_mongoengine import serializers, fields
from rest_framework import serializers as serializer
from rest_framework.serializers import PrimaryKeyRelatedField, SlugRelatedField, SerializerMethodField
from .models import Provinsi, Kabupaten, Kecamatan, Desa


class ProvinsiSerializer(serializers.DocumentSerializer):
    # siteStats = SerializerMethodField()

    class Meta:
        model = Provinsi
        fields = ['id', 'name']

    # def get_siteStats(self, obj):
    #     stat = Kabupaten.


class KabupatenSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Kabupaten
        depth = 1
        fields = ['id', 'provinsi', 'provinsi.name',
                  'name','longlat']


class KecamatanKabSerializer(serializers.DocumentSerializer):

    class Meta:
        model = Kecamatan
        depth = 1
        fields = ['id',  'kabupaten', 'kabupaten.name', 'name']


class KecamatanKotSerializer(serializers.DocumentSerializer):

    class Meta:
        model = Kecamatan
        depth = 1
        fields = ['id', 'kota', 'kota.name',
                  'kabupaten', 'kabupaten.name', 'name']


class DesaSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Desa
        depth = 1
        fields = ['id', 'kecamatan', 'kecamatan.name', 'name']


# class CustomProvinsiSerializer(serializers.DynamicDocumentSerializer):
#     id = fields.ObjectIdField()
