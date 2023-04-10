# * Import Python Module
import json
import datetime
from flask import Blueprint, request
from mongoengine import DoesNotExist


# * Import User Defined Functions
from app.validators.models.chatbotResponseValidators import (
    ChatbotResponseModel,
    CreateChatbotResponseModel,
)
from service.errorHandler import error_handler
from service.pydanticDecorator import pydantic_validation
from app.models.chatbotResponseDbModel import ChatbotResponse
from service.response import response


# * Define Blueprint for API Routes
chatbot_response_module = Blueprint("chatbot_response_module", __name__)


# * Define API Route for Create Chatbot Response API
@chatbot_response_module.route(
    "/", methods=["POST"], endpoint="create-chatbot-response"
)
@pydantic_validation(CreateChatbotResponseModel)
@error_handler
def create_chatbot_response_main():
    # * Get Data from Frontend
    data = json.loads(request.data)

    # * Save Data in Mongodb
    chatbot_response = ChatbotResponse(**data).save()

    body = {
        "data": json.loads(chatbot_response.to_json()),
        "msg": "Create ChatbotResponse successfully",
    }
    return response(201, body)


# * Design API for update chatbot response details
@chatbot_response_module.route(
    "/<id>", methods=["PUT"], endpoint="update-chatbot-response"
)
@pydantic_validation(ChatbotResponseModel)
@error_handler
def update_chatbot_response_by_id(id):
    # get the chatbot response instance with the given id
    chatbot_responses = ChatbotResponse.objects(id=id)

    # Check if the chatbot response is None or not
    if chatbot_responses.first() == None:
        return response(404, {"message": "ChatbotResponse not found"})

    # get the update data from the request body
    data = request.get_json()

    # update the chatbot response instance with the new data
    chatbot_responses.update(**data)

    # update the modified_date field to the current date and time
    chatbot_responses.update(set__modified_date=datetime.datetime.now)

    body = {
        "data": json.loads(chatbot_responses.first().to_json()),
        "message": "ChatbotResponse updated successfully",
    }
    return response(200, body)


# * Desing API, which read id and delete chatbot response
@chatbot_response_module.route(
    "/<id>", methods=["DELETE"], endpoint="delete-chatbot-response"
)
@error_handler
def delete_chatbot_response_by_id(id):
    try:
        ChatbotResponse.objects.get(id=id).delete()
        body = {"message": "Chatbot Response deleted successfully"}
        return response(204, body)
    except DoesNotExist:
        body = {"message": "Chatbot Response not found"}
        return response(404, body)


# * Desing API, which reads all chatbot responses from the database
@chatbot_response_module.route(
    "/", methods=["GET"], endpoint="get-all-chatbot-response"
)
@error_handler
def get_all_chatbot_responses():
    chatbot_responses = ChatbotResponse.objects()
    body = {
        "msg": "Successfully get all Chatbot Response details.",
        "data": json.loads(chatbot_responses.to_json()),
    }
    return response(200, body)


# * Design API, which takes document id and returns value of that document
@chatbot_response_module.route(
    "/<id>", methods=["GET"], endpoint="get-single-chatbot-response"
)
@error_handler
def get_chatbot_response_by_id(id):
    try:
        chatbot_response = ChatbotResponse.objects.get(id=id)
        body = {
            "msg": "Successfully get single Chatbot Response details.",
            "data": json.loads(chatbot_response.to_json()),
        }
        return response(200, body)
    except DoesNotExist:
        body = {"message": "ChatbotResponse not found"}
        return response(404, body)
