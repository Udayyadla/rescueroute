from django.test import SimpleTestCase,Client,override_settings
from django.urls import path

from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes
    )

from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import (
    ValidationError,
    NotAuthenticated,
    PermissionDenied,
    NotFound)


@api_view(["GET"])
@permission_classes([AllowAny])
def validation_error_view(request):
    raise ValidationError({
        "quantity":["Quantity must be greater than zero."]})

@api_view(["GET"])
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def authentication_error_view(request):
    raise NotAuthenticated("authentication required.")

@api_view(["GET"])
@permission_classes([AllowAny])
def permission_error_view(request):
    raise PermissionDenied("Access denied.")


@api_view(["GET"])
@permission_classes([AllowAny])
def not_found_view(request):
    raise NotFound("Donation not found.")

urlpatterns=[
    path("test-validation/",validation_error_view,),
    path("test-authentication/",authentication_error_view),
    path("test-not-found/",not_found_view),
    path("test-permission/",permission_error_view,name="test_permission_error")
   
    ]

@override_settings(
    DEBUG = False,
    ALLOWED_HOSTS = ["testserver"],
    ROOT_URLCONF = __name__,
    )

class APIContractTests(SimpleTestCase):

    def setup(self):
        self.client = Client()

    def test_validation_error(self):
        respone = self.client.get("/test-validation/")
        self.assertEqual(respone.status_code,400)

    def test_not_found_error(self):
        response = self.client.get("/test-not-found/")
        self.assertEqual(response.status_code,404)

    def test_authentication_error(self):
        response = self.client.get("/test-authentication/")    
        self.assertEqual(response.status_code,401)    

    def test_permission_error(self):
            response = self.client.get("/test-permission/")    
            self.assertEqual(response.status_code,403)

