from django.db import models
from mongoengine import *
from mongoengine.fields import *
from userinfo.models import vendor

from datetime import timedelta, datetime

class provinsi(Document):
    #user = ReferenceField(UserInfo)
    name = StringField(required=True)
    tanggal_pembuatan = DateTimeField(required=True, default=datetime.now)
    tanggal_perubahan = DateTimeField(required=True, default=datetime.now)
    prefix = StringField()
    code = StringField()
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
    longlat = PointField()
    tanggal_pembuatan = DateTimeField(required=True, default=datetime.now)
    tanggal_perubahan = DateTimeField(required=True, default=datetime.now)

    meta = {
        'strict': False,
    }

    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'longlat': str(self.longlat),
            # 'provinsi': str(self.provinsi.serialize()),
            'tanggal_pembuatan': str(self.tanggal_pembuatan),
            'tanggal_perubahan': str(self.tanggal_perubahan),
        }


class kota(Document):
    name = StringField(required=True)
    provinsi = ReferenceField(provinsi)
    longlat = PointField()
    tanggal_pembuatan = DateTimeField(required=True, default=datetime.now)
    tanggal_perubahan = DateTimeField(required=True, default=datetime.now)

    meta = {
        'strict': False,
    }

    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'longlat': str(self.longlat),
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

class Odp(Document):
    #unik_id = IntField(required=True, unique=True)
    latitude = StringField(required=True)
    longitude = StringField(required=True)
    longlat = PointField()
    teknologi = StringField()
    nama = StringField(required=True)
    desa_kelurahan_name = StringField()
    kecamatan_name = StringField()
    kabupaten_name = StringField()
    kota_name = StringField()
    provinsi_name = StringField()
    kode_pos = StringField(required=True, default='00000')
    vendor_name = StringField()
    desa_kelurahan = ReferenceField(desa)
    kecamatan = ReferenceField(kecamatan)
    kabupaten = ReferenceField(kabupaten)
    kota = ReferenceField(kota)
    provinsi = ReferenceField(provinsi)
    vendor = ReferenceField(vendor)
    monthly_sla = DictField()
    yearly_sla = FloatField()
    created_at = DateTimeField(required=True, default=datetime.now)
    updated_at = DateTimeField(required=True, default=datetime.now)

    meta = { 'unique_together': ['latitude', 'longitude'] }


class Odp_backup(Document):
    #unik_id = IntField(required=True, unique=True)
    latitude = StringField(required=True, unique=True)
    longitude = StringField(required=True, unique=True)
    longlat = PointField()
    teknologi = StringField()
    nama = StringField(required=True)
    desa_kelurahan = StringField()
    kecamatan = StringField()
    kabupaten = StringField()
    kota = StringField()
    provinsi = StringField()
    kode_pos = StringField(required=True, default='00000')
    vendorid = StringField()
    created_at = DateTimeField(required=True, default=datetime.now)
    updated_at = DateTimeField(required=True, default=datetime.now)

class bts_onair(Document):
    unik_id = StringField(required=True, unique=True)
    latitude = StringField(required=True, unique=True)
    longitude = StringField(required=True, unique=True)
    longlat = PointField()
    #teknologi = StringField()
    nama = StringField(required=True)
    desa_kelurahan = StringField()
    kecamatan_name = StringField()
    kabupaten_name = StringField()
    kota_name = StringField()
    provinsi_name = StringField()
    desa = ReferenceField(desa)
    kecamatan = ReferenceField(kecamatan)
    kabupaten = ReferenceField(kabupaten)
    kota = ReferenceField(kota)
    provinsi = ReferenceField(provinsi)
    kode_pos = StringField(required=False, default='00000')
    #vendorid = StringField()
    created_at = DateTimeField(required=True, default=datetime.now)
    updated_at = DateTimeField(required=True, default=datetime.now)
    access_date = DateTimeField()
