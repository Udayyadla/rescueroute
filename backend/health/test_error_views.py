import logging

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from django.http import JsonResponse
# Create your views here.
logger = logging.getLogger(__name__)


def test_django_server(request):
    total_donations = 100
    completed_donations = 0
    percentage = (total_donations/completed_donations) * 100
    return JsonResponse({
        "percentage":percentage})

@api_view(["GET"])
@permission_classes([AllowAny])
def test_server_error(request):
    """
    Endpoint to test server error handling.
    """

    total_food = 100
    delievered_food = 0

    percentage = (total_food / delievered_food) * 100  # This will raise a ZeroDivisionError
    return Response(
        {
            "message": f"Percentage of delivered food: {percentage}%",
        })