"""
Unit tests for update device endpoint.
"""

from unittest.mock import MagicMock, patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class UpdateDeviceEndpointTest(TestCase):
    """
    Test update device endpoint with mocks.
    """

    def setUp(self):
        """
        Set up test client and mocks.
        """
        self.client = APIClient()

        self.mock_user_platform = MagicMock()
        self.mock_user_platform.id = 1
        self.mock_user_platform.email = "test@example.com"
        self.mock_user_platform.platform.id = 1
        self.mock_user_platform.platform.name = "Plataforma A"

    @patch("apps.devices.views.DeviceViewSet.partial_update")
    def test_update_device_success(self, mock_partial_update):
        """
        Test successful device update.
        """
        from rest_framework.response import Response

        mock_response = Response(
            {
                "id": 1,
                "name": "Dispositivo Actualizado",
                "ip_address": "192.168.1.1",
                "is_active": False,
            },
            status=status.HTTP_200_OK,
        )
        mock_partial_update.return_value = mock_response

        data = {
            "name": "Dispositivo Actualizado",
            "is_active": False,
        }

        self.client.force_authenticate(user=self.mock_user_platform)
        response = self.client.patch("/api/devices/1/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Dispositivo Actualizado")

    @patch("apps.devices.views.DeviceViewSet.partial_update")
    def test_update_device_validation_error(self, mock_partial_update):
        """
        Test device update with validation errors.
        """
        from rest_framework.response import Response

        mock_response = Response(
            {"ip_address": ["IP inválida."]},
            status=status.HTTP_400_BAD_REQUEST,
        )
        mock_partial_update.return_value = mock_response

        data = {
            "ip_address": "invalid_ip",
        }

        self.client.force_authenticate(user=self.mock_user_platform)
        response = self.client.patch("/api/devices/1/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_device_unauthorized(self):
        """
        Test device update without authentication.
        """
        data = {"name": "Dispositivo Actualizado"}

        response = self.client.patch("/api/devices/1/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
