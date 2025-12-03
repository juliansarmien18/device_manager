"""
Authentication URLs.
"""

from apps.authentication.views import PlatformTokenObtainPairView, register_view
from django.urls import path

app_name = "authentication"

urlpatterns = [
    path("login/", PlatformTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("register/", register_view, name="register"),
]
