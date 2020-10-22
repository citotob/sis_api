#from rest_framework import serializers

from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework_mongoengine import fields
from rest_framework import serializers
from .models import Odp

class ODPSerializer(DocumentSerializer):
    class Meta:
        model = Odp
        depth = 2
        exclude = ('vendorid.teknologi',)

class siteonairSerializer(DocumentSerializer):
    class Meta:
        model = Odp
        fields = '__all__'
        depth = 0
