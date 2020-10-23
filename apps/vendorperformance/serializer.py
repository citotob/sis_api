from rest_framework_mongoengine.serializers import DocumentSerializer, DynamicDocumentSerializer
from rest_framework_mongoengine.serializers import serializers
from rest_framework.validators import ValidationError
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from .models import VPScore
import functools


class VPSerializer(DocumentSerializer):

    class Meta:
        model = VPScore
        # fields = '__all__'
        exclude = ('user.password', 'vendor')
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

    def validate(self, attrs):
        doc = attrs['doc']
        fs = FileSystemStorage(
            location=f'{settings.MEDIA_ROOT}/vp_score/{attrs["vendor"].id}/',
            base_url=f'{settings.MEDIA_URL}/vp_score/{attrs["vendor"].id}/'
        )
        if doc.content_type != 'application/pdf':
            raise ValidationError('File type not PDF')
        filename = fs.save(doc.name, doc)
        file_path = fs.url(filename)
        attrs['doc'] = file_path
        return attrs
