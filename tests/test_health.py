from django.test import TestCase


class HealthTests(TestCase):
    def test_liveness(self):
        response = self.client.get("/livez/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["service"], "goreecloud-social")

    def test_readiness(self):
        response = self.client.get("/readyz/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ready")

    def test_status_is_bounded_and_truthful(self):
        response = self.client.get("/api/v1/status/")
        payload = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["lifecycle"], "development")
        self.assertFalse(payload["production_ready"])
        self.assertEqual(set(payload["platform_integrations"].values()), {"blocked"})
