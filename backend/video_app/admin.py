from django.contrib import admin
from .models import (
    Video, VideoCategory, VideoView, VideoLike, VideoBookmark,
    VideoComment, VideoCommentLike, VideoShare, VideoReport,
    VideoHashtag, UserFollowing
)

@admin.register(VideoCategory)
class VideoCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'order']
    list_editable = ['order']
    ordering = ['order']

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'creator', 'description', 'category', 'status', 'views_count', 'likes_count', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['description', 'tags', 'creator__username']
    readonly_fields = ['views_count', 'likes_count', 'comments_count', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'

@admin.register(VideoView)
class VideoViewAdmin(admin.ModelAdmin):
    list_display = ['video', 'user', 'viewed_at']
    list_filter = ['viewed_at']

@admin.register(VideoLike)
class VideoLikeAdmin(admin.ModelAdmin):
    list_display = ['video', 'user', 'created_at']
    list_filter = ['created_at']

@admin.register(VideoBookmark)
class VideoBookmarkAdmin(admin.ModelAdmin):
    list_display = ['video', 'user', 'created_at']
    list_filter = ['created_at']

@admin.register(VideoComment)
class VideoCommentAdmin(admin.ModelAdmin):
    list_display = ['video', 'user', 'text_preview', 'parent', 'likes_count', 'created_at']
    list_filter = ['created_at', 'is_deleted']
    search_fields = ['text', 'user__username']
    readonly_fields = ['likes_count', 'created_at', 'updated_at']

    def text_preview(self, obj):
        return obj.text[:100]
    text_preview.short_description = 'Text'

@admin.register(VideoCommentLike)
class VideoCommentLikeAdmin(admin.ModelAdmin):
    list_display = ['comment', 'user', 'created_at']

@admin.register(VideoShare)
class VideoShareAdmin(admin.ModelAdmin):
    list_display = ['video', 'user', 'platform', 'shared_at']
    list_filter = ['platform', 'shared_at']

@admin.register(VideoReport)
class VideoReportAdmin(admin.ModelAdmin):
    list_display = ['video', 'reporter', 'reason', 'is_reviewed', 'created_at']
    list_filter = ['reason', 'is_reviewed', 'created_at']
    actions = ['mark_as_reviewed']

    def mark_as_reviewed(self, request, queryset):
        queryset.update(is_reviewed=True)
    mark_as_reviewed.short_description = "Mark selected reports as reviewed"

@admin.register(VideoHashtag)
class VideoHashtagAdmin(admin.ModelAdmin):
    list_display = ['tag', 'uses_count']
    ordering = ['-uses_count']

@admin.register(UserFollowing)
class UserFollowingAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    list_filter = ['created_at']
    search_fields = ['follower__username', 'following__username']
