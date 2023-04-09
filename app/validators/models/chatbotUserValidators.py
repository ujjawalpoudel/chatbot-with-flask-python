import pydantic
from typing import Optional

from utils.validationCheck import email_check, bson_id_check
from app.models.chatbotDbModel import User


class UserIdModel(pydantic.BaseModel, extra=pydantic.Extra.forbid):
    userId: str

    @pydantic.validator("userId")
    @classmethod
    def id_valid_check(cls, user_id) -> None:
        if bson_id_check(user_id):
            try:
                User.objects.get(id=user_id)
                return user_id
            except User.DoesNotExist:
                message = "Given userId ({0}) does not exits in database.".format(
                    user_id
                )
                raise ValueError(message)
        else:
            message = "Given userId ({0}) is not valid object userId.".format(user_id)
            raise ValueError(message)


class UserModel(pydantic.BaseModel, extra=pydantic.Extra.forbid):
    fullname: str
    age: int
    email: str
    address: Optional[str]
    password: str

    @pydantic.validator("email")
    @classmethod
    def email_valid_check(cls, email_address) -> None:
        if email_check(email_address):
            return email_address
        else:
            message = "Given email ({0}) is not valid.".format(email_address)
            raise ValueError(message)
