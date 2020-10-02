from django.db import models
import random
from django.conf import settings
from mongoengine import *
from mongoengine import signals
#from django.contrib.auth.hashers import make_password, check_password
import datetime
from bson import ObjectId
from datetime import timedelta ,datetime
from userinfo.models import *
from sites.models import *

class rfi_doc(Document):
    name = StringField()
    path = StringField()
    create_date = DateTimeField(required=True, default=datetime.now)
    update_date = DateTimeField(required=True, default=datetime.now)

    def serialize(self):
        return {
            "name": self.name,
            "path": self.path,
            "create_date": self.create_date,
            "update_date": self.update_date,
        }

class rfi_score(Document):
    rfi_doc = ReferenceField(rfi_doc)
    rekomendasi_teknologi = StringField(required=True,default='-')
    material_on_site = DateTimeField(required=True, default=datetime.now)
    installation = DateTimeField(required=True, default=datetime.now)
    on_air = DateTimeField(required=True, default=datetime.now)
    integration = DateTimeField(required=True, default=datetime.now)
    days_material_on_site = IntField(required=True,default=0)
    days_installation = IntField(required=True,default=0)
    days_on_air = IntField(required=True,default=0)
    created_at = DateTimeField(required=True, default=datetime.now)
    updated_at = DateTimeField(required=True, default=datetime.now)

class vp_score(Document):
    kecepatan = IntField(required=True,default=0)
    ketepatan = IntField(required=True,default=0)
    kualitas = IntField(required=True,default=0)
    vendor = ReferenceField(vendor)

class total_calc(Document):
    rfi = IntField(required=True,default=0)
    vp = IntField(required=True,default=0)
    teknologi = IntField(required=True,default=0)
    created_at = DateTimeField(required=True, default=datetime.now)
    updated_at = DateTimeField(required=True, default=datetime.now)

class vendor_application(Document):
    users = ReferenceField(UserInfo)
    rfi_score = ReferenceField(rfi_score)
    vp_score = ReferenceField(vp_score)
    total_calc = ReferenceField(total_calc)
    rank = IntField(required=True,default=0)
    created_at = DateTimeField(required=True, default=datetime.now)
    updated_at = DateTimeField(required=True, default=datetime.now)
"""
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
"""
"""
nomor = StringField(required=True, unique=True)
    judul = StringField(required=True)
    type = StringField(required=True, choices=[
                         'VIP', 'Non-VIP'], default='Non-VIP')
    sites = ListField(ReferenceField(site_location))
    creator = StringField(required=True)
    rfi_no = StringField(required=True)
    rfi_doc = ReferenceField(document_batch)
    tanggal_mulai_undangan = DateTimeField(
        default=datetime.utcnow() + timedelta(hours=7))
    tanggal_selesai_undangan = DateTimeField(
        default=datetime.utcnow() + timedelta(hours=7))
    tanggal_mulai_kerja = DateTimeField(
        default=datetime.utcnow() + timedelta(hours=7))
    tanggal_selesai_kerja = DateTimeField(
        default=datetime.utcnow() + timedelta(hours=7))
"""
"""
class batch_vendor(Document):
    vendor = ReferenceField(vendor)
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
    vendor = ReferenceField(vendor)
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
"""