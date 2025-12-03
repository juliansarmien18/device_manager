"""
Unit tests for create device endpoint.
"""

from unittest.mock import MagicMock, patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class CreateDeviceEndpointTest(TestCase):
    """
    Test create device endpoint with mocks.
    """

    def setUp(self):
        """
        Set up test client and mocks.
        """
        self.client = APIClient()
        self.url = "/api/devices/"

        self.mock_user_platform = MagicMock()
        self.mock_user_platform.id = 1
        self.mock_user_platform.email = "test@example.com"
        self.mock_user_platform.platform.id = 1
        self.mock_user_platform.platform.name = "Plataforma A"

    @patch("apps.devices.views.DeviceViewSet.create")
    def test_create_device_success(self, mock_create):
        """
        Test successful device creation.
        """
        from rest_framework.response import Response

        mock_response = Response(
            {
                "id": 1,
                "name": "Nuevo Dispositivo",
                "ip_address": "192.168.1.100",
                "is_active": True,
            },
            status=status.HTTP_201_CREATED,
        )
        mock_create.return_value = mock_response

        data = {
            "name": "Nuevo Dispositivo",
            "ip_address": "192.168.1.100",
            "is_active": True,
        }

        self.client.force_authenticate(user=self.mock_user_platform)
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch("apps.devices.views.DeviceViewSet.create")
    def test_create_device_validation_error(self, mock_create):
        """
        Test device creation with validation errors.
        """
        from rest_framework.response import Response

        mock_response = Response(
            {"ip_address": ["IP inválida."]},
            status=status.HTTP_400_BAD_REQUEST,
        )
        mock_create.return_value = mock_response

        data = {
            "name": "Dispositivo",
            "ip_address": "invalid_ip",
            "is_active": True,
        }

        self.client.force_authenticate(user=self.mock_user_platform)
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("ip_address", response.data)

    def test_create_device_unauthorized(self):
        """
        Test device creation without authentication.
        """
        data = {
            "name": "Dispositivo",
            "ip_address": "192.168.1.1",
            "is_active": True,
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_device_missing_fields(self):
        """
        Test device creation with missing required fields.
        """
        data = {"name": "Dispositivo"}

        self.client.force_authenticate(user=self.mock_user_platform)
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
