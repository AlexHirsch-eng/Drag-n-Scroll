"""
URL configuration for Video sharing API
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VideoViewSet, videos_list, user_feed, upload_video,
    video_feed, categories_list
)

router = DefaultRouter()
router.register(r'videos', VideoViewSet, basename='video')

# Custom paths must come BEFORE router to avoid conflicts
urlpatterns = [
    # Video feed endpoint (frontend calls /videos/feed/)
    path('videos/feed/', video_feed, name='video-feed'),
    # Video list endpoint
    path('videos/list/', videos_list, name='videos-list'),
    # Upload video endpoint
    path('videos/upload/', upload_video, name='upload-video'),
    # User feed endpoint
    path('users/<int:user_id>/feed/', user_feed, name='user-feed'),
    # Categories list endpoint
    path('categories-list/', categories_list, name='categories-list'),
    # ViewSet routes (must be last)
    path('', include(router.urls)),
]
