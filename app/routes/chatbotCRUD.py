# Standard Library Imports
import json
from datetime import datetime

# Third-Party Imports
from flask import Blueprint, request
from mongoengine import DoesNotExist

# Local Imports
from app.models.chatbotDbModel import User
from app.validators.models.chatbotUserValidators import UserModel, UpdateUserModel
from service.errorHandler import error_handler
from service.pydanticDecorator import pydantic_validation
from service.response import response
from utils.passwordHash import hash_password


# * Define Blueprint for API Routes
chatbot_user_module = Blueprint("chatbot_user_module", __name__)


# * Define API Route for Create User API
@chatbot_user_module.route("/", methods=["POST"], endpoint="create-user")
@pydantic_validation(UserModel)
@error_handler
def create_user_main():
    # * Get Data from Frontend
    data = json.loads(request.data)
    data["password"] = hash_password(data["password"])

    # * Save Data in Mongodb
    user = User(**data).save()

    body = {
        "data": json.loads(user.to_json()),
        "msg": "Create User successfully",
    }
    return response(201, body)


# Define an endpoint for updating user details
@chatbot_user_module.route("/<id>", methods=["PUT"], endpoint="update-user")
@pydantic_validation(UpdateUserModel)
@error_handler
def update_chatbot_user_by_id(id):
    # Get the user instance with the given id
    users = User.objects(id=id)

    # Check if the user instance is None or not
    if users.first() is None:
        return response(404, {"message": "User not found"})

    # Get the update data from the request body
    data = request.get_json()

    # Update the user instance with the new data
    users.update(**data)

    # Update the modified_date field to the current date and time
    users.update(set__modified_date=datetime.now())

    # Build the response body
    body = {
        "data": json.loads(users.first().to_json()),
        "message": "User updated successfully",
    }

    # Return the response with the updated user instance
    return response(200, body)


# Define an API endpoint to delete a user by id
@chatbot_user_module.route("/<id>", methods=["DELETE"], endpoint="delete-user")
@error_handler
def delete_chatbot_user_by_id(id):
    # Attempt to delete the user with the given id
    try:
        User.objects.get(id=id).delete()
        body = {"message": "User deleted successfully"}
        # Return a success response with a 204 status code
        return response(204, body)
    # If the user is not found, return a 404 error response
    except DoesNotExist:
        body = {"message": "User not found"}
        return response(404, body)


# define the API route to get all users
@chatbot_user_module.route("/", methods=["GET"], endpoint="get-all-users")
@error_handler
def get_all_chatbot_users():
    # retrieve all users from the database
    users = User.objects()

    # format the response body
    body = {
        "msg": "Successfully get all users details.",
        "data": json.loads(users.to_json()),
    }

    # return the response
    return response(200, body)


# Define endpoint for getting a single user by ID
@chatbot_user_module.route("/<id>", methods=["GET"], endpoint="get-single-user")
@error_handler
def get_chatbot_user_by_id(id):
    try:
        # Get user object by ID from database
        user = User.objects.get(id=id)
        # Create response body with success message and user details
        body = {
            "msg": "Successfully get single user details.",
            "data": json.loads(user.to_json()),
        }
        # Return response with 200 OK status code and response body
        return response(200, body)
    except DoesNotExist:
        # If user not found, create response body with error message
        body = {"message": "User not found"}
        # Return response with 404 Not Found status code and response body
        return response(404, body)
