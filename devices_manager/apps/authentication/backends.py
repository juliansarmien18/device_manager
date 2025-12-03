"""
Custom authentication backends.
"""

from apps.platforms.models import Platform, UserPlatform
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken


class PlatformJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication that validates platform from token.
    """

    def get_validated_token(self, raw_token):
        """
        Validates the token and ensures it contains platform_id.
        """
        validated_token = super().get_validated_token(raw_token)
        if "platform_id" not in validated_token:
            raise InvalidToken("Token does not contain platform_id")
        return validated_token

    def get_user(self, validated_token):
        """
        Returns the user_platform instance based on the token.
        Ensures Django user-like attributes are set.
        """
        try:
            user_id = validated_token["user_id"]
            platform_id = validated_token["platform_id"]

            platform = Platform.objects.get(id=platform_id, is_active=True)

            user_platform = UserPlatform.objects.get(
                id=user_id,
                platform=platform,
                is_active=True,
            )

            if not hasattr(user_platform, "is_authenticated"):
                user_platform.is_authenticated = True
            if not hasattr(user_platform, "is_anonymous"):
                user_platform.is_anonymous = False

            return user_platform
        except (Platform.DoesNotExist, UserPlatform.DoesNotExist, KeyError) as e:
            raise AuthenticationFailed("Invalid token or user not found") from e
