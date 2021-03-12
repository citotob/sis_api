from django.db import models
from mongoengine import DynamicDocument, Document, fields
# Create your models here.


class Provinsi(Document):
    name = fields.StringField()
    latitude = fields.StringField()
    longitude = fields.StringField()
    prefix = fields.StringField()
    tanggal_pembuatan = fields.DateTimeField()
    tanggal_perubahan = fields.DateTimeField()
    __v = fields.IntField(db_field='__v')
    code = fields.StringField()
    meta = {'collection': 'provinsi'}


class Kabupaten(Document):
    name = fields.StringField()
    provinsi = fields.ReferenceField(Provinsi)
    # latitude = fields.StringField()
    # longitude = fields.StringField()
    longlat = fields.PointField()
    tanggal_pembuatan = fields.DateTimeField()
    tanggal_perubahan = fields.DateTimeField()
    __v = fields.IntField(db_field='__v')

    meta = {'collection': 'kabupaten'}


class Kota(Document):
    name = fields.StringField()
    provinsi = fields.ReferenceField(Provinsi)
    # latitude = fields.StringField()
    # longitude = fields.StringField()
    longlat = fields.PointField()
    tanggal_pembuatan = fields.DateTimeField()
    tanggal_perubahan = fields.DateTimeField()
    __v = fields.IntField(db_field='__v')

    meta = {
        'collection': 'kota',
        'ordering': 'name',
    }


class Kecamatan(Document):
    name = fields.StringField()
    kabupaten = fields.ReferenceField(Kabupaten)
    kota = fields.ReferenceField(Kota)
    # latitude = fields.StringField()
    # longitude = fields.StringField()
    longlat = fields.PointField()
    tanggal_pembuatan = fields.DateTimeField()
    tanggal_perubahan = fields.DateTimeField()
    __v = fields.IntField(db_field='__v')

    meta = {'collection': 'kecamatan'}


class Desa(Document):
    name = fields.StringField()
    kecamatan = fields.ReferenceField(Kecamatan)
    kota = fields.ReferenceField(Kota)
    tanggal_pembuatan = fields.DateTimeField()
    tanggal_perubahan = fields.DateTimeField()
    __v = fields.IntField(db_field='__v')

    meta = {'collection': 'desa'}
