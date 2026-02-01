"""
URL configuration for core app
"""
from django.urls import path
from .views import UserProfileView, UserDetailView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('me/', UserDetailView.as_view(), name='user-detail'),
]
