from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    # Chat Rooms
    path('rooms/', views.get_chat_rooms, name='get_chat_rooms'),
    path('rooms/<int:room_id>/', views.get_chat_room_detail, name='get_chat_room_detail'),
    path('rooms/create_direct/', views.create_direct_chat, name='create_direct_chat'),
    path('rooms/create_group/', views.create_group_chat, name='create_group_chat'),
    path('rooms/<int:room_id>/read/', views.mark_messages_read, name='mark_messages_read'),

    # Messages
    path('messages/', views.get_messages, name='get_messages'),
    path('messages/create/', views.send_message, name='send_message'),
    path('messages/<int:message_id>/translate/', views.translate_message, name='translate_message'),

    # Users
    path('users/suggested/', views.get_suggested_users, name='get_suggested_users'),

    # Typing Indicators
    path('typing/', views.typing_indicator, name='typing_indicator'),

    # AI Chat
    path('ai/', views.ai_chat, name='ai_chat'),
]
