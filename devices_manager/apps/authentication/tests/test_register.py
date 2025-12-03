"""
Unit tests for register endpoint.
"""

from unittest.mock import MagicMock, patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class RegisterEndpointTest(TestCase):
    """
    Test register endpoint with mocks.
    """

    def setUp(self):
        """
        Set up test client.
        """
        self.client = APIClient()
        self.url = "/api/auth/register/"

    @patch("apps.authentication.views.RegisterSerializer")
    def test_register_success(self, mock_serializer_class):
        """
        Test successful user registration.
        """
        mock_user_platform = MagicMock(spec=["id", "email", "platform"])
        mock_user_platform.id = 1
        mock_user_platform.email = "test@example.com"
        mock_user_platform.platform.name = "Plataforma A"

        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.save.return_value = mock_user_platform
        mock_serializer_class.return_value = mock_serializer

        data = {
            "email": "test@example.com",
            "password": "password123",
            "platform_id": 1,
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Usuario registrado exitosamente.")
        self.assertEqual(response.data["user_id"], 1)
        self.assertEqual(response.data["email"], "test@example.com")

    @patch("apps.authentication.views.RegisterSerializer")
    def test_register_validation_error(self, mock_serializer_class):
        """
        Test registration with validation errors.
        """
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = False
        mock_serializer.errors = {"email": ["Este email ya está registrado."]}
        mock_serializer_class.return_value = mock_serializer

        data = {
            "email": "test@example.com",
            "password": "password123",
            "platform_id": 1,
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_register_missing_fields(self):
        """
        Test registration with missing required fields.
        """
        data = {"email": "test@example.com"}

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
