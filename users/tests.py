from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class UserTests(APITestCase):
    username = "TestUser"
    email = "test@mail.ru"
    password = "TestPassword123"

    def test_create_user(self):
        """
        Test we can register a user.
        """
        url = reverse("register")
        data = {
            "username": self.username,
            "password": self.password,
            "email": self.email,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data, {"id": 1, "username": self.username, "email": self.email}
        )
        self.assertIsNotNone(User.objects.filter(username=self.username))

    def test_login_user(self):
        """
        Test user can log in.
        """
        self.test_create_user()
        url = reverse("login")
        data = {"username": self.username, "password": self.password}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        self.assertIn("token", response.data)

    def test_logout_user(self):
        """
        Test user can log out.
        """
        self.test_login_user()
        token = Token.objects.get(user__username=self.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        url = reverse("logout")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data)
