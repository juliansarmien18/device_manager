"""
Tests for devices app.
"""

from apps.devices.models import Device
from apps.platforms.models import Platform, UserPlatform
from django.test import TestCase


class DeviceModelTest(TestCase):
    """
    Test Device model.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.platform = Platform.objects.create(name="Plataforma Test", is_active=True)
        self.user_platform = UserPlatform.objects.create(
            email="test@example.com",
            platform=self.platform,
            password="hashed_password",
            is_active=True,
        )
        self.device = Device.objects.create(
            name="Dispositivo Test",
            ip_address="192.168.1.1",
            is_active=True,
            user_platform=self.user_platform,
        )

    def test_device_creation(self):
        """
        Test device creation.
        """
        self.assertEqual(self.device.name, "Dispositivo Test")
        self.assertEqual(self.device.ip_address, "192.168.1.1")
        self.assertTrue(self.device.is_active)
        self.assertEqual(self.device.user_platform, self.user_platform)

    def test_device_str(self):
        """
        Test device string representation.
        """
        expected = f"{self.device.name} ({self.device.ip_address})"
        self.assertEqual(str(self.device), expected)

    def test_device_deletion_cascade(self):
        """
        Test that device is deleted when user_platform is deleted.
        """
        device_id = self.device.id
        self.user_platform.delete()
        self.assertFalse(Device.objects.filter(id=device_id).exists())
