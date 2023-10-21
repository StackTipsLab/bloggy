from rest_framework.exceptions import APIException


class NotFoundException(APIException):
    status_code = 400
    default_detail = "Content not found"
    default_code = "bad_request"
