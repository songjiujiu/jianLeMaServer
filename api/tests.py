from django.test import TestCase
from django.test import override_settings

from .models import HealthGoal


class HealthCheckTests(TestCase):
    def test_health_check_returns_ok(self):
        response = self.client.get("/api/health/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_create_health_goal_writes_to_database(self):
        response = self.client.post(
            "/api/create_health_goal/",
            {"name": "Zhang San", "age": "18"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["data"]["name"], "Zhang San")
        self.assertEqual(HealthGoal.objects.count(), 1)
        self.assertEqual(HealthGoal.objects.first().age, 18)


@override_settings(DEBUG=True)
class DevLoginTests(TestCase):
    def test_dev_login_returns_token(self):
        response = self.client.post(
            "/api/auth/dev-login/",
            {"username": "apifox_user", "nickname": "Apifox Test User"},
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
            {"note": "done today"},
            HTTP_AUTHORIZATION=f"Bearer {access}",
            content_type="application/json",
        )

        self.assertIn(response.status_code, [200, 201])
        self.assertEqual(response.json()["note"], "done today")

    def test_token_can_create_and_list_goal(self):
        login_response = self.client.post(
            "/api/auth/dev-login/",
            {"username": "apifox_user"},
            content_type="application/json",
        )
        access = login_response.json()["access"]

        create_response = self.client.post(
            "/api/goals/",
            {"title": "Learn Python", "description": "Practice Django ORM"},
            HTTP_AUTHORIZATION=f"Bearer {access}",
            content_type="application/json",
        )

        self.assertEqual(create_response.status_code, 201)
        self.assertEqual(create_response.json()["title"], "Learn Python")

        list_response = self.client.get(
            "/api/goals/",
            HTTP_AUTHORIZATION=f"Bearer {access}",
        )

        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(list_response.json()["items"]), 1)
        self.assertEqual(list_response.json()["items"][0]["title"], "Learn Python")
