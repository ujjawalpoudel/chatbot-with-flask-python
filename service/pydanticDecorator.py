from functools import wraps
import json

from pydantic import ValidationError
from service.response import response


def pydantic_validation(model_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                if args[0]["httpMethod"] == "GET":
                    parameters = args[0]["queryStringParameters"]
                    if parameters is not None:
                        data = args[0]["queryStringParameters"]
                    else:
                        data = {}
                else:
                    data = json.loads(args[0]["body"])
                model_name(**data)
                return f(*args, **kwargs)
            except ValidationError as e:
                print("Error at pydantic_validation:- ", e)
                errors = []
                errors_list = json.loads(e.json())
                for error in errors_list:
                    errors.append({"attribute": error["loc"][0], "msg": error["msg"]})
            response_body = {
                "errors": errors,
                "status": False,
                "message": "Validation Error",
            }
            return response(400, response_body)

        return decorated_function

    return decorator
