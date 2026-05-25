from django.test import TestCase
from django.test import override_settings


class HealthCheckTests(TestCase):
    def test_health_check_returns_ok(self):
        response = self.client.get("/api/health/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")


@override_settings(DEBUG=True)
class DevLoginTests(TestCase):
    def test_dev_login_returns_token(self):
        response = self.client.post(
            "/api/auth/dev-login/",
            {"username": "apifox_user", "nickname": "Apifox 测试用户"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.json())

    def test_token_can_create_today_check_in(self):
        login_response = self.client.post(
            "/api/auth/dev-login/",
            {"username": "apifox_user"},
            content_type="application/json",
        )
        access = login_response.json()["access"]

        response = self.client.post(
            "/api/check-ins/today/",
            {"note": "今天完成了"},
            HTTP_AUTHORIZATION=f"Bearer {access}",
            content_type="application/json",
        )

        self.assertIn(response.status_code, [200, 201])
        self.assertEqual(response.json()["note"], "今天完成了")
