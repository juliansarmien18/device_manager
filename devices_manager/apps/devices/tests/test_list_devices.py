"""
Unit tests for list devices endpoint.
"""

from unittest.mock import MagicMock, patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class ListDevicesEndpointTest(TestCase):
    """
    Test list devices endpoint with mocks.
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

    @patch("apps.devices.views.DeviceViewSet.list")
    def test_list_devices_success(self, mock_list):
        """
        Test successful device listing.
        """
        from rest_framework.response import Response

        mock_response = Response(
            {
                "count": 2,
                "results": [
                    {
                        "id": 1,
                        "name": "Dispositivo 1",
                        "ip_address": "192.168.1.1",
                        "is_active": True,
                    },
                    {
                        "id": 2,
                        "name": "Dispositivo 2",
                        "ip_address": "192.168.1.2",
                        "is_active": True,
                    },
                ],
            },
            status=status.HTTP_200_OK,
        )
        mock_list.return_value = mock_response

        self.client.force_authenticate(user=self.mock_user_platform)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_devices_unauthorized(self):
        """
        Test listing devices without authentication.
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
