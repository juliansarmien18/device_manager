"""
Platform serializers.
"""
from rest_framework import serializers
from apps.platforms.models import Platform


class PlatformSerializer(serializers.ModelSerializer):
    """
    Serializer for Platform model.
    """

    class Meta:
        model = Platform
        fields = ['id', 'name', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

