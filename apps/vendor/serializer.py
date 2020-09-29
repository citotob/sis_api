#from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer
from sites.models import *

class BatchSerializer(DocumentSerializer):
    class Meta:
        model = batch
        fields = '__all__'
        #depth = 2

class SiteSerializer(DocumentSerializer):
    class Meta:
        model = site_location
        fields = '__all__'
        depth = 2