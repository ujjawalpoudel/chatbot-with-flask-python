import datetime

# import mongoengine_goodjson as gj
from mongoengine import Document
from mongoengine.fields import DateTimeField, StringField, IntField, EmailField
from mongoengine import ValidationError

# Connect to MongoDB database
# from config import db_connected


def not_null(name):
    if len(name) < 2:
        raise ValidationError("Name must have at least 2 characters")


class DefaultAttributes:
    meta = {"allow_inheritance": True}
    creation_date = DateTimeField()
    modified_date = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(DefaultAttributes, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.modified_date = datetime.datetime.now()
        return super(DefaultAttributes, self).save(*args, **kwargs)


class User(DefaultAttributes, Document):
    name = StringField(max_length=200, required=True, validation=not_null)
    age = IntField(max_value=100, min_value=0, required=True)
    email = EmailField(required=True)
    address = StringField()
