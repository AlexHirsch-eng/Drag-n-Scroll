"""
Serializers for Video sharing
"""
from rest_framework import serializers
from .models import Video, VideoLike, VideoComment
from core.models import User


class VideoAuthorSerializer(serializers.ModelSerializer):
    """Full user info for video creator to match frontend expectations"""
    profile = serializers.SerializerMethodField()
    followers_count = serializers.IntegerField(default=0)
    following_count = serializers.IntegerField(default=0)
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile', 'followers_count', 'following_count', 'is_following']
        read_only_fields = ['id', 'username', 'email']

    def get_profile(self, obj):
        """Return profile data or empty dict"""
        if hasattr(obj, 'profile'):
            return {
                'bio': getattr(obj.profile, 'bio', ''),
                'avatar': getattr(obj.profile, 'avatar', None),
            }
        return {}

    def get_is_following(self, obj):
        """Check if current user is following this user"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return hasattr(request.user, 'following') and \
                   request.user.following.filter(following_id=obj.id).exists()
        return False


class VideoSerializer(serializers.ModelSerializer):
    """Serializer for Video model - matches frontend Video interface"""
    creator = VideoAuthorSerializer(source='user', read_only=True)
    # Map video_url to both video_file and url for frontend compatibility
    video_file = serializers.CharField(source='video_url', read_only=True)
    url = serializers.CharField(source='video_url', read_only=True)
    # Map thumbnail_url to thumbnail
    thumbnail = serializers.CharField(source='thumbnail_url', read_only=True)
    # Default values for fields that don't exist in our simplified model
    duration = serializers.IntegerField(default=0)
    category = serializers.SerializerMethodField()
    music_title = serializers.CharField(default='Оригинальный звук')
    shares_count = serializers.IntegerField(default=0)
    is_saved = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = [
            'id', 'creator', 'video_file', 'url', 'thumbnail', 'duration',
            'description', 'category', 'tags', 'music_title',
            'likes_count', 'comments_count', 'views_count', 'shares_count',
            'is_liked', 'is_saved', 'created_at'
        ]
        read_only_fields = [
            'likes_count', 'comments_count', 'views_count', 'created_at',
            'video_file', 'url', 'thumbnail'
        ]

    def get_category(self, obj):
        """Return default category - frontend expects this"""
        return {
            'id': 1,
            'name': 'Общее',
            'description': 'Обучающие видео'
        }

    def get_is_liked(self, obj):
        """Check if current user liked this video"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return VideoLike.objects.filter(
                video=obj,
                user=request.user
            ).exists()
        return False

    def get_is_saved(self, obj):
        """Check if current user saved this video"""
        # For now, return False - we can implement bookmarks later
        return False

    def create(self, validated_data):
        """Create video for current user"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class VideoCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a video"""
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_url', 'thumbnail_url', 'hsk_level', 'tags']


class VideoLikeSerializer(serializers.ModelSerializer):
    """Serializer for video likes"""
    class Meta:
        model = VideoLike
        fields = ['id', 'video', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class VideoCommentSerializer(serializers.ModelSerializer):
    """Serializer for video comments"""
    author = VideoAuthorSerializer(source='user', read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = VideoComment
        fields = ['id', 'author', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def create(self, validated_data):
        """Create comment for current user"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
