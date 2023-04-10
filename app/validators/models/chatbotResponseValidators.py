# * Import Python Module
import pydantic
from typing import Optional

# * Import User Defined Functions
from utils.validationCheck import bson_id_check
from app.models.chatbotResponseDbModel import ChatbotResponse
from app.validators.models.chatbotUserValidators import UserIdModel


class ChatbotResponseIdModel(pydantic.BaseModel, extra=pydantic.Extra.forbid):
    chatbotId: str

    @pydantic.validator("chatbotId")
    @classmethod
    def id_valid_check(cls, chatbot_id) -> None:
        if bson_id_check(chatbot_id):
            try:
                ChatbotResponse.objects.get(id=chatbot_id)
                return chatbot_id
            except ChatbotResponse.DoesNotExist:
                message = "Given chatbotId ({0}) does not exits in database.".format(
                    chatbot_id
                )
                raise ValueError(message)
        else:
            message = "Given chatbotId ({0}) is not valid object chatbotId.".format(
                chatbot_id
            )
            raise ValueError(message)


class ChatbotResponseModel(pydantic.BaseModel, extra=pydantic.Extra.forbid):
    symptom: str
    condition: str
    recommendedAction: Optional[str]


class CreateChatbotResponseModel(UserIdModel, extra=pydantic.Extra.forbid):
    symptom: str
    condition: str
    recommendedAction: Optional[str]
