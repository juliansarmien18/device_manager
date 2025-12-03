"""
Platform views.
"""
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from apps.platforms.models import Platform
from apps.platforms.serializers import PlatformSerializer


class PlatformViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Platform model (read-only).
    """

    queryset = Platform.objects.filter(is_active=True)
    serializer_class = PlatformSerializer
    permission_classes = [AllowAny]

