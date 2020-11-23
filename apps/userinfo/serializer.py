from apps.vendorperformance.models import VPScore
from apps.vendorperformance.serializer import VPSerializer
from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import vendor
from rest_framework import serializers


class VendorScoreSerializer(DocumentSerializer):
    class Meta:
        model = vendor
        fields = '__all__'
        depth = 2

    def to_representation(self, instance):
        vp = VPScore.objects(vendor=instance.id).order_by('-created_at')
        instance.nilai = VPSerializer(vp, many=True).data
        return super().to_representation(instance)
