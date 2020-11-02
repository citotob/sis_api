from django.db import models
from mongoengine import DynamicDocument, Document, fields, EmbeddedDocument
from datetime import datetime
from apps.userinfo.models import UserInfo, vendor
# Create your models here.


class VPScore(Document):
    user = fields.ReferenceField(UserInfo)
    kecepatan = fields.IntField(min_value=0, max_value=5, default=0)
    ketepatan = fields.IntField(min_value=0, max_value=5, default=0)
    kualitas = fields.IntField(min_value=0, max_value=5, default=0)
    vendor = fields.ReferenceField(vendor)
    doc = fields.DynamicField(required=True)
    created_at = fields.DateTimeField(
        required=True, default=datetime.now)
    updated_at = fields.DateTimeField(required=True, default=datetime.now)

    meta = {
        'collection': 'vp_score',
        'ordering': ['-updated_at']
    }
