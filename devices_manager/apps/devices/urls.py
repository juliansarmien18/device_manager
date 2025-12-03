"""
Device URLs.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.devices.views import DeviceViewSet

router = DefaultRouter()
router.register(r'devices', DeviceViewSet, basename='device')

app_name = 'devices'

urlpatterns = [
    path('', include(router.urls)),
]

