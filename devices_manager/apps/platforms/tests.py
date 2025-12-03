"""
Tests for platforms app.
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.platforms.models import Platform, UserPlatform


class PlatformModelTest(TestCase):
    """
    Test Platform model.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.platform = Platform.objects.create(
            name='Plataforma Test',
            description='Descripción de prueba',
            is_active=True,
        )

    def test_platform_creation(self):
        """
        Test platform creation.
        """
        self.assertEqual(self.platform.name, 'Plataforma Test')
        self.assertTrue(self.platform.is_active)
        self.assertIsNotNone(self.platform.created_at)

    def test_platform_str(self):
        """
        Test platform string representation.
        """
        self.assertEqual(str(self.platform), 'Plataforma Test')

    def test_platform_unique_name(self):
        """
        Test that platform name must be unique.
        """
        with self.assertRaises(Exception):
            Platform.objects.create(name='Plataforma Test')


class UserPlatformModelTest(TestCase):
    """
    Test UserPlatform model.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.platform = Platform.objects.create(
            name='Plataforma Test',
            is_active=True,
        )
        self.user_platform = UserPlatform.objects.create(
            email='test@example.com',
            platform=self.platform,
            password='hashed_password',
            is_active=True,
        )

    def test_user_platform_creation(self):
        """
        Test user platform creation.
        """
        self.assertEqual(self.user_platform.email, 'test@example.com')
        self.assertEqual(self.user_platform.platform, self.platform)
        self.assertTrue(self.user_platform.is_active)

    def test_user_platform_str(self):
        """
        Test user platform string representation.
        """
        expected = f'{self.user_platform.email} - {self.platform.name}'
        self.assertEqual(str(self.user_platform), expected)

    def test_user_platform_unique_email_platform(self):
        """
        Test that email+platform combination must be unique.
        """
        with self.assertRaises(Exception):
            UserPlatform.objects.create(
                email='test@example.com',
                platform=self.platform,
                password='another_password',
            )

    def test_same_email_different_platforms(self):
        """
        Test that same email can exist in different platforms.
        """
        platform2 = Platform.objects.create(name='Plataforma 2', is_active=True)
        user_platform2 = UserPlatform.objects.create(
            email='test@example.com',
            platform=platform2,
            password='hashed_password',
        )
        self.assertEqual(user_platform2.email, 'test@example.com')
        self.assertEqual(user_platform2.platform, platform2)

