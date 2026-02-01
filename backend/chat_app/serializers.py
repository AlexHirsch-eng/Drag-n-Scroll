from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import UserProfile
from .models import (
    ChatRoom, ChatParticipant, ChatMessage, MessageReadStatus,
    Story, StoryView, StoryReaction, UserBlock, TypingIndicator
)

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'learning_language', 'current_hsk_level']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']


class ChatParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_online = serializers.SerializerMethodField()

    class Meta:
        model = ChatParticipant
        fields = ['id', 'user', 'role', 'last_read_at', 'nickname', 'joined_at', 'is_online']

    def get_is_online(self, obj):
        # TODO: Implement proper online status tracking
        return False


class ChatRoomListSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()
    participants_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = [
            'id', 'name', 'room_type', 'other_user', 'participants_count',
            'last_message', 'last_message_at', 'unread_count'
        ]

    def get_other_user(self, obj):
        request = self.context.get('request')
        if obj.room_type == 'direct' and request and request.user.is_authenticated:
            # Find the other participant (not the current user)
            participant = ChatParticipant.objects.filter(
                room=obj,
                user=request.user
            ).first()

            if participant:
                other_participant = ChatParticipant.objects.filter(
                    room=obj,
                user__isnull=False
                ).exclude(user=request.user).first()

                if other_participant:
                    return UserSerializer(other_participant.user).data
        return None

    def get_participants_count(self, obj):
        return obj.participants.count()

    def get_last_message(self, obj):
        # Get the most recent message
        message = obj.messages.filter(
            message_type='text'
        ).order_by('-created_at').first()

        if message:
            return {
                'text': message.text[:100],
                'sender_id': message.sender_id,
                'created_at': message.created_at
            }
        return None

    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            participant = ChatParticipant.objects.filter(
                room=obj,
                user=request.user
            ).first()

            if participant:
                # Count messages created after last_read_at
                return obj.messages.filter(
                    created_at__gt=participant.last_read_at,
                    sender__isnull=False
                ).exclude(sender=request.user).count()
        return 0


class ChatRoomDetailSerializer(serializers.ModelSerializer):
    participants = ChatParticipantSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'room_type', 'avatar', 'participants', 'last_message', 'created_at', 'updated_at']

    def get_last_message(self, obj):
        message = obj.messages.order_by('-created_at').first()
        if message:
            return {
                'id': message.id,
                'text': message.text[:200] if message.text else f"[{message.message_type}]",
                'sender_id': message.sender_id,
                'message_type': message.message_type,
                'status': message.status,
                'created_at': message.created_at
            }
        return None


class ChatRoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['name', 'room_type']

    def validate(self, data):
        if data.get('room_type') == 'group' and not data.get('name'):
            raise serializers.ValidationError({"name": "Group chats must have a name."})
        return data

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        room = super().create(validated_data)

        # Add creator as participant
        if room.room_type == 'group':
            ChatParticipant.objects.create(
                room=room,
                user=self.context['request'].user,
                role='admin'
            )

        return room


class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    reply_to = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = [
            'id', 'room', 'sender', 'message_type', 'text', 'attachment',
            'reply_to', 'status', 'created_at', 'updated_at',
            'translation_ru', 'translation_en', 'translation_zh', 'translated_at'
        ]
        read_only_fields = ['sender', 'created_at', 'updated_at']

    def get_reply_to(self, obj):
        if obj.reply_to:
            return {
                'id': obj.reply_to.id,
                'text': obj.reply_to.text[:100] if obj.reply_to.text else f"[{obj.reply_to.message_type}]",
                'sender': obj.reply_to.sender.username
            }
        return None


class ChatMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['room', 'text', 'message_type', 'attachment', 'reply_to']

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)


class MessageReadStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageReadStatus
        fields = ['message', 'user', 'read_at']
        read_only_fields = ['read_at']


class StorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_viewed = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = [
            'id', 'user', 'media_file', 'media_type', 'thumbnail',
            'duration', 'views_count', 'is_viewed', 'created_at', 'expires_at'
        ]

    def get_is_viewed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return StoryView.objects.filter(
                story=obj,
                user=request.user
            ).exists()
        return False


class StoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['media_file', 'media_type', 'thumbnail', 'duration']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user

        # Set expiry time (24 hours from now)
        from django.utils import timezone
        from datetime import timedelta
        validated_data['expires_at'] = timezone.now() + timedelta(hours=24)

        return super().create(validated_data)


class StoryViewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StoryView
        fields = ['story', 'user', 'viewed_at']
        read_only_fields = ['viewed_at']


class StoryReactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StoryReaction
        fields = ['story', 'user', 'emoji', 'created_at']
        read_only_fields = ['created_at']


class UserBlockSerializer(serializers.ModelSerializer):
    blocker = UserSerializer(read_only=True)
    blocked = UserSerializer(read_only=True)

    class Meta:
        model = UserBlock
        fields = ['blocker', 'blocked', 'created_at']


class TypingIndicatorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TypingIndicator
        fields = ['room', 'user', 'created_at']
        read_only_fields = ['created_at']


class SuggestedUserSerializer(serializers.Serializer):
    """Serializer for suggested users in new chat modal"""
    id = serializers.IntegerField()
    username = serializers.CharField()
    bio = serializers.CharField()
    avatar = serializers.ImageField()
    online = serializers.BooleanField()


class ChatRoomWithLastMessageSerializer(serializers.ModelSerializer):
    """Enhanced serializer for chat list with last message details"""
    other_user = serializers.SerializerMethodField()
    participants_count = serializers.SerializerMethodField()
    last_message_preview = serializers.SerializerMethodField()
    last_message_sender = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = [
            'id', 'name', 'room_type', 'other_user', 'avatar',
            'participants_count', 'last_message_preview', 'last_message_sender',
            'last_message_at', 'unread_count'
        ]

    def get_other_user(self, obj):
        request = self.context.get('request')
        if obj.room_type == 'direct' and request and request.user.is_authenticated:
            # Get the other participant
            other_participant = ChatParticipant.objects.filter(
                room=obj,
                user__isnull=False
            ).exclude(user=request.user).first()

            if other_participant:
                user = other_participant.user
                avatar = None
                if hasattr(user, 'profile') and user.profile and user.profile.avatar:
                    avatar = user.profile.avatar.url

                return {
                    'id': user.id,
                    'username': user.username,
                    'avatar': avatar,
                    'online': False  # TODO: Implement online status
                }
        return None

    def get_last_message_preview(self, obj):
        message = obj.messages.order_by('-created_at').first()
        if message and message.message_type == 'text':
            return message.text
        return None

    def get_last_message_sender(self, obj):
        request = self.context.get('request')
        message = obj.messages.order_by('-created_at').first()
        if message:
            return 'me' if request and request.user.is_authenticated and message.sender_id == request.user.id else 'them'
        return None

    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            participant = ChatParticipant.objects.filter(
                room=obj,
                user=request.user
            ).first()

            if participant:
                return obj.messages.filter(
                    created_at__gt=participant.last_read_at
                ).exclude(sender=request.user).count()
        return 0

    def get_participants_count(self, obj):
        if obj.room_type == 'group':
            return obj.participants.count()
        return 2  # Direct messages have 2 participants
