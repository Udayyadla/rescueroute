from unittest.mock import patch

from django.db.utils import OperationalError
from django.test import SimpleTestCase
from rest_framework.test import APIClient

# Create your tests here.

class HealthCheckTests(SimpleTestCase):
    def setUp(self):
        self.client = APIClient()

    def test_liveness_check(self):
        response = self.client.get("/api/health/liveness")

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data["status"],"ok")
    @patch("health.views.connections")
    def test_readiness_database_failure(self, mock_connections):
        mock_connections.__getitem__.side_effect = OperationalError(
            "Database unavailable")

        response = self.client.get("/api/health")
        self.assertEqual(response.status_code,503)
        self.assertEqual(response.data["status"],"unhealthy")
