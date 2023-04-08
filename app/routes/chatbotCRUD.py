from flask import Blueprint, request
import json

import json

from service.response import response
from service.pydanticDecorator import pydantic_validation
from app.validators.chatbot.createChatbotUserValidators import CreateUserModel
from app.models.chatbotDbModel import User

chatbot_user_module = Blueprint("chatbot_user_module", __name__)


@chatbot_user_module.route("/")
def welcome_chatbot():
    return "<h1>Welcome to Medical Chatbot</h1>"


@chatbot_user_module.route("/createUser", methods=["POST"])
# @pydantic_validation(CreateUserModel)
def create_user_main():
    data = json.loads(request.data)
    print("Data:", data)
    user = User(**data).save()
    print("yaha gayo  ke nae")
    body = {
        "data": json.loads(user.to_json()),
        "msg": "Create User successfully",
    }
    return response(200, body)


# @chatbot_user_module.route("/updateUser", methods=["PUT"])
# def update_chatbot_user():
#     req = json.loads(request.data)
#     # summary=budgetSummary(req)
#     return json.dumps()


# @chatbot_user_module.route("/deleteUser", methods=["DELETE"])
# def delete_chatbot_user():
#     req = json.loads(request.data)
#     # summary=excelbudget(req)
#     return json.dumps()


# @chatbot_user_module.route("/readUsers", methods=["GET"])
# def get_chatbot_users():
#     req = json.loads(request.data)
#     # summary=excelbudget(req)
#     return json.dumps()


# @chatbot_user_module.route("/readUser", methods=["GET"])
# def get_chatbot_user():
#     req = json.loads(request.data)
#     # summary=excelbudget(req)
#     return json.dumps()
