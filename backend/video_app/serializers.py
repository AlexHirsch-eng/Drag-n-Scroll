from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Video, VideoCategory, VideoView, VideoLike, VideoBookmark,
    VideoComment, VideoCommentLike, VideoShare, VideoReport,
    VideoHashtag, UserFollowing
)

User = get_user_model()


class VideoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCategory
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile', 'followers_count', 'following_count', 'is_following']

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserFollowing.objects.filter(
                follower=request.user,
                following=obj
            ).exists()
        return False


class VideoListSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    category = VideoCategorySerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = [
            'id', 'creator', 'video_file', 'url', 'thumbnail', 'duration',
            'description', 'category', 'tags', 'music_title',
            'lesson_number', 'lesson_title', 'lesson_words',
            'views_count', 'likes_count', 'comments_count', 'shares_count',
            'is_liked', 'is_saved', 'created_at'
        ]

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return VideoLike.objects.filter(
                video=obj,
                user=request.user
            ).exists()
        return False

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return VideoBookmark.objects.filter(
                video=obj,
                user=request.user
            ).exists()
        return False

    def get_url(self, obj):
        if obj.video_file:
            return obj.video_file.url
        return None


class VideoDetailSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    category = VideoCategorySerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = '__all__'

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return VideoLike.objects.filter(
                video=obj,
                user=request.user
            ).exists()
        return False

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return VideoBookmark.objects.filter(
                video=obj,
                user=request.user
            ).exists()
        return False

    def get_url(self, obj):
        if obj.video_file:
            return obj.video_file.url
        return None


class VideoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            'video_file', 'thumbnail', 'duration', 'description',
            'category', 'tags', 'music_title',
            'lesson_number', 'lesson_title', 'lesson_words'
        ]

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)


class VideoCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = VideoComment
        fields = [
            'id', 'video', 'user', 'parent', 'text', 'likes_count',
            'is_liked', 'replies', 'created_at', 'updated_at',
            'translation_ru', 'translation_en', 'translated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

    def get_replies(self, obj):
        # Only return direct replies (not nested)
        if obj.parent is None:
            replies = VideoComment.objects.filter(parent=obj, is_deleted=False)
            return VideoCommentSerializer(replies, many=True).data
        return []

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return VideoCommentLike.objects.filter(
                comment=obj,
                user=request.user
            ).exists()
        return False


class VideoCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoComment
        fields = ['video', 'text', 'parent']
        extra_kwargs = {
            'video': {'required': False}
        }

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class VideoLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoLike
        fields = ['video', 'user', 'created_at']
        read_only_fields = ['user', 'created_at']


class VideoBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoBookmark
        fields = ['video', 'user', 'created_at']
        read_only_fields = ['user', 'created_at']


class VideoViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoView
        fields = ['video', 'user', 'viewed_at']
        read_only_fields = ['user', 'viewed_at']


class VideoShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoShare
        fields = ['video', 'user', 'platform', 'shared_at']
        read_only_fields = ['shared_at']


class VideoReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoReport
        fields = ['video', 'reporter', 'reason', 'description', 'is_reviewed', 'action_taken']
        read_only_fields = ['reporter', 'is_reviewed', 'action_taken']


class VideoHashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoHashtag
        fields = ['tag', 'uses_count']


class UserFollowingSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    following = UserSerializer(read_only=True)

    class Meta:
        model = UserFollowing
        fields = ['id', 'follower', 'following', 'created_at']


class UserFollowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ['following']

    def validate_following(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError("You cannot follow yourself.")
        return value

    def create(self, validated_data):
        validated_data['follower'] = self.context['request'].user
        return super().create(validated_data)
