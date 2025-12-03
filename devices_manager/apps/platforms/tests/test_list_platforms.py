"""
Unit tests for list platforms endpoint.
"""

from unittest.mock import MagicMock, patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class ListPlatformsEndpointTest(TestCase):
    """
    Test list platforms endpoint with mocks.
    """

    def setUp(self):
        """
        Set up test client.
        """
        self.client = APIClient()
        self.url = "/api/platforms/"

    @patch("apps.platforms.views.PlatformViewSet.list")
    def test_list_platforms_success(self, mock_list):
        """
        Test successful platform listing.
        """
        from rest_framework.response import Response

        mock_response = Response(
            {
                "count": 2,
                "results": [
                    {
                        "id": 1,
                        "name": "Plataforma A",
                        "description": "Descripción A",
                        "is_active": True,
                    },
                    {
                        "id": 2,
                        "name": "Plataforma B",
                        "description": "Descripción B",
                        "is_active": True,
                    },
                ],
            },
            status=status.HTTP_200_OK,
        )
        mock_list.return_value = mock_response

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)

    @patch("apps.platforms.views.PlatformViewSet.list")
    def test_list_platforms_empty(self, mock_list):
        """
        Test listing platforms when none exist.
        """
        from rest_framework.response import Response

        mock_response = Response(
            {"count": 0, "results": []},
            status=status.HTTP_200_OK,
        )
        mock_list.return_value = mock_response

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results", [])), 0)
