"""
Unit tests for get device endpoint.
"""

from unittest.mock import MagicMock, patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class GetDeviceEndpointTest(TestCase):
    """
    Test get device endpoint with mocks.
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

    @patch("apps.devices.views.DeviceViewSet.retrieve")
    def test_get_device_success(self, mock_retrieve):
        """
        Test successful device retrieval.
        """
        from rest_framework.response import Response

        mock_response = Response(
            {
                "id": 1,
                "name": "Dispositivo 1",
                "ip_address": "192.168.1.1",
                "is_active": True,
            },
            status=status.HTTP_200_OK,
        )
        mock_retrieve.return_value = mock_response

        self.client.force_authenticate(user=self.mock_user_platform)
        response = self.client.get("/api/devices/1/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], 1)

    @patch("apps.devices.views.DeviceViewSet.retrieve")
    def test_get_device_not_found(self, mock_retrieve):
        """
        Test device retrieval when device does not exist.
        """
        from rest_framework.exceptions import NotFound
        from rest_framework.response import Response

        mock_retrieve.side_effect = NotFound()
        mock_retrieve.return_value = Response(
            {"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND
        )

        self.client.force_authenticate(user=self.mock_user_platform)
        response = self.client.get("/api/devices/999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_device_unauthorized(self):
        """
        Test device retrieval without authentication.
        """
        response = self.client.get("/api/devices/1/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
