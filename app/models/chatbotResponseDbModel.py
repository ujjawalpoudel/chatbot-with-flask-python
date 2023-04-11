# Standard Library Imports
import datetime

# Third-Party Imports
from mongoengine import Document
from mongoengine.fields import DateTimeField, StringField, ReferenceField

# Custom modules
from app.models.chatbotDbModel import User


class DefaultAttributes:
    meta = {"allow_inheritance": True}
    creation_date = DateTimeField()
    # modified_date = DateTimeField(default=datetime.datetime.now)

    modified_date = DateTimeField(
        default=datetime.datetime.now, required=True, update=True
    )

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(DefaultAttributes, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.modified_date = datetime.datetime.now()
        return super(DefaultAttributes, self).save(*args, **kwargs)


class ChatbotResponse(DefaultAttributes, Document):
    symptom = StringField(required=True)
    condition = StringField(required=True)
    recommendedAction = StringField()

    userId = ReferenceField(User)
