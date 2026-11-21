import logging
from django.http import JsonResponse

logger = logging.getLogger("health")


def server_error(request):
    return JsonResponse(
        {
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An internal server error occurred.",
                "details": None,
            },
            
        },
        status= 500
    )