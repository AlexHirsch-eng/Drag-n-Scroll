from django.contrib import admin
from .models import (
    ChatRoom, ChatParticipant, ChatMessage, MessageReadStatus,
    Story, StoryView, StoryReaction, UserBlock, TypingIndicator
)

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'room_type', 'created_by', 'participants_count', 'created_at']
    list_filter = ['room_type', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']

    def participants_count(self, obj):
        return obj.participants.count()
    participants_count.short_description = 'Participants'

@admin.register(ChatParticipant)
class ChatParticipantAdmin(admin.ModelAdmin):
    list_display = ['room', 'user', 'role', 'joined_at']
    list_filter = ['role', 'joined_at']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'sender', 'message_type', 'text_preview', 'status', 'created_at']
    list_filter = ['message_type', 'status', 'created_at']
    search_fields = ['text', 'sender__username']
    readonly_fields = ['created_at', 'updated_at']

    def text_preview(self, obj):
        return obj.text[:100] if obj.text else f"{obj.message_type}"
    text_preview.short_description = 'Content'

@admin.register(MessageReadStatus)
class MessageReadStatusAdmin(admin.ModelAdmin):
    list_display = ['message', 'user', 'read_at']

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'media_type', 'views_count', 'created_at', 'expires_at']
    list_filter = ['media_type', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['views_count', 'created_at']

@admin.register(StoryView)
class StoryViewAdmin(admin.ModelAdmin):
    list_display = ['story', 'user', 'viewed_at']
    list_filter = ['viewed_at']

@admin.register(StoryReaction)
class StoryReactionAdmin(admin.ModelAdmin):
    list_display = ['story', 'user', 'emoji', 'created_at']
    list_filter = ['created_at']

@admin.register(UserBlock)
class UserBlockAdmin(admin.ModelAdmin):
    list_display = ['blocker', 'blocked', 'created_at']
    list_filter = ['created_at']
    search_fields = ['blocker__username', 'blocked__username']

@admin.register(TypingIndicator)
class TypingIndicatorAdmin(admin.ModelAdmin):
    list_display = ['room', 'user', 'created_at']
    readonly_fields = ['created_at']
