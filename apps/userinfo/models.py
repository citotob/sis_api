from bson import ObjectId
import datetime
from django.contrib.auth.hashers import make_password, check_password
from mongoengine import signals
from mongoengine import *
from datetime import timedelta ,datetime
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
import random


# Create your models here.
class JenisSurvey(Document):
    #user = ReferenceField(UserInfo)
    user = StringField(required=False)
    jenis = StringField(required=True)

    def serialize(self):
        return {
            'id': str(self.id),
            #'user': str(self.user),
            'jenis': str(self.jenis),
        }

class Surveyor(Document):
    #user = ReferenceField(UserInfo)
    #user = StringField(required=False)
    name = StringField(required=True)
    jenissurvey = ReferenceField(JenisSurvey)

    meta = {
        'indexes': [
            {'fields': ('name', 'jenissurvey'), 'unique': True}
        ]
    }

    def serialize(self):
        return {
            'id': str(self.id),
            #'user': str(self.user),
            'jenissurvey': self.jenissurvey.serialize(),
            'name': str(self.name),
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
    name = StringField(required=True)
    organization = ReferenceField(Surveyor)
    email = StringField(required=True, unique=True)
    phone = StringField(required=True)
    status = StringField(required=True, choices=[
                         'requested', 'verified', 'declined'], default='requested')
    comment = StringField(required=False)
    role = ReferenceField(UserRole)
    #surveyor = StringField(required=True)
    doc = ReferenceField(DocumentUser)
    # role = StringField(required=True)
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
            "organization": self.organization.serialize(),
            "email": self.email,
            "phone": self.phone,
            "status": self.status,
            "comment": self.comment,
            #"surveyor": self.surveyor,
            "role": self.role.serialize(),
            "doc": self.doc.serialize(),
        }

    # def hashPassword(self, password):
    #    return make_password(password, settings.SECRET_KEY)

    # def checkPassword(self, password):
    #    return check_password(password, self.password, 'pbkdf2_sha256')

    # def clean(self):
    #     self.password = self.hashPassword(self.password)
    #     print(self.checkPassword(self.password))


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

