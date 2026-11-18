from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.exceptions import NotAuthenticated, PermissionDenied, NotFound


class TestDonationSerializer(serializers.Serializer):
    food_name = serializers.CharField()
    quantity = serializers.IntegerField()

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero")
        return value


class TestValidationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TestDonationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Validation passed.", "success": True})


class TestAuthenticationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        raise NotAuthenticated("Authentication Credentials were not provided.")


class TestPermissionView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        raise PermissionDenied("Only donors can perform this operation.")


class TestNotFoundView(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        raise NotFound("Donation not found.")