"""
URL configuration for Video sharing API
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VideoViewSet, videos_list, user_feed, upload_video

router = DefaultRouter()
router.register(r'videos', VideoViewSet, basename='video')

# Custom paths must come BEFORE router to avoid conflicts
urlpatterns = [
    path('videos/list/', videos_list, name='videos-list'),
    path('videos/upload/', upload_video, name='upload-video'),
    path('users/<int:user_id>/feed/', user_feed, name='user-feed'),
    path('', include(router.urls)),
]
