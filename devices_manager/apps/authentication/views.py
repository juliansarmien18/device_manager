"""
Authentication views.
"""

from apps.authentication.serializers import (
    PlatformTokenObtainPairSerializer,
    RegisterSerializer,
)
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


class PlatformTokenObtainPairView(TokenObtainPairView):
    """
    Custom token obtain view that requires platform_id.
    """

    serializer_class = PlatformTokenObtainPairSerializer
    permission_classes = [AllowAny]


@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):
    """
    Register a new user in a platform.
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user_platform = serializer.save()
        return Response(
            {
                "message": "Usuario registrado exitosamente.",
                "user_id": user_platform.id,
                "email": user_platform.email,
                "platform": user_platform.platform.name,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
