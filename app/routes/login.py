# * Import Python Module
import json
from flask import Blueprint, request
from mongoengine import DoesNotExist


# * Import Patient Defined Functions
from app.validators.models.loginValidators import LoginModel
from service.pydanticDecorator import pydantic_validation
from app.models.chatbotDbModel import User
from utils.passwordHash import check_password, hash_password
from service.response import response


# * Define Blueprint for API Routes
login_module = Blueprint("login_module", __name__)


# * Define API Route for Login
@login_module.route("/login", methods=["POST"], endpoint="login")
@pydantic_validation(LoginModel)
def login():
    try:
        # * Get Data from Frontend
        data = json.loads(request.data)

        email = data["email"]
        password = data["password"]

        # * Get Data from Mongodb
        user = User.objects.get(email=email)

        # Check if a password matches the hashed password
        if check_password(password, user.password):
            return response(302, {"msg": "Successfully Login"})
        else:
            return response(401, {"msg": "Invalid password"})
    except DoesNotExist:
        return response(401, {"msg": "Invalid Email Address"})
