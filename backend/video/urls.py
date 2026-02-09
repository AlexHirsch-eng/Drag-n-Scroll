"""
URL configuration for Video sharing API
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VideoViewSet, videos_list, user_feed

router = DefaultRouter()
router.register(r'videos', VideoViewSet, basename='video')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/videos/list/', videos_list, name='videos-list'),
    path('api/video/users/<int:user_id>/feed/', user_feed, name='user-feed'),
]
