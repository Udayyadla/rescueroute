from django.urls import path
from config.urls import urlpatterns as production_urls
from .test_error_views import (
    test_server_error,
    test_django_server,
)

urlpatterns = [
    path("api/health/test-server-error", test_server_error, name="test_server_error"),
    path("api/health/test-django-error", test_django_server, name="test-django-error"),
    *production_urls,
]

# Preserve the production HTTP 500 handler
# When using this test-only ROOT_URLCONF
handler500 = "config.error_views.server_error"
