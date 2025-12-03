"""
Admin configuration for platforms app.
"""

from apps.platforms.models import Platform, UserPlatform
from django.contrib import admin


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    """
    Admin configuration for Platform model.
    """

    list_display = ["name", "description", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "description"]
    readonly_fields = ["created_at", "updated_at", "created_by", "updated_by"]


@admin.register(UserPlatform)
class UserPlatformAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserPlatform model.
    """

    list_display = ["email", "platform", "is_active", "last_login", "created_at"]
    list_filter = ["platform", "is_active", "created_at"]
    search_fields = ["email", "platform__name"]
    readonly_fields = ["last_login", "created_at", "updated_at", "created_by", "updated_by"]
    filter_horizontal = []
