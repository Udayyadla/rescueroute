from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    ValidationError,
    NotAuthenticated,
    PermissionDenied,
    AuthenticationFailed,
    NotFound,
)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return None

    if isinstance(exc, ValidationError):
        code = "VALIDATION_ERROR"
        message = "Invalid request data."
        details = response.data

    elif isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        code = "AUTHENTICATION_ERROR"
        detail = (
            response.data.get("detail") if isinstance(response.data, dict) else None
        )
        if isinstance(detail, str):
            message = detail
        else:
            message = "Invalid or expired authentication token."
        details = None

    elif isinstance(exc, PermissionDenied):
        code = "PERMISSION_DENIED"
        message = str(exc.detail)
        details = None

    elif isinstance(exc, NotFound):
        code = "NOT_FOUND"
        message = str(exc.detail)
        details = None
    else:
        code = "API_ERROR"
        message = "An API error occurred."
        details = response.data

    response.data = {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details,
        },
    }

    return response
