"""
Unit tests for toggle_active endpoint.
"""

from unittest.mock import MagicMock, patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class ToggleActiveEndpointTest(TestCase):
    """
    Test toggle_active endpoint with mocks.
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

    @patch("apps.devices.views.DeviceViewSet.toggle_active")
    def test_toggle_active_success(self, mock_toggle_active):
        """
        Test successful device active status toggle.
        """
        from rest_framework.response import Response

        mock_response = Response(
            {
                "id": 1,
                "name": "Dispositivo 1",
                "is_active": False,
            },
            status=status.HTTP_200_OK,
        )
        mock_toggle_active.return_value = mock_response

        self.client.force_authenticate(user=self.mock_user_platform)
        response = self.client.patch("/api/devices/1/toggle_active/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["is_active"], False)

    @patch("apps.devices.views.DeviceViewSet.toggle_active")
    def test_toggle_active_not_found(self, mock_toggle_active):
        """
        Test toggle_active when device does not exist.
        """
        from rest_framework.exceptions import NotFound
        from rest_framework.response import Response

        mock_toggle_active.side_effect = NotFound()
        mock_toggle_active.return_value = Response(
            {"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND
        )

        self.client.force_authenticate(user=self.mock_user_platform)
        response = self.client.patch("/api/devices/999/toggle_active/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_toggle_active_unauthorized(self):
        """
        Test toggle_active without authentication.
        """
        response = self.client.patch("/api/devices/1/toggle_active/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
