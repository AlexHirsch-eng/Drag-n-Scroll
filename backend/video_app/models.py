from django.db import models
from django.conf import settings

class VideoCategory(models.Model):
    """Categories for videos (Vocabulary, Grammar, Culture, etc.)"""
    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=10)  # Emoji or icon
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.icon} {self.name}"


class Video(models.Model):
    """User-generated learning videos (TikTok-style)"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('processing', 'Processing'),
        ('ready', 'Ready'),
        ('failed', 'Failed'),
    ]

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='videos'
    )

    # Video file and metadata
    video_file = models.FileField(upload_to='videos/%Y/%m/')
    thumbnail = models.ImageField(upload_to='video_thumbnails/%Y/%m/', blank=True)
    duration = models.IntegerField(help_text='Duration in seconds')

    # Content
    description = models.TextField()
    category = models.ForeignKey(
        VideoCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='videos'
    )
    tags = models.JSONField(default=list, help_text='List of hashtags')
    music_title = models.CharField(max_length=200, blank=True)

    # Lesson connection (optional)
    lesson_number = models.IntegerField(null=True, blank=True)
    lesson_title = models.CharField(max_length=200, blank=True)
    lesson_words = models.JSONField(default=list, help_text='Words taught in this video')

    # Statistics
    views_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)

    # Moderation
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    is_reported = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['category']),
            models.Index(fields=['status']),
            models.Index(fields=['-likes_count']),
        ]

    def __str__(self):
        return f"Video {self.id} by {self.creator.username}"


class VideoView(models.Model):
    """Track video views"""
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='video_views'
    )
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['video', 'user']


class VideoLike(models.Model):
    """Track video likes"""
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_likes')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='video_likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['video', 'user']


class VideoBookmark(models.Model):
    """Track saved/bookmarked videos"""
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='bookmarks')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='video_bookmarks'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['video', 'user']
        verbose_name = 'Video Bookmark'


class VideoComment(models.Model):
    """Comments on videos"""
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='video_comments'
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    text = models.TextField()
    likes_count = models.IntegerField(default=0)

    # Translations (auto-generated from Chinese)
    translation_ru = models.TextField(blank=True, null=True, help_text='Translation to Russian')
    translation_en = models.TextField(blank=True, null=True, help_text='Translation to English')
    translated_at = models.DateTimeField(auto_now_add=False, null=True, blank=True,
                                        help_text='When the translation was last updated')

    # Moderation
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['video', '-created_at']),
        ]

    def __str__(self):
        return f"Comment by {self.user.username} on Video {self.video.id}"


class VideoCommentLike(models.Model):
    """Likes on comments"""
    comment = models.ForeignKey(VideoComment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comment_likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['comment', 'user']


class VideoShare(models.Model):
    """Track video shares"""
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='shares')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='video_shares'
    )
    platform = models.CharField(max_length=50, blank=True)  # instagram, twitter, etc.
    shared_at = models.DateTimeField(auto_now_add=True)


class VideoReport(models.Model):
    """User reports for inappropriate content"""
    REPORT_REASONS = [
        ('spam', 'Spam'),
        ('inappropriate', 'Inappropriate Content'),
        ('misinformation', 'Misinformation'),
        ('harassment', 'Harassment'),
        ('other', 'Other'),
    ]

    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='video_reports'
    )

    reason = models.CharField(max_length=50, choices=REPORT_REASONS)
    description = models.TextField(blank=True)

    is_reviewed = models.BooleanField(default=False)
    action_taken = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)


class VideoHashtag(models.Model):
    """Popular hashtags for categorization"""
    tag = models.CharField(max_length=100, unique=True)
    uses_count = models.IntegerField(default=0)

    def __str__(self):
        return self.tag


class UserFollowing(models.Model):
    """User following system (for social features)"""
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['follower', 'following']
        verbose_name = 'User Following'

    def __str__(self):
        return f"{self.follower.username} → {self.following.username}"

