# * Import Python Module
import pydantic
from typing import Optional
from enum import Enum
from datetime import datetime

# * Import User Defined Functions
from utils.validationCheck import bson_id_check
from app.models.patientDbModel import Patient
from app.validators.models.chatbotUserValidators import UserIdModel


class PatientIdModel(pydantic.BaseModel, extra=pydantic.Extra.forbid):
    patientId: str

    @pydantic.validator("patientId")
    @classmethod
    def id_valid_check(cls, patient_id) -> None:
        if bson_id_check(patient_id):
            try:
                Patient.objects.get(id=patient_id)
                return patient_id
            except Patient.DoesNotExist:
                message = "Given patient_id ({0}) does not exits in database.".format(
                    patient_id
                )
                raise ValueError(message)
        else:
            message = "Given patient_id ({0}) is not valid object patient_id.".format(
                patient_id
            )
            raise ValueError(message)


class AddressModel(pydantic.BaseModel, extra=pydantic.Extra.forbid):
    street: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zipCode: Optional[str]


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class PatientModel(UserIdModel, extra=pydantic.Extra.forbid):
    gender: GenderEnum
    phoneNumber: str
    address: Optional[AddressModel]
    lastVisit: Optional[datetime]
