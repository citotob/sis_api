#from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer
from vendor.models import *

class vendor_applicationSerializer(DocumentSerializer):
    class Meta:
        model = vendor_application
        fields = '__all__'
        depth = 2
