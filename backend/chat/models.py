from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatRoom(models.Model):
    ROOM_TYPES = (
        ('direct', 'Direct Message'),
        ('group', 'Group Chat'),
    )

    name = models.CharField(max_length=255, blank=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES, default='direct')
    participants = models.ManyToManyField(User, through='ChatParticipant', related_name='chat_rooms')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.name or f"{self.room_type} chat {self.id}"

    @property
    def other_user(self):
        """For direct chats, return the other participant"""
        if self.room_type == 'direct':
            participant = self.participants.exclude(id=self.created_by.id).first()
            return participant
        return None


class ChatParticipant(models.Model):
    ROLES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
    )

    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='participant_info')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_participations')
    role = models.CharField(max_length=10, choices=ROLES, default='member')
    nickname = models.CharField(max_length=100, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    last_read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['room', 'user']

    def __str__(self):
        return f"{self.user.username} in {self.room.name}"


class ChatMessage(models.Model):
    MESSAGE_TYPES = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('file', 'File'),
    )

    STATUS_CHOICES = (
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
    )

    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='text')
    text = models.TextField(blank=True)
    attachment = models.JSONField(null=True, blank=True)
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='sent')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Translation fields
    translation_ru = models.TextField(blank=True, null=True)
    translation_en = models.TextField(blank=True, null=True)
    translation_zh = models.TextField(blank=True, null=True)
    translation_kz = models.TextField(blank=True, null=True)
    translation_de = models.TextField(blank=True, null=True)
    translation_fr = models.TextField(blank=True, null=True)
    translation_es = models.TextField(blank=True, null=True)
    translation_ja = models.TextField(blank=True, null=True)
    translation_ko = models.TextField(blank=True, null=True)
    translated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username}: {self.text[:50]}"
