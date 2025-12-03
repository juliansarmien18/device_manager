"""
Platform URLs.
"""

from apps.platforms.views import PlatformViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"platforms", PlatformViewSet, basename="platform")

app_name = "platforms"

urlpatterns = [
    path("", include(router.urls)),
]
