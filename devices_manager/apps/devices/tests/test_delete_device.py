"""
Unit tests for delete device endpoint.
"""

from unittest.mock import MagicMock, patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class DeleteDeviceEndpointTest(TestCase):
    """
    Test delete device endpoint with mocks.
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

    @patch("apps.devices.views.DeviceViewSet.destroy")
    def test_delete_device_success(self, mock_destroy):
        """
        Test successful device deletion.
        """
        from rest_framework.response import Response

        mock_response = Response(status=status.HTTP_204_NO_CONTENT)
        mock_destroy.return_value = mock_response

        self.client.force_authenticate(user=self.mock_user_platform)
        response = self.client.delete("/api/devices/1/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch("apps.devices.views.DeviceViewSet.destroy")
    def test_delete_device_not_found(self, mock_destroy):
        """
        Test device deletion when device does not exist.
        """
        from rest_framework.exceptions import NotFound
        from rest_framework.response import Response

        mock_destroy.side_effect = NotFound()
        mock_destroy.return_value = Response(
            {"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND
        )

        self.client.force_authenticate(user=self.mock_user_platform)
        response = self.client.delete("/api/devices/999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_device_unauthorized(self):
        """
        Test device deletion without authentication.
        """
        response = self.client.delete("/api/devices/1/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
