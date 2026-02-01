"""
Views for core app
"""
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import User, UserProfile
from .serializers import UserProfileSerializer, UserDetailSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update user profile
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update user details
    """
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
