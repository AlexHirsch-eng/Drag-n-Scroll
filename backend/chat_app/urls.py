"""
URL configuration for Chat App
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'rooms', views.ChatRoomViewSet, basename='chatroom')
router.register(r'messages', views.ChatMessageViewSet, basename='chatmessage')

urlpatterns = [
    path('', include(router.urls)),
    path('users/suggested/', views.suggested_users, name='suggested-users'),
    path('rooms/<int:room_id>/read/', views.mark_messages_read, name='mark-read'),
    path('messages/<int:message_id>/translate/', views.translate_message, name='translate-message'),
    path('stories/', views.stories_list, name='stories-list'),
    path('stories/<int:story_id>/', views.story_detail, name='story-detail'),
    path('users/<int:user_id>/stories/', views.user_stories, name='user-stories'),
    path('stories/<int:story_id>/react/', views.react_to_story, name='react-story'),
    path('users/blocked/', views.blocked_users, name='blocked-users'),
    path('users/blocked/<int:user_id>/', views.unblock_user, name='unblock-user'),
    path('typing/', views.send_typing_indicator, name='send-typing'),
    path('rooms/<int:room_id>/typing/', views.typing_users, name='typing-users'),
]
