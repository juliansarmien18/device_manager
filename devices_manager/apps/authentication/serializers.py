"""
Authentication serializers.
"""

from apps.platforms.models import Platform, UserPlatform
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers


class PlatformSerializer(serializers.ModelSerializer):
    """
    Serializer for Platform model.
    """

    class Meta:
        model = Platform
        fields = ["id", "name", "description", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class UserPlatformSerializer(serializers.ModelSerializer):
    """
    Serializer for UserPlatform model.
    """

    platform = PlatformSerializer(read_only=True)
    platform_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserPlatform
        fields = [
            "id",
            "email",
            "platform",
            "platform_id",
            "is_active",
            "last_login",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "last_login", "created_at", "updated_at"]


class RegisterSerializer(serializers.Serializer):
    """
    Serializer for user registration.
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )
    platform_id = serializers.IntegerField(required=True)

    def validate_platform_id(self, value):
        """
        Validate that platform exists and is active.
        """
        try:
            platform = Platform.objects.get(id=value, is_active=True)
        except Platform.DoesNotExist:
            raise serializers.ValidationError("Plataforma no encontrada o inactiva.")
        return value

    def validate_email(self, value):
        """
        Validate email format (already handled by EmailField).
        """
        return value.lower().strip()

    def create(self, validated_data):
        """
        Create a new UserPlatform instance.
        """
        from django.contrib.auth.hashers import make_password

        email = validated_data["email"]
        password = validated_data["password"]
        platform_id = validated_data["platform_id"]

        platform = Platform.objects.get(id=platform_id)

        if UserPlatform.objects.filter(email=email, platform=platform).exists():
            raise serializers.ValidationError(
                {"email": "Este email ya está registrado en esta plataforma."}
            )

        user_platform = UserPlatform.objects.create(
            email=email,
            platform=platform,
            password=make_password(password),
            is_active=True,
        )

        return user_platform


class PlatformTokenObtainPairSerializer(serializers.Serializer):
    """
    Custom token serializer that includes platform_id in the token.
    Uses UserPlatform instead of Django User.
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    platform_id = serializers.IntegerField(required=True)

    def validate(self, attrs):
        """
        Validate credentials and generate token with platform_id.
        """
        email = attrs.get("email", "").lower().strip()
        password = attrs.get("password")
        platform_id = attrs.get("platform_id")

        try:
            platform = Platform.objects.get(id=platform_id, is_active=True)
        except Platform.DoesNotExist:
            raise serializers.ValidationError(
                {"platform_id": "Plataforma no encontrada o inactiva."}
            )

        try:
            user_platform = UserPlatform.objects.get(
                email=email,
                platform=platform,
                is_active=True,
            )
        except UserPlatform.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "Credenciales inválidas o usuario inactivo."}
            )

        from django.contrib.auth.hashers import check_password

        if not check_password(password, user_platform.password):
            raise serializers.ValidationError({"password": "Credenciales inválidas."})

        user_platform.last_login = timezone.now()
        user_platform.save(update_fields=["last_login"])

        from rest_framework_simplejwt.tokens import RefreshToken

        refresh = RefreshToken()
        refresh["user_id"] = user_platform.id
        refresh["platform_id"] = platform_id
        refresh["email"] = user_platform.email

        access = refresh.access_token
        access["user_id"] = user_platform.id
        access["platform_id"] = platform_id
        access["email"] = user_platform.email

        data = {
            "refresh": str(refresh),
            "access": str(access),
        }

        return data
