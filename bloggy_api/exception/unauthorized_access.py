from rest_framework.exceptions import APIException


class UnauthorizedAccess(APIException):
    status_code = 401
    default_detail = "You're not authorized to perform this action."
    default_code = "unauthorized"
