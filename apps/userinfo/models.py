from bson import ObjectId
import datetime
from django.contrib.auth.hashers import make_password, check_password
from mongoengine import signals
from mongoengine import *
from datetime import timedelta ,datetime
from django.conf import settings
from django.db import models
#from django.contrib.auth.models import AbstractUser
import random


class vendor(Document):
    name = StringField(required=True, unique=True)
    teknologi = ListField()
    latitude = StringField(required=True)
    longitude = StringField(required=True)
    nilai = FloatField()
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
            'teknologi': self.teknologi,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'nilai': str(self.nilai),
        }

class UserRole(Document):
    name = StringField(required=True)
    create_date = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))
    update_date = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))
    meta = {'collection': 'userrole'}

    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'create_date': str(self.create_date),
            'update_date': str(self.update_date),
        }


class DocumentUser(Document):
    name = StringField()
    path = StringField()
    create_date = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))
    update_date = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))

    def serialize(self):
        return {
            "name": self.name,
            "path": self.path,
            "create_date": self.create_date,
            "update_date": self.update_date,
        }


class UserInfo(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    name = StringField(required=True, default='-')
    company = ReferenceField(vendor)
    email = StringField(required=True, unique=True)
    phone = StringField(required=True, default='-')
    status = StringField(required=True, choices=[
                         'requested', 'verified', 'declined'], default='requested')
    comment = StringField(required=False)
    role = ReferenceField(UserRole)
    #surveyor = StringField(required=True)
    doc = ReferenceField(DocumentUser)
    token_reset = StringField()
    create_date = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))
    update_date = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))

    #note = StringField(required=True, default='-')

    def serialize(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "name": self.name,
            "company": self.company.serialize(),
            "email": self.email,
            "phone": self.phone,
            "status": self.status,
            "comment": self.comment,
            "role": self.role.serialize(),
            "doc": self.doc.serialize(),
            "token_reset": self.token_reset
        }


class UserToken(Document):
    key = StringField(required=True)
    created = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))
    updated = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))
    user = ReferenceField(UserInfo)

    meta = {
        'indexes': [
            {'fields': ('key', 'user'), 'unique': True}
        ]
    }

class Message(Document):
    title = StringField(required=True,default='-')
    message = StringField(required=True,default='-')
    created = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))
    updated = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))
    userfrom = ReferenceField(UserInfo)
    userto = ListField(required=True)
    redirect = StringField(required=True,default='/')
    status = StringField(required=True, choices=[
                         'new', 'open'], default='new')

