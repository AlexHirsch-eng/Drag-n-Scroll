"""
Views for core app
"""
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import connections
from django.core.management import call_command
from django.conf import settings
import re
import logging
from .models import User, UserProfile, UserCourseProgress
from .serializers import UserProfileSerializer, UserDetailSerializer, UserSerializer

logger = logging.getLogger(__name__)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update user profile
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Get user profile, create if missing
        """
        profile = getattr(self.request.user, 'profile', None)
        if not profile:
            # Profile missing - create it
            profile = UserProfile.objects.create(
                user=self.request.user,
                learning_language='RU'
            )
        return profile


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
@permission_classes([permissions.IsAuthenticated])
def debug_auth(request):
    """
    Debug endpoint to check auth state
    """
    user = request.user
    try:
        profile = UserProfile.objects.get(user=user)
        profile_data = {
            'exists': True,
            'learning_language': profile.learning_language,
            'current_hsk_level': profile.current_hsk_level,
        }
    except UserProfile.DoesNotExist:
        profile_data = {'exists': False}

    try:
        progress = UserCourseProgress.objects.get(user=user)
        progress_data = {
            'exists': True,
            'current_day': progress.current_day,
            'total_xp': progress.total_xp,
        }
    except UserCourseProgress.DoesNotExist:
        progress_data = {'exists': False}

    return Response({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active,
        },
        'profile': profile_data,
        'progress': progress_data,
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def debug_courses(request):
    """
    Debug endpoint to check course data availability
    """
    from course.models import Course, CourseDay

    # Get all courses
    courses = Course.objects.filter(is_active=True)
    courses_data = []

    for course in courses:
        days = course.days.all().order_by('day_number')
        courses_data.append({
            'id': course.id,
            'hsk_level': course.hsk_level,
            'title': course.title,
            'total_days': course.total_days,
            'available_days': days.count(),
            'days': [{'id': day.id, 'day_number': day.day_number, 'title': day.title} for day in days]
        })

    return Response({
        'total_courses': courses.count(),
        'courses': courses_data,
    })


@api_view(['GET'])
@permission_classes([])
def debug_database(request):
    """
    Debug endpoint to check database configuration and persistence
    """
    from django.conf import settings
    import os
    from django.db import connections

    db_info = {
        'default_engine': settings.DATABASES['default']['ENGINE'],
        'database_name': str(settings.DATABASES['default'].get('NAME')),
        'is_persistent': False,
        'platform': os.environ.get('RENDER', os.environ.get('VERCEL', 'local')),
    }

    # Check if using PostgreSQL (persistent)
    if 'postgresql' in db_info['default_engine'].lower():
        db_info['is_persistent'] = True
        db_info['database_type'] = 'PostgreSQL'
        db_info['persistence'] = 'GOOD - Data persists across restarts'
    elif 'sqlite' in db_info['default_engine'].lower():
        db_info['is_persistent'] = False
        db_info['database_type'] = 'SQLite'
        db_info['persistence'] = 'CRITICAL - Data LOST on container restart!'

    # Test database connection
    try:
        db_conn = connections['default']
        with db_conn.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_info['connection_status'] = 'connected'
    except Exception as e:
        db_info['connection_status'] = f'error: {str(e)}'

    # Check for DATABASE_URL
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        db_info['has_database_url'] = True
        # Mask password
        import re
        db_info['database_url'] = re.sub(r'(://[^:]+:)[^@]+(@)', r'\1****\2', db_url)
    else:
        db_info['has_database_url'] = False
        db_info['database_url'] = None

    return Response(db_info)


def mask_database_url(url):
    """Mask password in database URL for safe display"""
    if not url:
        return None
    # Replace password in postgres://user:password@host with postgres://user:****@host
    return re.sub(r'(://[^:]+:)[^@]+(@)', r'\1****\2', url)


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

        # Get database info for diagnostics
        db_url = getattr(settings, 'DATABASE_URL', 'not set')
        masked_url = mask_database_url(db_url)

        return Response({
            'status': 'healthy',
            'database': 'connected',
            'service': 'drag-n-scroll-api',
            'database_url': masked_url
        }, status=status.HTTP_200_OK)
    except Exception as e:
        db_url = getattr(settings, 'DATABASE_URL', 'not set')
        masked_url = mask_database_url(db_url)

        return Response({
            'status': 'unhealthy',
            'database': 'disconnected',
            'service': 'drag-n-scroll-api',
            'database_url': masked_url,
            'error': str(e)
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['POST'])
@permission_classes([])  # Allow unauthenticated for initial setup
def run_migrations(request):
    """
    Run database migrations manually
    Call this endpoint to apply migrations when you can't access shell
    """
    try:
        call_command('migrate', '--run-syncdb', verbosity=2)
        return Response({
            'status': 'success',
            'message': 'Migrations completed successfully'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
