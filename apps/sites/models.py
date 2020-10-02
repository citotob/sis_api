from django.db import models
import random
from django.conf import settings
from mongoengine import *
from mongoengine import signals
#from django.contrib.auth.hashers import make_password, check_password
import datetime
from bson import ObjectId
from datetime import timedelta ,datetime
from userinfo.models import UserInfo, company
from rest_framework_mongoengine import serializers as drfm_serializers
from rest_framework import serializers as drf_serializers
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
    tanggal_pembuatan = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))
    tanggal_perubahan = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))
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
    tanggal_pembuatan = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))
    tanggal_perubahan = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))

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
    tanggal_pembuatan = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))
    tanggal_perubahan = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))

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
    tanggal_pembuatan = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))
    tanggal_perubahan = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))

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
    tanggal_pembuatan = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))
    tanggal_perubahan = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))

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

class rekomendasi_teknologi(Document):
  jarak_ODP = IntField(required=True,default=0)
  teknologi = StringField(required=True,default='-')

class site(Document):
    unik_id = IntField(required=True,unique=True)
    latitude = StringField(required=True)
    longitude = StringField(required=True)
    rekomendasi_teknologi = ReferenceField(rekomendasi_teknologi)
    nama = StringField(required=True)
    desa = ReferenceField(desa)
    kecamatan = ReferenceField(kecamatan)
    kabupaten = ReferenceField(kabupaten)
    kota = ReferenceField(kota)
    provinsi = ReferenceField(provinsi)
    kode_pos = StringField(required=True,default='00000')
    site_matchmaking ListField(ReferenceField(site_matchmaking))
    created_at = DateTimeField(
        default=datetime.utcnow() + timedelta(hours=7))
    updated_at = DateTimeField(
        default=datetime.utcnow() + timedelta(hours=7))
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
        #except Exception as e:
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

class batch(Document):
    #sites = ListField(required=True)
    #creator = ReferenceField(users)
    nomor = StringField(required=True, unique=True)
    judul = StringField(required=True)
    type = StringField(required=True, choices=[
                         'VIP', 'Non-VIP'], default='Non-VIP')
    sites = ListField(ReferenceField(site_location))
    creator = ReferenceField(UserInfo)
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
    penyedia_undang = ListField(ReferenceField(company))
    penyedia_kerja = ListField(ReferenceField(company))
    status = ListField(required=True)
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
            'rfi_doc': self.rfi_doc.serialize(),
            'tanggal_mulai_undangan': str(self.tanggal_mulai_undangan),
            'tanggal_selesai_undangan': str(self.tanggal_selesai_undangan),
            'tanggal_mulai_kerja': str(self.tanggal_mulai_kerja),
            'tanggal_selesai_kerja': str(self.tanggal_selesai_kerja),
            'penyedia_undang': penyedia_,
            #'penyedia_undang': drf_serializers.ListField(child=self.penyedia_undang),
            #'penyedia_kerja': drf_serializers.ListField(child=self.penyedia_kerja),
            'penyedia_kerja': penyedia_k,
            'status': self.status,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
        }

class site_matchmaking(Document):
    site = ReferenceField(site)
    batch = ReferenceField(batch)
    applicants array [ref: > vendor_application.id]
    created_at timestamp
    updated_at timestamp