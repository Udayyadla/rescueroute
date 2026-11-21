from django.test import Client, SimpleTestCase, override_settings



@override_settings(
    DEBUG=False,
    DEBUG_PROPAGATE_EXCEPTIONS=False,
    ALLOWED_HOSTS=["testserver"],
    ROOT_URLCONF = "health.test_urls"
)
class ProductionErrorTests(SimpleTestCase):

    def setUp(self):
        self.client = Client(raise_request_exception=False)
        self.url = "/api/health/test-server-error"

    def test_http_500_is_json(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 500)

        self.assertEqual(
            response["Content-Type"],
            "application/json"
        )

    def test_error_response_structure(self): # OK
        response = self.client.get(self.url)

        expected = {
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An internal server error occurred.",
                "details": None,
            }
        }

        self.assertEqual(response.json(), expected)

    def test_no_sensitive_details_exposed(self):
        response = self.client.get(self.url)

        body = response.content.decode("utf-8")

        self.assertNotIn("Traceback", body)
        self.assertNotIn("ZeroDivisionError", body)
        self.assertNotIn("health/views.py", body)
        self.assertNotIn("health\\\\views.py", body)

    def test_exception_logged(self):
        with self.assertLogs(
            "django.request", level="ERROR"
        ) as captured:
            response = self.client.get(self.url)

        self.assertEqual(response.status_code, 500)

        logs = "\n".join(captured.output)

        self.assertIn("ZeroDivisionError", logs)
        self.assertIn("division by zero", logs)

    def test_not_found_remains_404(self):
        response = self.client.get(
            "/api/health/endpoint-does-not-exist"
        )

        self.assertEqual(response.status_code, 404)

    def test_regular_django_view_returns_json_500(self):
        response = self.client.get("/api/health/test-django-error")
        self.assertEqual(response.status_code,500)
        self.assertEqual(
            response["Content-type"],"application/json")
        self.assertEqual(response.json()["error"]["code"],"INTERNAL_SERVER_ERROR")

    def test_error_response_does_not_expose_traceback(self): # OK
        response = self.client.get("/api/health/test-django-error")
        body = response.content.decode("utf-8")
        self.assertEqual(response.status_code,500)
        self.assertNotIn("ZeroDivisionError",body)
        self.assertNotIn("Traceback",body)
        self.assertNotIn("division by zero", body)


    def test_html_accept_header_still_returns_json(self):
        response = self.client.get("/api/health/test-django-error",HTTP_ACCEPT="text/html")
        self.assertEqual(response.status_code,500)
        self.assertEqual(response["Content-Type"],"application/json")
        
        