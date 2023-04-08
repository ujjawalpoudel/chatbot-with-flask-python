import json


def response(status_code, body):
    """Build a standard JSON response

    Args:
        code: int: HTTP status code
        body: AnyOf [JSON serializable string, dict]: Body to serialize
    """
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
        },
        "body": body,
        "isBase64Encoded": False,
    }
