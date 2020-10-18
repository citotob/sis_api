#from rest_framework import serializers

from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework_mongoengine import fields
from rest_framework import serializers
from .models import site_matchmaking, batch, vendor_application, site_offair

"""
class ODPSerializer(DocumentSerializer):
    class Meta:
        model = Odp
        depth = 2
        exclude = ('vendorid.teknologi',)
"""

class VendorApplicationSerializer(DocumentSerializer):
    class Meta:
        model = vendor_application
        depth = 2


class SiteMatchmakingSerializer(DocumentSerializer):

    class Meta:
        model = site_matchmaking
        depth = 2
    # fields = ['id', 'siteid', 'applicants', 'created_at', 'updated_at']
        exclude = ('batchid', 'applicants.batchid')


class BatchSerializer(DocumentSerializer):

    class Meta:
        model = batch
        fields = '__all__'
        # exclude = ('sites.batchid')

    def to_representation(self, instance):
        try:
            data = site_matchmaking.objects(id__in=instance.sites)
            serializers = SiteMatchmakingSerializer(data, many=True)
            instance.sites = serializers.data
        except Exception as e:
            print(e)
        return super().to_representation(instance)
        # return instance



class siteoffairSerializer(DocumentSerializer):
    class Meta:
        model = site_offair
        #fields = '__all__'
        depth = 1
