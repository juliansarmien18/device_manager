"""
Unit tests for my_devices endpoint.
"""

from unittest.mock import MagicMock, patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class MyDevicesEndpointTest(TestCase):
    """
    Test my_devices endpoint with mocks.
    """

    def setUp(self):
        """
        Set up test client and mocks.
        """
        self.client = APIClient()
        self.url = "/api/devices/my_devices/"

        self.mock_user_platform = MagicMock()
        self.mock_user_platform.id = 1
        self.mock_user_platform.email = "test@example.com"
        self.mock_user_platform.platform.id = 1
        self.mock_user_platform.platform.name = "Plataforma A"

    @patch("apps.devices.views.DeviceViewSet.my_devices")
    def test_my_devices_success(self, mock_my_devices):
        """
        Test successful my_devices retrieval.
        """
        from rest_framework.response import Response

        mock_response = Response(
            [
                {"id": 1, "name": "Dispositivo 1", "ip_address": "192.168.1.1"},
                {"id": 2, "name": "Dispositivo 2", "ip_address": "192.168.1.2"},
            ],
            status=status.HTTP_200_OK,
        )
        mock_my_devices.return_value = mock_response

        self.client.force_authenticate(user=self.mock_user_platform)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)

    @patch("apps.devices.views.DeviceViewSet.my_devices")
    def test_my_devices_empty(self, mock_my_devices):
        """
        Test my_devices when user has no devices.
        """
        from rest_framework.response import Response

        mock_response = Response([], status=status.HTTP_200_OK)
        mock_my_devices.return_value = mock_response

        self.client.force_authenticate(user=self.mock_user_platform)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_my_devices_unauthorized(self):
        """
        Test my_devices without authentication.
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
