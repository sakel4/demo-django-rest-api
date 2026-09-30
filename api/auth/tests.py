from django.test import SimpleTestCase
from django.urls import reverse


class HealthCheckTests(SimpleTestCase):
    def test_health_check_returns_ok(self):
        response = self.client.get(reverse("auth-health"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"status": "ok", "message": "Auth API is reachable."},
        )

    def test_health_check_only_allows_get(self):
        response = self.client.post(reverse("auth-health"))

        self.assertEqual(response.status_code, 405)
