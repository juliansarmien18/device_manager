"""
Admin configuration for devices app.
"""

from apps.devices.models import Device
from django.contrib import admin


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    """
    Admin configuration for Device model.
    """

    list_display = ["name", "ip_address", "is_active", "user_platform", "created_at"]
    list_filter = ["is_active", "created_at", "user_platform__platform"]
    search_fields = ["name", "ip_address", "user_platform__email"]
    readonly_fields = ["created_at", "updated_at", "created_by", "updated_by"]
