"""
Serializers for Video sharing
"""
from rest_framework import serializers
from .models import Video, VideoLike, VideoComment
from core.models import User


class VideoAuthorSerializer(serializers.ModelSerializer):
    """Minimal user info for video author"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id', 'username', 'email']


class VideoSerializer(serializers.ModelSerializer):
    """Serializer for Video model"""
    author = VideoAuthorSerializer(source='user', read_only=True)
    is_liked = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    views_count = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Video
        fields = [
            'id', 'author', 'title', 'description', 'video_url', 'thumbnail_url',
            'hsk_level', 'tags', 'likes_count', 'comments_count', 'views_count',
            'is_liked', 'created_at'
        ]
        read_only_fields = ['likes_count', 'comments_count', 'views_count', 'created_at']

    def get_is_liked(self, obj):
        """Check if current user liked this video"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return VideoLike.objects.filter(
                video=obj,
                user=request.user
            ).exists()
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
