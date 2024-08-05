import connect

from mongoengine import Document
from mongoengine.fields import StringField, EmailField, BooleanField, IntField


class Contact(Document):
    full_name = StringField()
    email_address = EmailField()
    is_sent = BooleanField(default=False)



