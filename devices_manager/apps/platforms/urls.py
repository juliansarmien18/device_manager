"""
Platform URLs.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.platforms.views import PlatformViewSet

router = DefaultRouter()
router.register(r'platforms', PlatformViewSet, basename='platform')

app_name = 'platforms'

urlpatterns = [
    path('', include(router.urls)),
]

