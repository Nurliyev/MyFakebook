from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from profiles.models import User


class BaseTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            email="user@email.com",
            username="user",
            password="password",
            is_active=True,
        )

        self.client = Client()
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.user = {
            "username": "username",
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "hyperygty@gmail.com",
            "password": "testpassword",
            "password2": "testpassword",
        }

        return super().setUp()


class RegisterTest(BaseTest):
    def test_registration_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/register.html")

    def test_can_register_user(self):
        response = self.client.post(self.register_url, self.user, follow=True)
        self.assertEqual(response.status_code, 200)


class LoginTest(BaseTest):
    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/login.html")

    def test_login_post(self):
        data = {
            "username": "user",
            "password": "password"
        }
        response = self.client.post(self.login_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/post-list.html")
