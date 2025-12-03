"""
Core models with audit fields.
"""

from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model with audit fields.
    Provides created_at, updated_at, created_by, and updated_by fields.
    """

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    created_by = models.ForeignKey(
        "platforms.UserPlatform",
        on_delete=models.SET_NULL,
        related_name="%(class)s_created",
        verbose_name="Creado por",
        null=True,
        blank=True,
        editable=False,
    )
    updated_by = models.ForeignKey(
        "platforms.UserPlatform",
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated",
        verbose_name="Actualizado por",
        null=True,
        blank=True,
        editable=False,
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]
