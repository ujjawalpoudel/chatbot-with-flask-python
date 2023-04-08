import json

from service.response import response
from service.pydanticDecorator import pydantic_validation
from app.validators.chatbot.createChatbotUserValidators import CreateUserModel
from app.models.chatbotDbModel import User


@pydantic_validation(CreateUserModel)
def create_user_main(event, context):
    data = json.loads(event["body"])
    user = User(**data).save()
    body = {
        "data": json.loads(user.to_json()),
        "msg": "Create User successfully",
    }
    return response(200, body)
