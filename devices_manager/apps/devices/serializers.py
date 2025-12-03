"""
Device serializers.
"""
from rest_framework import serializers
from apps.devices.models import Device
from apps.platforms.models import UserPlatform


class DeviceSerializer(serializers.ModelSerializer):
    """
    Serializer for Device model.
    """

    user_platform_email = serializers.EmailField(source='user_platform.email', read_only=True)
    platform_name = serializers.CharField(source='user_platform.platform.name', read_only=True)

    class Meta:
        model = Device
        fields = [
            'id',
            'name',
            'ip_address',
            'is_active',
            'user_platform_email',
            'platform_name',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'user_platform_email',
            'platform_name',
            'created_at',
            'updated_at',
        ]

    def validate_ip_address(self, value):
        """
        Validate IP address format.
        """
        if not value:
            raise serializers.ValidationError('La dirección IP es requerida.')
        return value

    def validate_name(self, value):
        """
        Validate device name.
        """
        if not value or not value.strip():
            raise serializers.ValidationError('El nombre del dispositivo es requerido.')
        return value.strip()

    def create(self, validated_data):
        """
        Create device instance.
        user_platform is passed from perform_create via context.
        """
        user_platform = self.context.get('user_platform')
        if not user_platform:
            raise serializers.ValidationError('user_platform es requerido.')
        
        device = Device.objects.create(
            user_platform=user_platform,
            created_by=user_platform,
            updated_by=user_platform,
            **validated_data
        )
        return device

