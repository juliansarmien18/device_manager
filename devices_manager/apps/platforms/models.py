"""
Platform models.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import EmailValidator
from apps.core.models import BaseModel


class Platform(BaseModel):
    """
    Platform model representing different platforms in the system.
    """

    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    is_active = models.BooleanField(default=True, verbose_name='Activa')

    class Meta:
        verbose_name = 'Plataforma'
        verbose_name_plural = 'Plataformas'
        ordering = ['name']

    def __str__(self):
        return self.name


class UserPlatform(BaseModel):
    """
    Relationship model between User and Platform.
    Allows the same user (email) to be registered in multiple platforms.
    Implements Django user-like interface for authentication.
    """

    email = models.EmailField(
        max_length=255,
        validators=[EmailValidator()],
        verbose_name='Email',
        db_index=True,
    )
    platform = models.ForeignKey(
        Platform,
        on_delete=models.CASCADE,
        related_name='user_platforms',
        verbose_name='Plataforma',
    )
    password = models.CharField(max_length=128, verbose_name='Contraseña')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    last_login = models.DateTimeField(null=True, blank=True, verbose_name='Último acceso')

    class Meta:
        verbose_name = 'Usuario de Plataforma'
        verbose_name_plural = 'Usuarios de Plataforma'
        unique_together = [['email', 'platform']]
        indexes = [
            models.Index(fields=['email', 'platform']),
        ]

    def __str__(self):
        return f'{self.email} - {self.platform.name}'

    is_authenticated = True
    is_anonymous = False

    def get_username(self):
        """
        Return the email as username.
        """
        return self.email

    @property
    def username(self):
        """
        Alias for email to maintain compatibility.
        """
        return self.email

    def check_password(self, raw_password):
        """
        Check password using Django's password hasher.
        """
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)

    def set_password(self, raw_password):
        """
        Set password using Django's password hasher.
        """
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)

