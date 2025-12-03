"""
Unit tests for login endpoint.
"""

from unittest.mock import patch

from django.test import TestCase
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient


class LoginEndpointTest(TestCase):
    """
    Test login endpoint with mocks.
    """

    def setUp(self):
        """
        Set up test client.
        """
        self.client = APIClient()
        self.url = "/api/auth/login/"

    @patch("apps.authentication.views.PlatformTokenObtainPairView.post")
    def test_login_success(self, mock_post):
        """
        Test successful login.
        """
        mock_response = Response(
            {
                "access": "mock_access_token",
                "refresh": "mock_refresh_token",
            },
            status=status.HTTP_200_OK,
        )
        mock_post.return_value = mock_response

        data = {
            "email": "test@example.com",
            "password": "password123",
            "platform_id": 1,
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    @patch("apps.authentication.views.PlatformTokenObtainPairView.post")
    def test_login_invalid_credentials(self, mock_post):
        """
        Test login with invalid credentials.
        """
        from rest_framework.exceptions import ValidationError

        mock_post.side_effect = ValidationError({"password": ["Credenciales inválidas."]})

        data = {
            "email": "test@example.com",
            "password": "wrongpassword",
            "platform_id": 1,
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_missing_fields(self):
        """
        Test login with missing required fields.
        """
        data = {"email": "test@example.com"}

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
