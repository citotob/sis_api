from django.db import models
import random
from django.conf import settings
from mongoengine import *
from mongoengine.fields import *
from mongoengine import signals
#from django.contrib.auth.hashers import make_password, check_password
import datetime
from bson import ObjectId
from datetime import timedelta, datetime
from userinfo.models import UserInfo, vendor
from vendorperformance.models import *
from rest_framework_mongoengine import serializers as drfm_serializers
from rest_framework import serializers as drf_serializers
from . import *
"""
class company(Document):
    name = StringField(required=True, unique=True)
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
"""

class provinsi(Document):
    #user = ReferenceField(UserInfo)
    name = StringField(required=True)
    tanggal_pembuatan = DateTimeField(required=True, default=datetime.now)
    tanggal_perubahan = DateTimeField(required=True, default=datetime.now)
    prefix = StringField(required=True)
    meta = {
        'strict': False,
    }

    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'tanggal_pembuatan': str(self.tanggal_pembuatan),
            'tanggal_perubahan': str(self.tanggal_perubahan),
        }


class kabupaten(Document):
    name = StringField(required=True)
    provinsi = ReferenceField(provinsi)
    tanggal_pembuatan = DateTimeField(required=True, default=datetime.now)
    tanggal_perubahan = DateTimeField(required=True, default=datetime.now)

    meta = {
        'strict': False,
    }

    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            # 'provinsi': str(self.provinsi.serialize()),
            'tanggal_pembuatan': str(self.tanggal_pembuatan),
            'tanggal_perubahan': str(self.tanggal_perubahan),
        }


class kota(Document):
    name = StringField(required=True)
    provinsi = ReferenceField(provinsi)
    tanggal_pembuatan = DateTimeField(required=True, default=datetime.now)
    tanggal_perubahan = DateTimeField(required=True, default=datetime.now)

    meta = {
        'strict': False,
    }

    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            # 'provinsi': str(self.provinsi.serialize()),
            'tanggal_pembuatan': str(self.tanggal_pembuatan),
            'tanggal_perubahan': str(self.tanggal_perubahan),
        }


class kecamatan(Document):
    name = StringField(required=True)
    kabupaten = ReferenceField(kabupaten)
    kota = ReferenceField(kota)
    tanggal_pembuatan = DateTimeField(required=True, default=datetime.now)
    tanggal_perubahan = DateTimeField(required=True, default=datetime.now)

    meta = {
        'strict': False,
    }

    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            # 'kabupaten': self.kabupaten.serialize(),
            # 'kota': self.kabupaten.serialize(),
            'tanggal_pembuatan': str(self.tanggal_pembuatan),
            'tanggal_perubahan': str(self.tanggal_perubahan),
        }


class desa(Document):
    name = StringField(required=True)
    kecamatan = ReferenceField(kecamatan)
    tanggal_pembuatan = DateTimeField(required=True, default=datetime.now)
    tanggal_perubahan = DateTimeField(required=True, default=datetime.now)

    meta = {
        'strict': False,
    }

    def serialize(self):
        return {
            'id': str(self.id),
            'name': str(self.name),
            # 'kecamatan': str(self.kecamatan.serialize()),
            'tanggal_pembuatan': str(self.tanggal_pembuatan),
            'tanggal_perubahan': str(self.tanggal_perubahan),
        }


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


class rekomendasi_teknologi(Document):
    jarak_odp = IntField(required=True, default=0)
    teknologi = StringField(required=True, default='-')

class Odp(Document):
    latitude = StringField(required=True)
    longitude = StringField(required=True)
    longlat = PointField()
    teknologi = ReferenceField(rekomendasi_teknologi)
    vendorid = ReferenceField(vendor)
    created_at = DateTimeField(required=True, default=datetime.now)
    updated_at = DateTimeField(required=True, default=datetime.now)
    
class site(Document):
    unik_id = IntField(required=True, unique=True)
    latitude = StringField(required=True)
    longitude = StringField(required=True)
    longlat = PointField()
    rekomendasi_teknologi = ReferenceField(rekomendasi_teknologi)
    nama = StringField(required=True)
    desa = ReferenceField(desa)
    kecamatan = ReferenceField(kecamatan)
    kabupaten = ReferenceField(kabupaten)
    kota = ReferenceField(kota)
    provinsi = ReferenceField(provinsi)
    kode_pos = StringField(required=True, default='00000')
    #site_matchmaking = ListField(ReferenceField(site_matchmaking))
    site_matchmaking = ListField()
    created_at = DateTimeField(required=True, default=datetime.now)
    updated_at = DateTimeField(required=True, default=datetime.now)
    #status = ListField(required=True)
    """
    def serialize(self):
        try:
            return {
                'id': str(self.id),
                'provinsi': self.provinsi.serialize(),
                'kabupaten': self.kabupaten.serialize(),
                'kecamatan': self.kecamatan.serialize(),
                'desa': self.desa.serialize(),
                'latitude': str(self.latitude),
                'longitude': str(self.longitude)
            }
        except:
            return {
                'id': str(self.id),
                'provinsi': self.provinsi.serialize(),
                'kota': self.kota.serialize(),
                'kecamatan': self.kecamatan.serialize(),
                'desa': self.desa.serialize(),
                'latitude': str(self.latitude),
                'longitude': str(self.longitude)
            }
    """

    def serialize(self):
        try:
            return {
                'id': str(self.id),
                'latitude': self.latitude,
                'longitude': self.longitude,
                'nama': self.nama,
                'desa': self.desa.serialize(),
                'kecamatan': self.kecamatan.serialize(),
                'kabupaten': self.kabupaten.serialize(),
                'provinsi': self.provinsi.serialize(),
                'kode_pos': self.kode_pos,
                'created_at': self.created_at,
                'updated_at': self.updated_at
            }
        except:
            # except Exception as e:
            print(e)
            return {
                'id': str(self.id),
                'latitude': self.latitude,
                'longitude': self.longitude,
                'nama': self.nama,
                'desa': self.desa.serialize(),
                'kecamatan': self.kecamatan.serialize(),
                'kota': self.kota.serialize(),
                'provinsi': self.provinsi.serialize(),
                'kode_pos': self.kode_pos,
                'created_at': self.created_at,
                'updated_at': self.updated_at
            }


class document_batch(Document):
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


class batch(Document):
    #sites = ListField(required=True)
    #creator = ReferenceField(users)
    nomor = StringField(required=True, unique=True)
    judul = StringField(required=True)
    type = StringField(required=True, choices=[
        'VIP', 'Non-VIP'], default='Non-VIP')
    # sites = ListField(ReferenceField(site_matchmaking))
    sites = ListField()
    creator = ReferenceField(UserInfo)
    rfi_no = StringField(required=True)
    rfi_doc_id = ReferenceField(document_batch)
    tanggal_mulai_undangan = DateTimeField(required=True, default=datetime.now)
    tanggal_selesai_undangan = DateTimeField(
        required=True, default=datetime.now)
    tanggal_mulai_kerja = DateTimeField(required=True, default=datetime.now)
    tanggal_selesai_kerja = DateTimeField(required=True, default=datetime.now)
    penyedia_undang = ListField(ReferenceField(vendor))
    penyedia_kerja = ListField(ReferenceField(vendor))
    status = ListField(required=True)
    created_at = DateTimeField(required=True, default=datetime.now)
    updated_at = DateTimeField(required=True, default=datetime.now)

    # meta = {
    #    'indexes': [
    #        {'fields': ('nomor'), 'unique': True}
    #    ]
    # }

    def serialize(self):
        penyedia_=[]
        for pu in self.penyedia_undang:
            penyedia_.append(pu.serialize())
        penyedia_k=[]
        for pk in self.penyedia_kerja:
            penyedia_k.append(pk.serialize())
        return {
            'id': str(self.id),
            'nomor': self.nomor,
            'judul': self.judul,
            'type': self.type,
            'creator': self.creator.serialize(),
            'rfi_no': self.rfi_no,
            'rfi_doc_id': self.rfi_doc_id.serialize(),
            'tanggal_mulai_undangan': str(self.tanggal_mulai_undangan),
            'tanggal_selesai_undangan': str(self.tanggal_selesai_undangan),
            'tanggal_mulai_kerja': str(self.tanggal_mulai_kerja),
            'tanggal_selesai_kerja': str(self.tanggal_selesai_kerja),
            'penyedia_undang': penyedia_,
            # 'penyedia_undang': drf_serializers.ListField(child=self.penyedia_undang),
            # 'penyedia_kerja': drf_serializers.ListField(child=self.penyedia_kerja),
            'penyedia_kerja': penyedia_k,
            'status': self.status,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
        }


class rfi_score(Document):
    #rfi_doc = ReferenceField(rfi_doc)
    rekomendasi_teknologi = StringField(required=True, default='-')
    material_on_site = DateTimeField(required=True, default=datetime.now)
    installation = DateTimeField(required=True, default=datetime.now)
    on_air = DateTimeField(required=True, default=datetime.now)
    integration = DateTimeField(required=True, default=datetime.now)
    days_material_on_site = IntField(required=True, default=0)
    days_installation = IntField(required=True, default=0)
    days_on_air = IntField(required=True, default=0)
    days_on_integration = IntField(required=True, default=0)
    created_at = DateTimeField(required=True, default=datetime.now)
    updated_at = DateTimeField(required=True, default=datetime.now)


"""
class vp_score(Document):
    kecepatan = IntField(required=True,default=0)
    ketepatan = IntField(required=True,default=0)
    kualitas = IntField(required=True,default=0)
    vendorid = ReferenceField(vendor)
    created_at = DateTimeField(required=True, default=datetime.now)
    updated_at = DateTimeField(required=True, default=datetime.now)
"""


class total_calc(Document):
    rfi = IntField(required=True, default=0)
    vp = IntField(required=True, default=0)
    teknologi = IntField(required=True, default=0)
    created_at = DateTimeField(required=True, default=datetime.now)
    updated_at = DateTimeField(required=True, default=datetime.now)


class vendor_application(Document):
    users = ReferenceField(UserInfo)
    vendorid = ReferenceField(vendor)
    batchid = ReferenceField(batch)
    #siteid = ReferenceField(site_matchmaking)
    rfi_score_id = ReferenceField(rfi_score)
    vp_score_id = ReferenceField(VPScore)
    total_calc_id = ReferenceField(total_calc)
    rank = IntField(required=True, default=0)
    rfi_no = StringField(required=True, default='-')
    rfi_doc_id = ReferenceField(rfi_doc)
    tanggal_mulai_sla = DateTimeField(required=True, default=datetime.now)
    tanggal_akhir_sla = DateTimeField(required=True, default=datetime.now)
    created_at = DateTimeField(required=True, default=datetime.now)
    updated_at = DateTimeField(required=True, default=datetime.now)

    meta = {
        'indexes': [
            {'fields': ('vendorid', 'batchid'), 'unique': True}
        ]
    }

    def serialize(self):
        return {
            "id": str(self.id),
            "users": self.users.serialize(),
            "vp_score_id": self.vp_score_id.serialize(),
            "total_calc": self.total_calc.serialize(),
            "rank": str(self.rank),
            "rfi_no": self.rfi_no,
            "rfi_doc_id": self.rfi_doc_id.serialize(),
            "tanggal_mulai_sla": str(self.tanggal_mulai_sla),
            "tanggal_akhir_sla": str(self.tanggal_akhir_sla),
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }


class site_matchmaking(Document):
    siteid = ReferenceField(site)
    batchid = ReferenceField(batch)
    applicants = ListField(ReferenceField(vendor_application))
    # applicants = ListField()
    created_at = DateTimeField(required=True, default=datetime.now)
    updated_at = DateTimeField(required=True, default=datetime.now)
