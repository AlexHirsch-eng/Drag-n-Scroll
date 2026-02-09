"""
Admin configuration for Video sharing
"""
from django.contrib import admin
from .models import Video, VideoLike, VideoComment


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """Admin for Video model"""
    list_display = ['id', 'user', 'title', 'hsk_level', 'views_count', 'likes_count', 'comments_count', 'created_at']
    list_filter = ['hsk_level', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['views_count', 'likes_count', 'comments_count', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(VideoLike)
class VideoLikeAdmin(admin.ModelAdmin):
    """Admin for VideoLike model"""
    list_display = ['id', 'video', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['video__title', 'user__username']
    readonly_fields = ['created_at']


@admin.register(VideoComment)
class VideoCommentAdmin(admin.ModelAdmin):
    """Admin for VideoComment model"""
    list_display = ['id', 'video', 'user', 'content_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['video__title', 'user__username', 'content']
    readonly_fields = ['created_at', 'updated_at']

    def content_preview(self, obj):
        """Show preview of comment content"""
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content'
