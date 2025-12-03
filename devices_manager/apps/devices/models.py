"""
Device models.
"""

from apps.core.models import BaseModel
from apps.platforms.models import UserPlatform
from django.core.validators import validate_ipv4_address
from django.db import models


class Device(BaseModel):
    """
    Device model representing devices associated with a user in a platform.
    """

    name = models.CharField(max_length=200, verbose_name="Nombre del dispositivo")
    ip_address = models.GenericIPAddressField(
        protocol="IPv4",
        validators=[validate_ipv4_address],
        verbose_name="Dirección IP",
    )
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    user_platform = models.ForeignKey(
        UserPlatform,
        on_delete=models.CASCADE,
        related_name="devices",
        verbose_name="Usuario de Plataforma",
    )

    class Meta:
        verbose_name = "Dispositivo"
        verbose_name_plural = "Dispositivos"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["user_platform", "is_active"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.ip_address})"
