from django.urls import path
from .views import (
    liveness_check,
    readiness_check,)

urlpatterns = [
    path("", readiness_check, name="readiness_check"),
    path("liveness", liveness_check, name="liveness_check"),

]
