# Standard library imports
import datetime
import json

# Third-party imports
from flask import Blueprint, request
from mongoengine import DoesNotExist

# Custom modules
from app.models.chatbotResponseDbModel import ChatbotResponse
from app.validators.models.chatbotResponseValidators import (
    ChatbotResponseModel,
    CreateChatbotResponseModel,
)
from service.errorHandler import error_handler
from service.machineLearning.getDescription import get_description
from service.machineLearning.getPrecaution import get_precaution
from service.machineLearning.getSymptomList import get_all_symptoms
from service.machineLearning.machineLearningModel import clf, cols
from service.machineLearning.makeSuggestion import make_suggestion
from service.pydanticDecorator import pydantic_validation
from service.response import response


# * Import Constant Variables
from static.problems import POSSIBLE_PROBLEMS_DICT_METADATA


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


# Define API Route for updating chatbot response details
@chatbot_response_module.route(
    "/<id>", methods=["PUT"], endpoint="update-chatbot-response"
)
@pydantic_validation(ChatbotResponseModel)
@error_handler
def update_chatbot_response_by_id(id):
    # Get the chatbot response instance with the given id
    chatbot_responses = ChatbotResponse.objects(id=id)

    # Check if the chatbot response is None or not
    if chatbot_responses.first() is None:
        return response(404, {"message": "ChatbotResponse not found"})

    # Get the update data from the request body
    data = request.get_json()

    # Update the chatbot response instance with the new data
    chatbot_responses.update(**data)

    # Update the modified_date field to the current date and time
    chatbot_responses.update(set__modified_date=datetime.datetime.now)

    # Prepare response body
    body = {
        "data": json.loads(chatbot_responses.first().to_json()),
        "message": "ChatbotResponse updated successfully",
    }

    # Return response with status code 200
    return response(200, body)


# Define API to delete a chatbot response by ID
@chatbot_response_module.route(
    "/<id>", methods=["DELETE"], endpoint="delete-chatbot-response"
)
@error_handler
def delete_chatbot_response_by_id(id):
    try:
        # Get chatbot response by ID and delete it
        ChatbotResponse.objects.get(id=id).delete()

        # Prepare response body
        body = {"message": "Chatbot Response deleted successfully"}

        # Return success response with status code 204
        return response(204, body)

    except DoesNotExist:
        # If chatbot response with the given ID is not found, return a 404 response
        body = {"message": "Chatbot Response not found"}
        return response(404, body)


# Design API to retrieve all chatbot responses from the database
@chatbot_response_module.route(
    "/", methods=["GET"], endpoint="get-all-chatbot-response"
)
@error_handler
def get_all_chatbot_responses():
    # Retrieve all chatbot responses from the database
    chatbot_responses = ChatbotResponse.objects()

    # Prepare response body with success message and retrieved chatbot responses
    body = {
        "msg": "Successfully get all Chatbot Response details.",
        "data": json.loads(chatbot_responses.to_json()),
    }

    # Return response with status code 200
    return response(200, body)


# Define API route to get a single chatbot response by ID
@chatbot_response_module.route(
    "/<id>", methods=["GET"], endpoint="get-single-chatbot-response"
)
@error_handler
def get_chatbot_response_by_id(id):
    try:
        # Retrieve chatbot response with given ID from MongoDB
        chatbot_response = ChatbotResponse.objects.get(id=id)

        # Prepare response body with chatbot response data
        body = {
            "msg": "Successfully get single Chatbot Response details.",
            "data": json.loads(chatbot_response.to_json()),
        }

        # Return response with status code 200 and body
        return response(200, body)
    except DoesNotExist:
        # Handle case where chatbot response with given ID is not found
        body = {"message": "ChatbotResponse not found"}
        return response(404, body)


# Define API route to get all possible problems
@chatbot_response_module.route(
    "/problems", methods=["GET"], endpoint="get-possible-problems"
)
@error_handler
def get_possible_problems():
    # Define response body with success message and data
    body = {
        "msg": "Successfully get all possible problems.",
        "data": POSSIBLE_PROBLEMS_DICT_METADATA,
    }

    # Return response with status code 200
    return response(200, body)


# * Desing API, which return all symptoms of particular problem
@chatbot_response_module.route(
    "/list-of-symptoms/<string:problem>", methods=["GET"], endpoint="list-of-symptoms"
)
@error_handler
def get_list_of_symptoms(problem):
    symptoms_exp = get_all_symptoms(clf, cols, problem)

    body = {
        "msg": "Successfully get all possible symptoms.",
        "data": symptoms_exp,
    }
    return response(200, body)


# * Desing API, which return all suggestion and remedy for particular problem
@chatbot_response_module.route(
    "/suggest-remedy", methods=["GET"], endpoint="suggest-remedy"
)
@error_handler
def get_suggest_remedy():
    data = json.loads(request.data)
    # Obtain the predicted disease from the data.
    disease_prediction = make_suggestion(data)

    # Create a response body with the necessary information.
    body = {
        "msg": "Successfully get all possible suggestion and remedy.",
        "data": {
            "problem": disease_prediction,
            "description": get_description(disease_prediction),
            "precaution_list": get_precaution(disease_prediction),
        },
    }

    # Return a response with a status code of 200 and the response body.
    return response(200, body)
