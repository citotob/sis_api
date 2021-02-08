#from rest_framework import serializers

from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework_mongoengine import fields
from rest_framework import serializers
from odps.models import Odp

class odpSerializer(DocumentSerializer):
    class Meta:
        model = Odp
        #fields = ['latitude', 'longitude', 'teknologi']
        depth = 0