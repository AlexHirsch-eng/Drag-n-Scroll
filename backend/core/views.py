"""
Views for core app
"""
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import connections
from .models import User, UserProfile
from .serializers import UserProfileSerializer, UserDetailSerializer, UserSerializer


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


class UserByIdView(generics.RetrieveAPIView):
    """
    Retrieve user by ID (for viewing other users' profiles)
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        return get_object_or_404(User, id=user_id)


@api_view(['GET'])
@permission_classes([])  # Allow unauthenticated access
def health_check(request):
    """
    Health check endpoint for monitoring deployment status
    Returns 200 OK if the service is healthy
    """
    try:
        # Check database connection
        db_conn = connections['default']
        db_conn.cursor()

        return Response({
            'status': 'healthy',
            'database': 'connected',
            'service': 'drag-n-scroll-api'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'database': 'disconnected',
            'service': 'drag-n-scroll-api',
            'error': str(e)
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
