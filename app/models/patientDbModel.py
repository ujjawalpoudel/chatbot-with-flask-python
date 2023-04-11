# Standard library imports
import datetime
import json

# Third-party imports
from mongoengine import (
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    DateTimeField,
    StringField,
    IntField,
    ReferenceField,
)

# Custom modules
from app.models.chatbotDbModel import User


GENDER = (("male", "MALE"), ("female", "FEMALE"), ("other", "OTHER"))


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


class Address(EmbeddedDocument):
    street = StringField()
    city = StringField()
    state = StringField()
    zipCode = StringField()


class Patient(DefaultAttributes, Document):
    gender = StringField(choices=GENDER)
    phoneNumber = StringField(required=True)
    address = EmbeddedDocumentField(Address)
    lastVisit = DateTimeField()

    userId = ReferenceField(User)
