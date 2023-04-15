# Standard library imports
import datetime
import json

# Third-party imports
from flask import Blueprint, request
from mongoengine import DoesNotExist

# Custom modules
from app.models.medicalrecordDbModel import medicalrecord
from service.errorHandler import error_handler
from service.pydanticDecorator import pydantic_validation
from service.response import response


# * Define Blueprint for API Routes
medicalrecord_module = Blueprint("medicalrecord_module", __name__)


# * Define API Route for Create medicalrecord API
@medicalrecord_module.route("/", methods=["POST"], endpoint="create-medical-record")
@error_handler
def create_medicalrecord_main():
    # * Get Data from Frontend
    data = json.loads(request.data)

    # * Save Data in Mongodb
    medicalrecord = medicalrecord(**data).save()

    body = {
        "data": json.loads(medicalrecord.to_json()),
        "msg": "Medical record created successfully.",
    }
    return response(201, body)


# * Define API for update medicalrecord details
@medicalrecord_module.route("/<id>", methods=["PUT"], endpoint="update-medical-record")
@error_handler
def update_medicalrecord_by_id(id):
    # get the medicalrecord instance with the given id
    medicalrecords = medicalrecord.objects(id=id)

    # Check if the medicalrecord is None or not
    if medicalrecords.first() == None:
        return response(404, {"message": "Medical record not found."})

    # get the update data from the request body
    data = request.get_json()

    # update the medicalrecord instance with the new data
    medicalrecords.update(**data)

    # update the modified_date field to the current date and time
    medicalrecords.update(set__modified_date=datetime.datetime.now)

    body = {
        "data": json.loads(medicalrecords.first().to_json()),
        "message": "Medical record updated successfully.",
    }
    return response(200, body)


# * Define API, which read id and delete medical record
@medicalrecord_module.route(
    "/<id>", methods=["DELETE"], endpoint="delete-medical-record"
)
@error_handler
def delete_medicalrecord_by_id(id):
    try:
        medicalrecord.objects.get(id=id).delete()
        body = {"message": "Medical record deleted successfully."}
        return response(204, body)
    except DoesNotExist:
        body = {"message": "Medical record not found."}
        return response(404, body)


# * Define API, which reads all medical records from the database
@medicalrecord_module.route("/", methods=["GET"], endpoint="get-all-medical-records")
@error_handler
def get_all_medicalrecords():
    medicalrecords = medicalrecord.objects()
    body = {
        "msg": "Successfully get all Medical record details.",
        "data": json.loads(medicalrecords.to_json()),
    }
    return response(200, body)


# * Define API, which takes document id and returns value of that document
@medicalrecord_module.route(
    "/<id>", methods=["GET"], endpoint="get-single-medical-record"
)
@error_handler
def get_medicalrecord_by_id(id):
    try:
        medicalrecord = medicalrecord.objects.get(id=id)
        body = {
            "msg": "Successfully get single medical record details.",
            "data": json.loads(medicalrecord.to_json()),
        }
        return response(200, body)
    except DoesNotExist:
        body = {"message": "Medical record not found"}
        return response(404, body)
