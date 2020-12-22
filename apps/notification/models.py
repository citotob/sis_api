from django.db import models
from mongoengine import DynamicDocument, Document, fields, EmbeddedDocument
from datetime import datetime
from userinfo.models import UserInfo
# Create your models here.


class Notification(Document):
    from_ = fields.ReferenceField(UserInfo, db_field='from', required=True)
    to = fields.ListField(field=fields.ReferenceField(UserInfo), db_field='to')
    type = fields.StringField(db_field='type')
    title = fields.StringField(db_field='title')
    message = fields.StringField(db_field='message')

    created_at = fields.DateTimeField(
        required=True, default=datetime.now)
    updated_at = fields.DateTimeField(required=True, default=datetime.now)

    meta = {
        'collection': 'notification',
        'ordering': ['-ctrated_att']
    }
