#from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer
from sites.models import *

class vendor_applicationSerializer(DocumentSerializer):
    class Meta:
        model = vendor_application
        fields = '__all__'
        depth = 2

class vendor_applicationResponSerializer(DocumentSerializer):
    class Meta:
        model = vendor_application
        #fields = fields = [
        #    'id',
        #    'users',
        #    'vendorid',
        #    #'batchid',
        #    'vp_score_id',
        #    #total_calc = ReferenceField(total_calc)
        #    'rank',
        #    'rfi_no',
        #    'rfi_doc_id',
        #    'tanggal_mulai_sla',
        #    'tanggal_akhir_sla',
        #    'created_at',
        #    'updated_at'
        #]
        exclude = ['batchid' ]
        depth = 2

class rfi_scoreSerializer(DocumentSerializer):
    class Meta:
        model = rfi_score
        fields = '__all__'
        depth = 2
