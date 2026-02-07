from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ChatRoom, ChatParticipant, ChatMessage

User = get_user_model()


class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ChatParticipantSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer(read_only=True)

    class Meta:
        model = ChatParticipant
        fields = ['user', 'role', 'nickname', 'joined_at', 'last_read_at']


class ChatRoomSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()
    participants_count = serializers.SerializerMethodField()
    last_message_preview = serializers.SerializerMethodField()
    last_message_at = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'room_type', 'other_user', 'participants_count',
                  'last_message_preview', 'last_message_at', 'unread_count', 'created_at', 'updated_at']

    def get_other_user(self, obj):
        # Get the context to check current user
        request = self.context.get('request')
        if not request:
            return None

        current_user = request.user
        if obj.room_type == 'direct':
            # Return the OTHER user (not the current one)
            participant = obj.participants.exclude(id=current_user.id).first()
            if participant:
                profile = None
                avatar_url = None
                bio = None

                # Safely get profile and its fields
                try:
                    if hasattr(participant, 'profile'):
                        profile = participant.profile
                        # Only get avatar URL if file exists (has a name)
                        if profile and hasattr(profile, 'avatar') and profile.avatar and hasattr(profile.avatar, 'name') and profile.avatar.name:
                            try:
                                avatar_url = profile.avatar.url
                            except:
                                avatar_url = None
                        # Get bio safely
                        if profile and hasattr(profile, 'bio'):
                            bio = profile.bio
                except:
                    pass

                return {
                    'id': participant.id,
                    'username': participant.username,
                    'email': participant.email,
                    'avatar': avatar_url,
                    'bio': bio,
                    'online': getattr(participant, 'is_online', False)
                }
        return None

    def get_participants_count(self, obj):
        return obj.participants.count()

    def get_last_message_preview(self, obj):
        last_msg = obj.messages.first()
        if last_msg:
            return last_msg.text[:50] if last_msg.text else ''
        return ''

    def get_last_message_at(self, obj):
        last_msg = obj.messages.first()
        if last_msg:
            return last_msg.created_at
        return None

    def get_unread_count(self, obj):
        # Simplified - should be calculated based on read receipts
        return 0


class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserBasicSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'room', 'sender', 'sender_id', 'message_type', 'text', 'status',
                  'created_at', 'updated_at', 'translation_ru', 'translation_en', 'translation_zh',
                  'translation_kz', 'translation_de', 'translation_fr', 'translation_es',
                  'translation_ja', 'translation_ko', 'translated_at']

    def to_representation(self, instance):
        # Ensure sender is always included, even if None
        data = super().to_representation(instance)
        if data.get('sender') is None and instance.sender_id:
            # Fallback to sender_id if sender object is not available
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                sender = User.objects.get(id=instance.sender_id)
                data['sender'] = UserBasicSerializer(sender).data
            except User.DoesNotExist:
                data['sender'] = {'id': instance.sender_id, 'username': 'Unknown', 'email': ''}
        return data


class ChatRoomDetailSerializer(serializers.ModelSerializer):
    participants = ChatParticipantSerializer(many=True, read_only=True)
    last_message = ChatMessageSerializer(read_only=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'room_type', 'participants', 'participants_count',
                  'last_message', 'unread_count', 'created_at', 'updated_at']


class CreateDirectChatSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


class CreateGroupChatSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)


class SendMessageSerializer(serializers.Serializer):
    room = serializers.IntegerField()
    text = serializers.CharField()
    message_type = serializers.CharField(default='text', required=False)


class SuggestedUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    bio = serializers.CharField(allow_blank=True, required=False)
    avatar = serializers.CharField(allow_blank=True, required=False)
    online = serializers.BooleanField(default=False)
