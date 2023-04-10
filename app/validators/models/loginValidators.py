import pydantic

from utils.validationCheck import email_check


class LoginModel(pydantic.BaseModel, extra=pydantic.Extra.forbid):
    email: str
    password: str

    @pydantic.validator("email")
    @classmethod
    def email_valid_check(cls, email_address) -> None:
        if email_check(email_address):
            return email_address
        else:
            message = "Given email ({0}) is not valid.".format(email_address)
            raise ValueError(message)
