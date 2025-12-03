"""
Device views.
"""

from apps.devices.models import Device
from apps.devices.serializers import DeviceSerializer
from apps.platforms.models import UserPlatform
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class DeviceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Device model.
    Returns only devices belonging to the authenticated user in their current platform.
    """

    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "ip_address"]
    ordering_fields = ["name", "created_at", "updated_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """
        Filter devices by authenticated user_platform.
        """
        user_platform = self.request.user
        if isinstance(user_platform, UserPlatform):
            return Device.objects.filter(
                user_platform=user_platform,
                user_platform__platform=user_platform.platform,
            )
        return Device.objects.none()

    def perform_create(self, serializer):
        """
        Set user_platform when creating a device.
        """
        user_platform = self.request.user
        if not isinstance(user_platform, UserPlatform):
            raise ValueError("Usuario no válido para crear dispositivo.")

        serializer.context["user_platform"] = user_platform
        serializer.save()

    def perform_update(self, serializer):
        """
        Set updated_by when updating a device.
        """
        user_platform = self.request.user
        if isinstance(user_platform, UserPlatform):
            serializer.save(updated_by=user_platform)
        else:
            serializer.save()

    @action(detail=False, methods=["get"])
    def my_devices(self, request):
        """
        Custom endpoint to get current user's devices.
        """
        user_platform = request.user
        if not isinstance(user_platform, UserPlatform):
            return Response(
                {"error": "Usuario no válido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        devices = Device.objects.filter(
            user_platform=user_platform,
            user_platform__platform=user_platform.platform,
        )
        serializer = self.get_serializer(devices, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"])
    def toggle_active(self, request, pk=None):
        """
        Toggle device active status.
        """
        device = self.get_object()
        user_platform = request.user
        if isinstance(user_platform, UserPlatform):
            device.updated_by = user_platform
        device.is_active = not device.is_active
        device.save()
        serializer = self.get_serializer(device)
        return Response(serializer.data)
