from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthenticationAPITests(APITestCase):
    def test_register_user_returns_token(self):
        response = self.client.post(
            reverse("v1:register"),
            {
                "username": "newuser",
                "email": "new@example.com",
                "password": "StrongPass123!",
                "password_confirm": "StrongPass123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data["data"])
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_login_user_returns_token(self):
        get_user_model().objects.create_user(username="newuser", password="StrongPass123!")

        response = self.client.post(
            reverse("v1:login"),
            {"username": "newuser", "password": "StrongPass123!"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data["data"])
