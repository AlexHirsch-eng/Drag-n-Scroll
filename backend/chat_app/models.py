from django.db import models
from django.conf import settings

class ChatRoom(models.Model):
    """Chat room for direct messages or group chats"""
    ROOM_TYPE_CHOICES = [
        ('direct', 'Direct Message'),
        ('group', 'Group Chat'),
    ]

    name = models.CharField(max_length=200, blank=True)  # Only for group chats
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, default='direct')
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ChatParticipant',
        related_name='chat_rooms'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_chats'
    )

    # Optional: avatar for group chats
    avatar = models.ImageField(upload_to='chat_avatars/%Y/%m/', blank=True)

    # Track last message activity
    last_message_at = models.DateTimeField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        if self.room_type == 'group':
            return f"Group: {self.name}"
        return f"DM: {self.id}"


class ChatParticipant(models.Model):
    """Through model for chat participants"""
    ROOM_ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('member', 'Member'),
    ]

    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROOM_ROLE_CHOICES, default='member')

    # Last read message tracking
    last_read_at = models.DateTimeField(auto_now_add=True)

    # Nickname for group chats (optional)
    nickname = models.CharField(max_length=100, blank=True)

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['room', 'user']
        indexes = [
            models.Index(fields=['room', 'user']),
        ]

    def __str__(self):
        return f"{self.user.username} in {self.room.id}"


class ChatMessage(models.Model):
    """Messages in chat rooms"""
    MESSAGE_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('file', 'File'),
        ('system', 'System'),
    ]

    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
    ]

    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    # Message content
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default='text')
    text = models.TextField(blank=True)
    attachment = models.JSONField(null=True, blank=True)

    # Translations (auto-generated)
    translation_ru = models.TextField(blank=True, null=True, help_text='Translation to Russian')
    translation_en = models.TextField(blank=True, null=True, help_text='Translation to English')
    translation_zh = models.TextField(blank=True, null=True, help_text='Translation to Chinese')
    translated_at = models.DateTimeField(auto_now_add=False, null=True, blank=True,
                                        help_text='When the translation was last updated')

    # Reply to another message
    reply_to = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='replies'
    )

    # Read receipts
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['room', '-created_at']),
            models.Index(fields=['sender', '-created_at']),
        ]

    def __str__(self):
        preview = self.text[:50] if self.text else f"{self.message_type} message"
        return f"{self.sender.username}: {preview}"


class MessageReadStatus(models.Model):
    """Track read status for each message recipient"""
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, related_name='read_statuses')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['message', 'user']


class Story(models.Model):
    """User stories (like Instagram)"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='stories'
    )

    # Story content
    media_file = models.FileField(upload_to='stories/%Y/%m/')
    media_type = models.CharField(max_length=20)  # image, video
    thumbnail = models.ImageField(upload_to='story_thumbnails/%Y/%m/', blank=True)

    # Optional: duration for video stories
    duration = models.IntegerField(null=True, blank=True)

    # View tracking
    views_count = models.IntegerField(default=0)
    viewed_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='StoryView',
        related_name='viewed_stories'
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()  # Stories expire after 24 hours

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"Story by {self.user.username}"


class StoryView(models.Model):
    """Track who viewed which stories"""
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='story_views')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='viewed_stories_list'
    )
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['story', 'user']


class StoryReaction(models.Model):
    """Reactions to stories"""
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='story_reactions'
    )

    emoji = models.CharField(max_length=50)  # ❤️, 🔥, etc.

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['story', 'user', 'emoji']


class UserBlock(models.Model):
    """Block users from contacting"""
    blocker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blocking'
    )
    blocked = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blocked_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['blocker', 'blocked']

    def __str__(self):
        return f"{self.blocker.username} blocked {self.blocked.username}"


class TypingIndicator(models.Model):
    """Track who is typing in which chat (temporary data)"""
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='typing_indicators')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Timestamp for auto-cleanup (indicators expire after 10 seconds)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['room', '-created_at']),
        ]
