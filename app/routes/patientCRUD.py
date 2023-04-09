# * Import Python Module
import json
from flask import Blueprint, request
from mongoengine import DoesNotExist


# * Import Patient Defined Functions
from app.validators.models.patientValidators import PatientModel
from service.pydanticDecorator import pydantic_validation
from service.errorHandler import error_handler
from app.models.patientDbModel import Patient
from service.response import response


# * Define Blueprint for API Routes
patient_module = Blueprint("patient_module", __name__)


# * Define API Route for Create Patient API
@patient_module.route("/", methods=["POST"], endpoint="create-pateint")
@pydantic_validation(PatientModel)
@error_handler
def create_patient_main():
    # * Get Data from Frontend
    data = json.loads(request.data)

    # * Save Data in Mongodb
    patient = Patient(**data).save()

    body = {
        "data": json.loads(patient.to_json()),
        "msg": "Create Patient successfully",
    }
    return response(201, body)


# * Design API for update patient details
@patient_module.route("/<id>", methods=["PUT"], endpoint="update-pateint")
@pydantic_validation(PatientModel)
@error_handler
def update_patient_by_id(id):
    # get the patient instance with the given id
    patients = Patient.objects(id=id)

    # Check if the patient is None or not
    if patients.first() == None:
        return response(404, {"message": "Patient not found"})

    # get the update data from the request body
    data = request.get_json()

    # update the patient instance with the new data
    patients.update(**data)

    body = {
        "data": json.loads(patients.first().to_json()),
        "message": "Patient updated successfully",
    }
    return response(200, body)


# * Desing API, which read id and delete patient
@patient_module.route("/<id>", methods=["DELETE"], endpoint="delete-pateint")
@error_handler
def delete_patient_by_id(id):
    try:
        Patient.objects.get(id=id).delete()
        body = {"message": "Patient deleted successfully"}
        return response(204, body)
    except DoesNotExist:
        body = {"message": "Patient not found"}
        return response(404, body)


# * Desing API, which reads all patients from the database
@patient_module.route("/", methods=["GET"], endpoint="get-all-pateints")
@error_handler
def get_all_patients():
    patients = Patient.objects()
    body = {
        "msg": "Successfully get all patients details.",
        "data": json.loads(patients.to_json()),
    }
    return response(200, body)


# * Design API, which takes document id and returns value of that document
@patient_module.route("/<id>", methods=["GET"], endpoint="get-single-pateint")
@error_handler
def get_patient_by_id(id):
    try:
        patient = Patient.objects.get(id=id)
        body = {
            "msg": "Successfully get single patient details.",
            "data": json.loads(patient.to_json()),
        }
        return response(200, body)
    except DoesNotExist:
        body = {"message": "Patient not found"}
        return response(404, body)