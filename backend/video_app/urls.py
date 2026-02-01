"""
URL configuration for Video App
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'videos', views.VideoViewSet, basename='video')
router.register(r'categories', views.VideoCategoryViewSet, basename='videocategory')

urlpatterns = [
    path('', include(router.urls)),
    path('videos/<int:video_id>/comments/', views.video_comments_detail, name='video-comments'),
    path('comments/<int:comment_id>/like/', views.like_comment, name='like-comment'),
    path('comments/<int:comment_id>/translate/', views.translate_comment, name='translate-comment'),
    path('users/<int:user_id>/feed/', views.user_feed, name='user-feed'),
    path('users/<int:user_id>/follow/', views.follow_user, name='follow-user'),
    path('videos/<int:video_id>/report/', views.report_video, name='report-video'),
    path('admin/import-videos/', views.import_videos_from_folder, name='admin-import-videos'),
    path('categories-list/', views.categories_list, name='categories-list'),
]
