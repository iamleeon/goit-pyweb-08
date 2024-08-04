import connect

from mongoengine import Document
from mongoengine.fields import ListField, StringField, ReferenceField


class Author(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    author = ReferenceField(Author)
    quote = StringField()
    tags = ListField(StringField())
