import logging

from django.db import connections
from django.db.utils import DatabaseError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from .serializers import LivenessResponseSerializer, ReadinessResponseSerializer

# Create your views here.
logger = logging.getLogger(__name__)


@extend_schema(
    summary="Application liveness check",
    description=(
        "Checks whether the Django application " "can respond to HTTP requests."
    ),
    responses={200: LivenessResponseSerializer},
    auth=[],
)
@api_view(["GET"])
@permission_classes([AllowAny])
def liveness_check(request):
    """
    Verifies that the application process is running.
    """

    return Response(
        {
            "status": "ok",
            "service": "excess-food-backend",
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    summary="Application readiness check",
    description=(
        "Checks whether the Django application " "and can execute a lightweight query."
    ),
    responses={
        200: ReadinessResponseSerializer,
        503: OpenApiResponse(
            response=ReadinessResponseSerializer, description="Database unavailable"
        ),
    },
    auth=[],
)
@api_view(["GET"])
@permission_classes([AllowAny])
def readiness_check(request):
    """
    Verifies that the application can communicate with the database.
    """

    try:
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()

    except (DatabaseError, OSError):
        logger.exception("Database Readiness check failed")

        return Response(
            {"status": "error", "database": "unavailable"},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    return Response(
        {
            "status": "healthy",
            "database": "connected",
        },
        status=status.HTTP_200_OK,
    )
