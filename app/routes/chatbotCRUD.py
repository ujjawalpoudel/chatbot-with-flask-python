# * Import Python Module
import json
import datetime
from flask import Blueprint, request
from mongoengine import DoesNotExist


# * Import User Defined Functions
from app.validators.models.chatbotUserValidators import UserModel
from service.errorHandler import error_handler
from service.pydanticDecorator import pydantic_validation
from app.models.chatbotDbModel import User
from service.response import response


# * Define Blueprint for API Routes
chatbot_user_module = Blueprint("chatbot_user_module", __name__)


# * Define API Route for Create User API
@chatbot_user_module.route("/", methods=["POST"], endpoint="create-user")
@pydantic_validation(UserModel)
@error_handler
def create_user_main():
    # * Get Data from Frontend
    data = json.loads(request.data)

    # * Save Data in Mongodb
    user = User(**data).save()

    body = {
        "data": json.loads(user.to_json()),
        "msg": "Create User successfully",
    }
    return response(201, body)


# * Design API for update user details
@chatbot_user_module.route("/<id>", methods=["PUT"], endpoint="update-user")
@pydantic_validation(UserModel)
@error_handler
def update_chatbot_user_by_id(id):
    # get the user instance with the given id
    users = User.objects(id=id)

    # Check if the user is None or not
    if users.first() == None:
        return response(404, {"message": "User not found"})

    # get the update data from the request body
    data = request.get_json()

    # update the user instance with the new data
    users.update(**data)

    # update the modified_date field to the current date and time
    users.update(set__modified_date=datetime.datetime.now)

    body = {
        "data": json.loads(users.first().to_json()),
        "message": "User updated successfully",
    }
    return response(200, body)


# * Desing API, which read id and delete user
@chatbot_user_module.route("/<id>", methods=["DELETE"], endpoint="delete-user")
@error_handler
def delete_chatbot_user_by_id(id):
    try:
        User.objects.get(id=id).delete()
        body = {"message": "User deleted successfully"}
        return response(204, body)
    except DoesNotExist:
        body = {"message": "User not found"}
        return response(404, body)


# * Desing API, which reads all users from the database
@chatbot_user_module.route("/", methods=["GET"], endpoint="get-all-users")
@error_handler
def get_all_chatbot_users():
    users = User.objects()
    body = {
        "msg": "Successfully get all users details.",
        "data": json.loads(users.to_json()),
    }
    return response(200, body)


# * Design API, which takes document id and returns value of that document
@chatbot_user_module.route("/<id>", methods=["GET"], endpoint="get-single-user")
@error_handler
def get_chatbot_user_by_id(id):
    try:
        user = User.objects.get(id=id)
        body = {
            "msg": "Successfully get single user details.",
            "data": json.loads(user.to_json()),
        }
        return response(200, body)
    except DoesNotExist:
        body = {"message": "User not found"}
        return response(404, body)
