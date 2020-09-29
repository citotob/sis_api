from django.db import models
import random
from django.conf import settings
from mongoengine import *
from mongoengine import signals
#from django.contrib.auth.hashers import make_password, check_password
import datetime
from bson import ObjectId
from datetime import timedelta ,datetime
#from userinfo.models import UserInfo, Surveyor, JenisSurvey
from sites.models import batch, site_location

class company(Document):
    name = StringField(required=True, unique=True)
    #jenissurvey = ReferenceField(JenisSurvey)
    created_at = DateTimeField(
        default=datetime.utcnow() + timedelta(hours=7))
    updated_at = DateTimeField(
        default=datetime.utcnow() + timedelta(hours=7))
    #meta = {
    #    'indexes': [
    #        {'fields': ('name'), 'unique': True}
    #    ]
    #}

    def serialize(self):
        return {
            'id': str(self.id),
            'name': str(self.name),
        }

class document_batch_vendor(Document):
    name = StringField()
    path = StringField()
    create_date = DateTimeField(
        default=datetime.utcnow() + timedelta(hours=7))
    update_date = DateTimeField(
        default=datetime.utcnow() + timedelta(hours=7))

    def serialize(self):
        return {
            "name": self.name,
            "path": self.path,
            "create_date": self.create_date,
            "update_date": self.update_date,
        }

class batch_vendor(Document):
    vendor = ReferenceField(company)
    batch_id = ReferenceField(batch)
    rfi_no = StringField(required=True,default='-')
    rfi_doc = ReferenceField(document_batch_vendor)
    tanggal_mulai_sla = DateTimeField(
        default=datetime.utcnow() + timedelta(hours=7))
    tanggal_selesai_sla = DateTimeField(
        default=datetime.utcnow() + timedelta(hours=7))
    status = ListField()
    created_at = DateTimeField(
        default=datetime.utcnow() + timedelta(hours=7))
    updated_at = DateTimeField(
        default=datetime.utcnow() + timedelta(hours=7))

    #meta = {
    #    'indexes': [
    #        {'fields': ('nomor'), 'unique': True}       
    #    ]
    #}
    
    def serialize(self):
        return {
            'id': str(self.id),
            'vendor': self.vendor.serialize(),
            'batch_id': self.batch_id.serialize(),
            'rfi_no': self.rfi_no,
            'rfi_doc': self.rfi_doc.serialize(),
            'tanggal_mulai_sla': str(self.tanggal_mulai_sla),
            'tanggal_selesai_sla': str(self.tanggal_selesai_sla),
            'status': self.status,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
        }

class site_vendor(Document):
    vendor = ReferenceField(company)
    batch_id = ReferenceField(batch)
    site_id = ReferenceField(site_location)
    rekomen_teknologi = StringField(required=True,default='-')
    tanggal_mulai_material = DateTimeField(
        default=datetime.utcnow() + timedelta(hours=7))
    tanggal_selesai_material = DateTimeField(
        default=datetime.utcnow() + timedelta(hours=7))
    tanggal_mulai_installation = DateTimeField(
        default=datetime.utcnow() + timedelta(hours=7))
    tanggal_selesai_installation = DateTimeField(
        default=datetime.utcnow() + timedelta(hours=7))
    tanggal_mulai_onair = DateTimeField(
        default=datetime.utcnow() + timedelta(hours=7))
    tanggal_selesai_onair = DateTimeField(
        default=datetime.utcnow() + timedelta(hours=7))
    tanggal_mulai_ir = DateTimeField(
        default=datetime.utcnow() + timedelta(hours=7))
    tanggal_selesai_ir = DateTimeField(
        default=datetime.utcnow() + timedelta(hours=7))
    status = ListField()
    created_at = DateTimeField(
        default=datetime.utcnow() + timedelta(hours=7))
    updated_at = DateTimeField(
        default=datetime.utcnow() + timedelta(hours=7))

    #meta = {
    #    'indexes': [
    #        {'fields': ('nomor'), 'unique': True}       
    #    ]
    #}
    
    def serialize(self):
        return {
            'id': str(self.id),
            'vendor': self.vendor.serialize(),
            'batch_id': str(self.batch_id),
            'site_id': self.site_id.serialize(),
            'rekomen_teknologi': self.rekomen_teknologi,
            'tanggal_mulai_material': str(self.tanggal_mulai_material),
            'tanggal_selesai_material': str(self.tanggal_selesai_material),
            'tanggal_mulai_installation': str(self.tanggal_mulai_installation),
            'tanggal_selesai_installation': str(self.tanggal_selesai_installation),
            'tanggal_mulai_onair': str(self.tanggal_mulai_onair),
            'tanggal_selesai_onair': str(self.tanggal_selesai_onair),
            'tanggal_mulai_ir': str(self.tanggal_mulai_ir),
            'tanggal_selesai_ir': str(self.tanggal_selesai_ir),
            'status': self.status,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
        }