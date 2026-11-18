from django.urls import path
from .views import liveness_check, readiness_check,test_server_error

urlpatterns = [
    path("", readiness_check, name="readiness_check"),
    path("liveness", liveness_check, name="liveness_check"),
    path("test-server-error", test_server_error, name="test_server_error"),
]
