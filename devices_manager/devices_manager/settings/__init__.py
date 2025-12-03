"""
Django settings for devices_manager project.

This file imports settings from the settings module based on environment.
Default is development settings.
"""

import os

ENVIRONMENT = os.environ.get("DJANGO_ENV", "dev")

try:
    if ENVIRONMENT == "prod":
        from .prod import *
    else:
        from .dev import *
except ImportError:
    from .base import *

    DEBUG = True
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]
