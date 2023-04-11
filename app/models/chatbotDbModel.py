# Standard library imports
import datetime

# Third-party imports
from mongoengine import Document, ValidationError
from mongoengine.fields import DateTimeField, StringField, IntField, EmailField


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
    fullname = StringField(max_length=200, required=True, validation=not_null)
    age = IntField(max_value=100, min_value=0, required=True)
    email = EmailField(required=True, unique=True)
    address = StringField()
    password = StringField(required=True)
