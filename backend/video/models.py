"""
Video sharing model
Users can post videos in their profile, and everyone can see them in Videos section
"""
from django.db import models
from core.models import User


class Video(models.Model):
    """User-posted video"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posted_videos'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # Video source: either URL (YouTube, Vimeo) or uploaded file
    video_url = models.URLField(max_length=500, blank=True, default='', help_text="YouTube, Vimeo, etc.")
    video_file = models.FileField(upload_to='videos/', blank=True, null=True, help_text="Uploaded video file")

    thumbnail_url = models.URLField(max_length=500, blank=True, default='')
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)

    # Video type - nullable for backward compatibility
    video_type = models.CharField(
        max_length=20,
        choices=[('url', 'URL Link'), ('file', 'Uploaded File')],
        blank=True,
        null=True,
        default='url'
    )

    hsk_level = models.IntegerField(default=1, help_text="HSK level (1-6)")
    tags = models.JSONField(default=list, blank=True, help_text="List of tags")

    # Engagement
    views_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

    def __str__(self):
        return f"{self.user.username}: {self.title}"


class VideoLike(models.Model):
    """Like on a video"""
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='liked_videos'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('video', 'user')
        verbose_name = 'Лайк видео'
        verbose_name_plural = 'Лайки видео'


class VideoComment(models.Model):
    """Comment on a video"""
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='video_comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Комментарий видео'
        verbose_name_plural = 'Комментарии видео'

    def __str__(self):
        return f"{self.user.username} on {self.video.title}"
