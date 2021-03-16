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
from odps.models import Odp, desa, kecamatan, kabupaten, kota, provinsi
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


#class Odp(Document):
#    latitude = StringField(required=True)
#    longitude = StringField(required=True)
#    longlat = PointField()
#    #teknologi = ReferenceField(rekomendasi_teknologi)
#    teknologi = StringField(choices=['FO', 'VSAT'])
#    vendorid = ReferenceField(vendor)
#    created_at = DateTimeField(required=True, default=datetime.now)
#    updated_at = DateTimeField(required=True, default=datetime.now)
"""
class Odp(Document):
    #unik_id = IntField(required=True, unique=True)
    latitude = StringField(required=True, unique=True)
    longitude = StringField(required=True, unique=True)
    longlat = PointField()
    teknologi = StringField()
    nama = StringField(required=True)
    desa_kelurahan = ReferenceField(desa)
    kecamatan = ReferenceField(kecamatan)
    kabupaten = ReferenceField(kabupaten)
    kota = ReferenceField(kota)
    provinsi = ReferenceField(provinsi)
    kode_pos = StringField(required=True, default='00000')
    vendorid = ReferenceField(vendor)
    created_at = DateTimeField(required=True, default=datetime.now)
    updated_at = DateTimeField(required=True, default=datetime.now)
"""

class ListOdp(EmbeddedDocument):
    odp = ReferenceField(Odp)
    jarak = StringField(required=True, default=0)


class rekomendasi_teknologi(Document):
    # jarak_odp = IntField(required=True, default=0)
    teknologi = StringField(required=True, default='-')
    list_odp = EmbeddedDocumentListField(ListOdp)


class site(Document):
    unik_id = StringField(required=True, unique=True)
    latitude = StringField(required=True)
    longitude = StringField(required=True)
    longlat = PointField()
    rekomendasi_teknologi = ReferenceField(rekomendasi_teknologi)
    nama = StringField(required=True)
    desa_kelurahan = ReferenceField(desa)
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
                'desa_kelurahan': self.desa_kelurahan.serialize(),
                'kecamatan': self.kecamatan.serialize(),
                'kabupaten': self.kabupaten.serialize(),
                'provinsi': self.provinsi.serialize(),
                'kode_pos': self.kode_pos,
                'created_at': self.created_at,
                'updated_at': self.updated_at
            }
        except:
            # except Exception as e:
            # print(e)
            return {
                'id': str(self.id),
                'latitude': self.latitude,
                'longitude': self.longitude,
                'nama': self.nama,
                'desa_kelurahan': self.desa_kelurahan.serialize(),
                'kecamatan': self.kecamatan.serialize(),
                'kota': self.kota.serialize(),
                'provinsi': self.provinsi.serialize(),
                'kode_pos': self.kode_pos,
                'created_at': self.created_at,
                'updated_at': self.updated_at
            }

class site_offair(Document):
    unik_id = StringField(required=True, default='-')
    latitude = StringField(required=True, unique=True)
    longitude = StringField(required=True, unique=True)
    longlat = PointField()
    #rekomendasi_teknologi = ReferenceField(rekomendasi_teknologi)
    nama = StringField(required=True)
    desa_kelurahan = ReferenceField(desa)
    kecamatan = ReferenceField(kecamatan)
    kabupaten = ReferenceField(kabupaten)
    kota = ReferenceField(kota)
    provinsi = ReferenceField(provinsi)
    kode_pos = StringField(required=True, default='00000')
    #site_matchmaking = ListField(ReferenceField(site_matchmaking))
    #site_matchmaking = ListField()
    created_at = DateTimeField(required=True, default=datetime.now)
    updated_at = DateTimeField(required=True, default=datetime.now)
    status = ListField(required=True)

    #meta = { 'allow_inheritance': True }

    def serialize(self):
        try:
            return {
                'id': str(self.id),
                'latitude': self.latitude,
                'longitude': self.longitude,
                'longlat': str(self.longlat),
                'nama': self.nama,
                'desa_kelurahan': self.desa_kelurahan.serialize(),
                'kecamatan': self.kecamatan.serialize(),
                'kabupaten': self.kabupaten.serialize(),
                'provinsi': self.provinsi.serialize(),
                'kode_pos': self.kode_pos,
                'created_at': self.created_at,
                'updated_at': self.updated_at
            }
        except:
            # except Exception as e:
            # print(e)
            return {
                'id': str(self.id),
                'latitude': self.latitude,
                'longitude': self.longitude,
                'longlat': str(self.longlat),
                'nama': self.nama,
                'desa_kelurahan': self.desa_kelurahan.serialize(),
                'kecamatan': self.kecamatan.serialize(),
                'kota': self.kota.serialize(),
                'provinsi': self.provinsi.serialize(),
                'kode_pos': self.kode_pos,
                'created_at': self.created_at,
                'updated_at': self.updated_at
            }

class site_offair_norel(Document):
    unik_id = StringField(required=True, default='-')
    latitude = StringField(required=True, unique=True)
    longitude = StringField(required=True, unique=True)
    longlat = PointField()
    nama = StringField(required=True)
    desa_kelurahan = StringField()
    kecamatan = StringField()
    kabupaten = StringField()
    kota = StringField()
    provinsi = StringField()
    kode_pos = StringField(required=True, default='00000')
    created_at = DateTimeField(required=True, default=datetime.now)
    updated_at = DateTimeField(required=True, default=datetime.now)
    status = ListField(required=True)

    #meta = { 'allow_inheritance': True }

    def serialize(self):
        try:
            return {
                'id': str(self.id),
                'latitude': self.latitude,
                'longitude': self.longitude,
                'longlat': str(self.longlat),
                'nama': self.nama,
                'desa_kelurahan': self.desa_kelurahan,
                'kecamatan': self.kecamatan,
                'kabupaten': self.kabupaten,
                'provinsi': self.provinsi,
                'kode_pos': self.kode_pos,
                'created_at': self.created_at,
                'updated_at': self.updated_at
            }
        except:
            # except Exception as e:
            # print(e)
            return {
                'id': str(self.id),
                'latitude': self.latitude,
                'longitude': self.longitude,
                'longlat': str(self.longlat),
                'nama': self.nama,
                'desa_kelurahan': self.desa_kelurahan,
                'kecamatan': self.kecamatan,
                'kota': self.kota,
                'provinsi': self.provinsi,
                'kode_pos': self.kode_pos,
                'created_at': self.created_at,
                'updated_at': self.updated_at
            }

class doc_permohonan_rfi(Document):
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
    judul = StringField(required=True, unique=True)
    type = StringField(required=True, choices=[
        'VIP', 'Non-VIP'], default='Non-VIP')
    # sites = ListField(ReferenceField(site_matchmaking))
    sites = ListField()
    creator = ReferenceField(UserInfo)
    no_doc_permohonan_rfi = StringField(required=True, unique=True)
    doc_permohonan_rfi = ReferenceField(doc_permohonan_rfi)
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

    def serialize(self):
        penyedia_ = []
        for pu in self.penyedia_undang:
            penyedia_.append(pu.serialize())
        penyedia_k = []
        for pk in self.penyedia_kerja:
            penyedia_k.append(pk.serialize())
        return {
            'id': str(self.id),
            # 'nomor': self.nomor,
            'judul': self.judul,
            'type': self.type,
            'creator': self.creator.serialize(),
            'no_doc_permohonan_rfi': self.no_doc_permohonan_rfi,
            'doc_permohonan_rfi': self.doc_permohonan_rfi.serialize(),
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

class doc_quotation(Document):
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
    rfi = FloatField(required=True, default=0)
    vp = FloatField(required=True, default=0)
    teknologi = FloatField(required=True, default=0)
    harga = FloatField(required=True, default=0)
    created_at = DateTimeField(required=True, default=datetime.now)
    updated_at = DateTimeField(required=True, default=datetime.now)


class vendor_application(Document):
    users = ReferenceField(UserInfo)
    vendorid = ReferenceField(vendor)
    batchid = ReferenceField(batch)
    #siteid = ReferenceField(site_matchmaking)
    ##rfi_score_id = ReferenceField(rfi_score)
    vp_score_id = ReferenceField(VPScore)
    ##total_calc_id = ReferenceField(total_calc)
    rank = IntField(required=True, default=0)
    rfi_no = StringField(required=True, default='-')
    rfi_doc_id = ReferenceField(rfi_doc)
    tanggal_mulai_sla = DateTimeField(required=True, default=datetime.now)
    tanggal_akhir_sla = DateTimeField(required=True, default=datetime.now)
    days_sla = IntField(required=True, default=0)
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
            #"total_calc": self.total_calc.serialize(),
            "rank": str(self.rank),
            "rfi_no": self.rfi_no,
            "rfi_doc_id": self.rfi_doc_id.serialize(),
            "tanggal_mulai_sla": str(self.tanggal_mulai_sla),
            "tanggal_akhir_sla": str(self.tanggal_akhir_sla),
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }

class rfi_score(Document):
    #rfi_doc = ReferenceField(rfi_doc)
    vendor_app = ReferenceField(vendor_application)
    rekomendasi_teknologi = StringField(required=True, default='-')
    material_on_site = DateTimeField(required=True, default=datetime.now)
    installation = DateTimeField(required=True, default=datetime.now)
    on_air = DateTimeField(required=True, default=datetime.now)
    integration = DateTimeField(required=True, default=datetime.now)
    days_material_on_site = IntField(required=True, default=0)
    days_installation = IntField(required=True, default=0)
    days_on_air = IntField(required=True, default=0)
    days_on_integration = IntField(required=True, default=0)
    doc_quotation = ReferenceField(doc_quotation)
    biaya = FloatField(required=True, default=0)
    total_calc = ReferenceField(total_calc)
    created_at = DateTimeField(required=True, default=datetime.now)
    updated_at = DateTimeField(required=True, default=datetime.now)

class site_matchmaking(Document):
    siteid = ReferenceField(site)
    batchid = ReferenceField(batch)
    #applicants = ListField(ReferenceField(vendor_application))
    # applicants = ListField()
    rfi_score = ListField(ReferenceField(rfi_score))
    #vp_score = ListField(ReferenceField(VPScore))
    #total_calc = ReferenceField(total_calc)
    created_at = DateTimeField(required=True, default=datetime.now)
    updated_at = DateTimeField(required=True, default=datetime.now)
"""
class total_calc(Document):
    vendorid = ReferenceField(vendor)
    batchid = ReferenceField(batch)
    smm = ReferenceField(site_matchmaking)
    rfi = IntField(required=True, default=0)
    vp = IntField(required=True, default=0)
    teknologi = IntField(required=True, default=0)
    created_at = DateTimeField(required=True, default=datetime.now)
    updated_at = DateTimeField(required=True, default=datetime.now)
"""
