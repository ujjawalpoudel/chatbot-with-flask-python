# * Import Python Module
import json
from flask import Blueprint, request
from mongoengine import DoesNotExist


# * Import User Defined Functions
from app.validators.chatbot.createChatbotUserValidators import CreateUserModel
from service.pydanticDecorator import pydantic_validation
from app.models.chatbotDbModel import User
from service.response import response


# * Define Blueprint for API Routes
chatbot_user_module = Blueprint("chatbot_user_module", __name__)


# * Define API Route for Create User API
@chatbot_user_module.route("/", methods=["POST"])
@pydantic_validation(CreateUserModel)
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


@chatbot_user_module.route("/<id>", methods=["PUT"])
def update_chatbot_user_by_id():
    # get the user instance with the given id
    try:
        user = User.objects.get(id=id)
    except DoesNotExist:
        return response(404, {"message": "User not found"})

    # get the update data from the request body
    data = request.get_json()

    # update the user instance with the new data
    user.update(**data)

    # save the updated user instance
    user.reload()

    body = {"data": user.to_json(), "message": "User updated successfully"}

    # return the updated user instance
    return response(200, body)


# * Desing API, which read id and delete user
@chatbot_user_module.route("/<id>", methods=["DELETE"])
def delete_chatbot_user_by_id(id):
    try:
        user = User.objects.get(id=id)
        user.delete()
        body = {"message": "User deleted successfully"}
        return response(204, body)
    except DoesNotExist:
        body = {"message": "User not found"}
        return response(404, body)


# * Desing API, which reads all users from the database
@chatbot_user_module.route("/", methods=["GET"])
def get_all_chatbot_users():
    users = User.objects()
    body = {
        "msg": "Successfully get all users details.",
        "data": json.loads(users.to_json()),
    }
    return response(200, body)


# * Design API, which takes document id and returns value of that document
@chatbot_user_module.route("/<id>", methods=["GET"])
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
