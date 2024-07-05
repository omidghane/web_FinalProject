# your_app/tests/test_views.py

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.models import CustomUser


def login(self):
    url = reverse("token_obtain_pair")
    data = {
        "email": "testuser@example.com",
        "password": "testpassword123",
    }
    response = self.client.post(url, data, format="json")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    return response.data["access"], response.data["refresh"]


class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123",
        )

    def test_user_register_view(self):
        url = reverse("user-register")
        data = {
            "username": "newuser",
            "password": "newpassword123",
            "email": "newuser@example.com",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "newuser")

    def test_user_login_view(self):
        url = reverse("token_obtain_pair")
        data = {
            "email": "testuser@example.com",
            "password": "testpassword123",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.access_token = response.data["access"]
        self.refresh_token = response.data["refresh"]

    def test_forget_password_view(self):
        url = reverse("user-forget-password")
        data = {"email": self.user.email}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_view(self):
        url = reverse("user-reset-password")
        access, _ = login(self)
        data = {"password": "newpassword123"}
        response = self.client.post(
            url, data, format="json", headers={"Authorization": f"Bearer {access}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpassword123"))

    def test_change_password_view(self):
        url = reverse("user-change-password")
        data = {"password": "newpassword123"}
        access, _ = login(self)

        response = self.client.post(
            url, data, format="json", headers={"Authorization": f"Bearer {access}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpassword123"))

    def test_change_email_view(self):
        url = reverse("user-change-email")
        data = {"id": self.user.id, "email": "newemail@example.com"}
        access, _ = login(self)
        response = self.client.post(
            url, data, format="json", headers={"Authorization": f"Bearer {access}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "newemail@example.com")

    def test_change_username_view(self):
        url = reverse("user-change-username")
        data = {"id": self.user.id, "username": "newusername"}
        access, _ = login(self)
        response = self.client.post(
            url, data, format="json", headers={"Authorization": f"Bearer {access}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "newusername")

    def test_logout_view(self):
        url = reverse("user-logout")
        access, refresh = login(self)
        data = {"refresh_token": str(refresh)}
        response = self.client.post(
            url, data, format="json", headers={"Authorization": f"Bearer {access}"}
        )
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_delete_user_view(self):
        url = reverse("user-delete-user")
        access, refresh = login(self)
        response = self.client.post(
            url, format="json", headers={"Authorization": f"Bearer {access}"}
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_deleted)
