from rest_framework_mongoengine.serializers import DocumentSerializer, DynamicDocumentSerializer
from rest_framework_mongoengine.serializers import serializers
from .models import VPScore
from datetime import datetime


class VPSerializer(DocumentSerializer):

    class Meta:
        model = VPScore
        fields = '__all__'
        # exclude = ('user.password',)
        depth = 5

    def update(self, instance, validated_data):
        instance.kecepatan = validated_data.get(
            'kecepatan', instance.kecepatan)
        instance.ketepatan = validated_data.get(
            'ketepatan', instance.ketepatan)
        instance.kualitas = validated_data.get('kualitas', instance.kualitas)
        instance.updated_at = datetime.now()
        instance.save()
        return instance


class VPCreateSerializer(DocumentSerializer):

    class Meta:
        model = VPScore
        fields = '__all__'
        # exclude = ('user.password',)
        depth = 0
