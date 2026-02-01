"""
API Views for Chat App (Instagram-style messaging and stories)
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q, Count, F, Subquery, OuterRef
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import (
    ChatRoom, ChatParticipant, ChatMessage, MessageReadStatus,
    Story, StoryView, StoryReaction, UserBlock, TypingIndicator
)
from .serializers import (
    ChatRoomListSerializer, ChatRoomDetailSerializer, ChatRoomCreateSerializer,
    ChatMessageSerializer, ChatMessageCreateSerializer, MessageReadStatusSerializer,
    StorySerializer, StoryCreateSerializer, StoryViewSerializer, StoryReactionSerializer,
    UserBlockSerializer, TypingIndicatorSerializer, SuggestedUserSerializer,
    ChatRoomWithLastMessageSerializer
)

User = get_user_model()


class ChatRoomViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing chat rooms
    Provides list, create, retrieve operations for direct messages and group chats
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['room_type']

    def get_queryset(self):
        # Only return rooms where user is a participant
        return ChatRoom.objects.filter(
            chatparticipant__user=self.request.user
        ).distinct().prefetch_related('participants', 'messages')

    def get_serializer_class(self):
        if self.action == 'list':
            return ChatRoomWithLastMessageSerializer
        if self.action == 'create':
            return ChatRoomCreateSerializer
        return ChatRoomDetailSerializer

    def perform_create(self, serializer):
        room = serializer.save(created_by=self.request.user)

        # Add creator as participant for group chats
        if room.room_type == 'group':
            ChatParticipant.objects.create(
                room=room,
                user=self.request.user,
                role='admin'
            )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Mark messages as read
        participant = ChatParticipant.objects.filter(
            room=instance,
            user=request.user
        ).first()

        if participant:
            # Update last_read_at
            participant.last_read_at = timezone.now()
            participant.save()

            # Create read status for unread messages
            unread_messages = ChatMessage.objects.filter(
                room=instance,
                created_at__gt=participant.last_read_at
            ).exclude(sender=request.user)

            for message in unread_messages:
                MessageReadStatus.objects.get_or_create(
                    message=message,
                    user=request.user,
                    defaults={'read_at': timezone.now()}
                )

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def create_direct(self, request):
        """Create or get existing direct message room with another user"""
        other_user_id = request.data.get('user_id')

        if not other_user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            other_user = User.objects.get(id=other_user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if other_user == request.user:
            return Response(
                {'error': 'You cannot create a chat with yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if room already exists
        existing_room = ChatRoom.objects.filter(
            room_type='direct',
            chatparticipant__user=request.user
        ).filter(
            chatparticipant__user=other_user
        ).first()

        if existing_room:
            serializer = ChatRoomDetailSerializer(existing_room)
            return Response(serializer.data)

        # Create new direct message room
        room = ChatRoom.objects.create(
            room_type='direct',
            created_by=request.user
        )

        # Add both participants
        ChatParticipant.objects.create(room=room, user=request.user, role='admin')
        ChatParticipant.objects.create(room=room, user=other_user, role='member')

        serializer = ChatRoomDetailSerializer(room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_participant(self, request, pk=None):
        """Add a participant to a group chat"""
        room = self.get_object()

        if room.room_type != 'group':
            return Response(
                {'error': 'Can only add participants to group chats'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if user is admin
        participant = ChatParticipant.objects.filter(
            room=room,
            user=request.user,
            role='admin'
        ).first()

        if not participant:
            return Response(
                {'error': 'Only admins can add participants'},
                status=status.HTTP_403_FORBIDDEN
            )

        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if already participant
        if ChatParticipant.objects.filter(room=room, user=user).exists():
            return Response(
                {'error': 'User is already a participant'},
                status=status.HTTP_400_BAD_REQUEST
            )

        ChatParticipant.objects.create(
            room=room,
            user=user,
            role='member'
        )

        return Response(
            {'message': f'{user.username} added to the chat'},
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def leave(self, request, pk=None):
        """Leave a group chat"""
        room = self.get_object()

        if room.room_type != 'group':
            return Response(
                {'error': 'Can only leave group chats'},
                status=status.HTTP_400_BAD_REQUEST
            )

        participant = ChatParticipant.objects.filter(
            room=room,
            user=request.user
        ).first()

        if participant:
            participant.delete()
            return Response({'message': 'Left the chat successfully'})

        return Response(
            {'error': 'You are not a participant'},
            status=status.HTTP_400_BAD_REQUEST
        )


class ChatMessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing chat messages
    """
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room_id = self.request.query_params.get('room')
        if room_id:
            # Verify user is participant
            room = ChatRoom.objects.filter(
                id=room_id,
                chatparticipant__user=self.request.user
            ).first()

            if room:
                return ChatMessage.objects.filter(
                    room=room
                ).select_related('sender').order_by('created_at')

        return ChatMessage.objects.none()

    def get_serializer_class(self):
        if self.action == 'create':
            return ChatMessageCreateSerializer
        return ChatMessageSerializer

    def perform_create(self, serializer):
        message = serializer.save(sender=self.request.user)

        # Update room's last_message_at
        ChatRoom.objects.filter(id=message.room.id).update(
            last_message_at=message.created_at
        )

        # Reset participant last_read_at (except sender)
        ChatParticipant.objects.filter(
            room=message.room
        ).exclude(user=self.request.user).update(
            last_read_at=timezone.now() - timezone.timedelta(days=1)
        )

        return message

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def unread(self, request):
        """Get all unread messages across all chats"""
        # Get all rooms where user is participant
        rooms = ChatRoom.objects.filter(chatparticipant__user=request.user)

        unread_messages = []

        for room in rooms:
            participant = ChatParticipant.objects.filter(
                room=room,
                user=request.user
            ).first()

            if participant:
                messages = ChatMessage.objects.filter(
                    room=room,
                    created_at__gt=participant.last_read_at
                ).exclude(sender=request.user).select_related('sender')

                unread_messages.extend(messages)

        serializer = ChatMessageSerializer(unread_messages, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def suggested_users(request):
    """Get suggested users to start a chat with"""
    # Get users that current user already has a direct chat with
    existing_chat_participants = ChatParticipant.objects.filter(
        user=request.user,
        room__room_type='direct'
    ).values_list('room_id', flat=True)

    # Get user IDs from those rooms
    other_participant_ids = ChatParticipant.objects.filter(
        room_id__in=existing_chat_participants
    ).exclude(user=request.user).values_list('user_id', flat=True)

    # Get blocked users
    blocked_users = UserBlock.objects.filter(
        blocker=request.user
    ).values_list('blocked_id', flat=True)

    # Get users that blocked current user
    blocked_by_users = UserBlock.objects.filter(
        blocked=request.user
    ).values_list('blocker_id', flat=True)

    excluded_ids = list(other_participant_ids) + list(blocked_users) + list(blocked_by_users) + [request.user.id]

    suggested = User.objects.exclude(
        id__in=excluded_ids
    ).order_by('username')[:20]

    result = []
    for user in suggested:
        # Get profile data safely
        bio = ''
        avatar = None
        if hasattr(user, 'profile'):
            profile = user.profile
            if hasattr(profile, 'bio'):
                bio = profile.bio or ''
            if hasattr(profile, 'avatar'):
                avatar = profile.avatar if profile.avatar else None

        result.append({
            'id': user.id,
            'username': user.username,
            'bio': bio,
            'avatar': avatar,
            'online': False  # TODO: Implement online status
        })

    serializer = SuggestedUserSerializer(result, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_messages_read(request, room_id):
    """Mark all messages in a room as read"""
    room = get_object_or_404(ChatRoom, id=room_id)

    # Verify user is participant
    participant = ChatParticipant.objects.filter(
        room=room,
        user=request.user
    ).first()

    if not participant:
        return Response(
            {'error': 'You are not a participant in this chat'},
            status=status.HTTP_403_FORBIDDEN
        )

    # Update last_read_at
    participant.last_read_at = timezone.now()
    participant.save()

    # Create read status for all unread messages
    unread_messages = ChatMessage.objects.filter(
        room=room
    ).exclude(sender=request.user).filter(
        created_at__gt=participant.last_read_at
    )

    for message in unread_messages:
        MessageReadStatus.objects.get_or_create(
            message=message,
            user=request.user,
            defaults={'read_at': timezone.now()}
        )

    return Response({'message': 'Messages marked as read'})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def stories_list(request):
    """Get all active stories from followed users or create a new story"""
    if request.method == 'GET':
        # Get stories from followed users and current user
        from video_app.models import UserFollowing

        followed_user_ids = UserFollowing.objects.filter(
            follower=request.user
        ).values_list('following_id', flat=True)

        # Get active stories (not expired)
        now = timezone.now()
        stories = Story.objects.filter(
            Q(user__in=followed_user_ids) | Q(user=request.user),
            expires_at__gt=now
        ).select_related('user').order_by('-created_at')

        serializer = StorySerializer(stories, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StoryCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        story = serializer.save()

        # Notify followers (implement notification logic if needed)

        serializer = StorySerializer(story, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def story_detail(request, story_id):
    """Get, view, or delete a specific story"""
    story = get_object_or_404(Story, id=story_id)

    if request.method == 'GET':
        # Track view
        if story.user != request.user:
            StoryView.objects.get_or_create(
                story=story,
                user=request.user,
                defaults={'viewed_at': timezone.now()}
            )
            # Increment view count
            Story.objects.filter(id=story.id).update(views_count=F('views_count') + 1)
            story.refresh_from_db()

        serializer = StorySerializer(story, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'DELETE':
        # Only story owner can delete
        if story.user != request.user:
            return Response(
                {'error': 'You can only delete your own stories'},
                status=status.HTTP_403_FORBIDDEN
            )

        story.delete()
        return Response(
            {'message': 'Story deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_stories(request, user_id):
    """Get all active stories for a specific user"""
    user = get_object_or_404(User, id=user_id)

    now = timezone.now()
    stories = Story.objects.filter(
        user=user,
        expires_at__gt=now
    ).order_by('-created_at')

    serializer = StorySerializer(stories, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def react_to_story(request, story_id):
    """Add or remove a reaction to a story"""
    story = get_object_or_404(Story, id=story_id)
    emoji = request.data.get('emoji')

    if not emoji:
        return Response(
            {'error': 'emoji is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if user already reacted
    existing = StoryReaction.objects.filter(
        story=story,
        user=request.user
    ).first()

    if existing:
        # Update reaction
        existing.emoji = emoji
        existing.save()
        serializer = StoryReactionSerializer(existing)
        return Response(serializer.data)
    else:
        # Create new reaction
        reaction = StoryReaction.objects.create(
            story=story,
            user=request.user,
            emoji=emoji
        )
        serializer = StoryReactionSerializer(reaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def blocked_users(request):
    """Get list of blocked users or block a user"""
    if request.method == 'GET':
        blocked = UserBlock.objects.filter(
            blocker=request.user
        ).select_related('blocked')

        serializer = UserBlockSerializer(blocked, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        user_id = request.data.get('user_id')

        if not user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if int(user_id) == request.user.id:
            return Response(
                {'error': 'You cannot block yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_to_block = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if already blocked
        if UserBlock.objects.filter(
            blocker=request.user,
            blocked=user_to_block
        ).exists():
            return Response(
                {'error': 'User is already blocked'},
                status=status.HTTP_400_BAD_REQUEST
            )

        UserBlock.objects.create(
            blocker=request.user,
            blocked=user_to_block
        )

        return Response(
            {'message': f'{user_to_block.username} has been blocked'},
            status=status.HTTP_201_CREATED
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unblock_user(request, user_id):
    """Unblock a user"""
    try:
        block = UserBlock.objects.get(
            blocker=request.user,
            blocked_id=user_id
        )
        block.delete()
        return Response({'message': 'User unblocked successfully'})
    except UserBlock.DoesNotExist:
        return Response(
            {'error': 'User is not blocked'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_typing_indicator(request):
    """Send typing indicator"""
    room_id = request.data.get('room_id')

    if not room_id:
        return Response(
            {'error': 'room_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Verify user is participant
    room = ChatRoom.objects.filter(
        id=room_id,
        chatparticipant__user=request.user
    ).first()

    if not room:
        return Response(
            {'error': 'Room not found or you are not a participant'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Remove old typing indicators
    TypingIndicator.objects.filter(user=request.user).delete()

    # Create new one
    TypingIndicator.objects.create(
        room=room,
        user=request.user
    )

    # Clean up old indicators (older than 5 seconds)
    cutoff = timezone.now() - timezone.timedelta(seconds=5)
    TypingIndicator.objects.filter(created_at__lt=cutoff).delete()

    return Response({'message': 'Typing indicator sent'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def typing_users(request, room_id):
    """Get list of users currently typing in a room"""
    room = get_object_or_404(ChatRoom, id=room_id)

    # Verify user is participant
    if not room.participants.filter(user=request.user).exists():
        return Response(
            {'error': 'You are not a participant in this room'},
            status=status.HTTP_403_FORBIDDEN
        )

    # Clean up old indicators
    cutoff = timezone.now() - timezone.timedelta(seconds=5)
    TypingIndicator.objects.filter(created_at__lt=cutoff).delete()

    # Get current typing users
    typing = TypingIndicator.objects.filter(
        room=room
    ).exclude(user=request.user).select_related('user')

    from .serializers import UserSerializer
    users = [t.user for t in typing]
    serializer = UserSerializer(users, many=True)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def translate_message(request, message_id):
    """
    Translate a chat message using Translation API
    POST /api/chats/messages/<message_id>/translate/
    Body: {"target_language": "ru"}  # "ru", "en", or "zh"
    """
    from video_app.translation_service import translation_service

    message = get_object_or_404(ChatMessage, id=message_id)
    target_language = request.data.get('target_language', 'en')

    # Validate target language
    if target_language not in ['ru', 'en', 'zh']:
        return Response({
            'error': 'Invalid target language. Use "ru", "en", or "zh".'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Check if user is participant in the room
    if not ChatParticipant.objects.filter(
        room=message.room,
        user=request.user
    ).exists():
        return Response({
            'error': 'You are not a participant in this chat room.'
        }, status=status.HTTP_403_FORBIDDEN)

    try:
        # Detect source language
        source = 'auto'
        if translation_service.is_chinese(message.text):
            source = 'zh'
        else:
            # Default to English if not Chinese
            source = 'en'

        # Perform translation
        translated_text = translation_service.translate(
            message.text,
            source=source,
            target=target_language
        )

        if not translated_text:
            return Response({
                'error': 'Translation failed. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Save translation
        if target_language == 'ru':
            message.translation_ru = translated_text
        elif target_language == 'en':
            message.translation_en = translated_text
        else:  # zh
            message.translation_zh = translated_text

        message.translated_at = timezone.now()
        message.save(update_fields=['translation_ru', 'translation_en', 'translation_zh', 'translated_at'])

        # Return updated message
        serializer = ChatMessageSerializer(message, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': f'Translation failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
