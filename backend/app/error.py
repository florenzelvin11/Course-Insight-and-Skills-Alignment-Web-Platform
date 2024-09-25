from json import dumps
from werkzeug.exceptions import HTTPException


class InputError(HTTPException):
    code = 400
    description = "No message specified"


class AccessError(HTTPException):
    code = 403
    description = "No message specified"
