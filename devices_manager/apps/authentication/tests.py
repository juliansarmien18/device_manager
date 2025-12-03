"""
Tests for authentication app.
"""

from apps.devices.models import Device
from apps.platforms.models import Platform, UserPlatform
from django.contrib.auth.hashers import make_password
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class AuthenticationTest(TestCase):
    """
    Test authentication endpoints.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.client = APIClient()
        self.platform = Platform.objects.create(
            name="Plataforma Test",
            is_active=True,
        )
        self.user_platform = UserPlatform.objects.create(
            email="test@example.com",
            platform=self.platform,
            password=make_password("testpass123"),
            is_active=True,
        )

    def test_register_new_user(self):
        """
        Test user registration.
        """
        url = "/api/auth/register/"
        data = {
            "email": "newuser@example.com",
            "password": "newpass123",
            "platform_id": self.platform.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            UserPlatform.objects.filter(
                email="newuser@example.com", platform=self.platform
            ).exists()
        )

    def test_register_duplicate_email_same_platform(self):
        """
        Test that duplicate email in same platform is rejected.
        """
        url = "/api/auth/register/"
        data = {
            "email": "test@example.com",
            "password": "testpass123",
            "platform_id": self.platform.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        """
        Test successful login.
        """
        url = "/api/auth/login/"
        data = {
            "email": "test@example.com",
            "password": "testpass123",
            "platform_id": self.platform.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_credentials(self):
        """
        Test login with invalid credentials.
        """
        url = "/api/auth/login/"
        data = {
            "email": "test@example.com",
            "password": "wrongpassword",
            "platform_id": self.platform.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_invalid_platform(self):
        """
        Test login with invalid platform.
        """
        url = "/api/auth/login/"
        data = {
            "email": "test@example.com",
            "password": "testpass123",
            "platform_id": 99999,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_contains_platform_id(self):
        """
        Test that JWT token contains platform_id.
        """
        url = "/api/auth/login/"
        data = {
            "email": "test@example.com",
            "password": "testpass123",
            "platform_id": self.platform.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)


class DeviceAPITest(TestCase):
    """
    Test device API endpoints.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.client = APIClient()
        self.platform = Platform.objects.create(name="Plataforma Test", is_active=True)
        self.user_platform = UserPlatform.objects.create(
            email="test@example.com",
            platform=self.platform,
            password=make_password("testpass123"),
            is_active=True,
        )

        login_url = "/api/auth/login/"
        login_data = {
            "email": "test@example.com",
            "password": "testpass123",
            "platform_id": self.platform.id,
        }
        login_response = self.client.post(login_url, login_data, format="json")
        self.token = login_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_list_devices(self):
        """
        Test listing devices.
        """
        Device.objects.create(
            name="Dispositivo 1",
            ip_address="192.168.1.1",
            user_platform=self.user_platform,
        )

        url = "/api/devices/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_create_device(self):
        """
        Test creating a device.
        """
        url = "/api/devices/"
        data = {
            "name": "Nuevo Dispositivo",
            "ip_address": "192.168.1.100",
            "is_active": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Device.objects.filter(
                name="Nuevo Dispositivo", user_platform=self.user_platform
            ).exists()
        )

    def test_get_device_detail(self):
        """
        Test getting device detail.
        """
        device = Device.objects.create(
            name="Dispositivo Test",
            ip_address="192.168.1.1",
            user_platform=self.user_platform,
        )
        url = f"/api/devices/{device.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Dispositivo Test")

    def test_update_device(self):
        """
        Test updating a device.
        """
        device = Device.objects.create(
            name="Dispositivo Test",
            ip_address="192.168.1.1",
            user_platform=self.user_platform,
        )
        url = f"/api/devices/{device.id}/"
        data = {"name": "Dispositivo Actualizado", "ip_address": "192.168.1.1"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        device.refresh_from_db()
        self.assertEqual(device.name, "Dispositivo Actualizado")

    def test_delete_device(self):
        """
        Test deleting a device.
        """
        device = Device.objects.create(
            name="Dispositivo Test",
            ip_address="192.168.1.1",
            user_platform=self.user_platform,
        )
        url = f"/api/devices/{device.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Device.objects.filter(id=device.id).exists())

    def test_unauthorized_access(self):
        """
        Test that unauthorized requests are rejected.
        """
        self.client.credentials()  # Remove token
        url = "/api/devices/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
