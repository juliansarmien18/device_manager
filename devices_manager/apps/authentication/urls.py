"""
Authentication URLs.
"""
from django.urls import path
from apps.authentication.views import PlatformTokenObtainPairView, register_view

app_name = 'authentication'

urlpatterns = [
    path('login/', PlatformTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', register_view, name='register'),
]

