from mongoengine import Document, FloatField, StringField, ReferenceField, DateTimeField
from mongoengine.errors import ValidationError
from datetime import datetime


# Custom modules
from app.models.patientDbModel import Patient


# "MedicalRecord" model with validators
class MedicalRecord(Document):
    bloodSugarLevel = FloatField(required=True, min_value=0, max_value=500)
    height = FloatField(required=True, min_value=0, max_value=300)
    weight = FloatField(required=True, min_value=0, max_value=1000)
    allergies = StringField()
    currentMedications = StringField()
    medicalHistory = StringField()
    systolicPressure = FloatField(required=True, min_value=0, max_value=300)
    diastolicPressure = FloatField(required=True, min_value=0, max_value=300)
    patientId = ReferenceField(Patient, required=True)
    dateCreated = DateTimeField(required=True, default=datetime.utcnow)
    dateModified = DateTimeField(required=True, default=datetime.utcnow)

    # Custom validation method for the "MedicalRecord" model
    def clean(self):
        # Check if systolic pressure is greater than diastolic pressure
        if self.systolicPressure < self.diastolicPressure:
            raise ValidationError(
                "Systolic pressure cannot be less than diastolic pressure"
            )
