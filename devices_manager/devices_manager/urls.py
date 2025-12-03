"""
URL configuration for devices_manager project.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.authentication.urls")),
    path("api/", include("apps.platforms.urls")),
    path("api/", include("apps.devices.urls")),
]
