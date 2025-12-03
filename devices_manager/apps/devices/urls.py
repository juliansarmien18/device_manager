"""
Device URLs.
"""

from apps.devices.views import DeviceViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"devices", DeviceViewSet, basename="device")

app_name = "devices"

urlpatterns = [
    path("", include(router.urls)),
]
