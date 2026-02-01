"""
Serializers for core app
"""
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from .models import User, UserProfile, UserCourseProgress


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['learning_language', 'current_hsk_level', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class UserCourseProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCourseProgress
        fields = [
            'current_day', 'current_lesson', 'current_step',
            'total_xp', 'streak_days', 'last_study_date',
            'completed_days', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(BaseUserSerializer):
    profile = UserProfileSerializer(read_only=True)
    progress = UserCourseProgressSerializer(read_only=True)

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = [
            'id', 'username', 'email', 'profile', 'progress',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserCreateSerializer(BaseUserCreateSerializer):
    """
    Serializer for user registration with additional fields
    """
    learning_language = serializers.ChoiceField(
        choices=[('RU', 'Russian'), ('KZ', 'Kazakh')],
        default='RU',
        write_only=True,
        required=False
    )

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ['username', 'email', 'password', 'learning_language']

    def validate(self, attrs):
        """
        Remove learning_language before passing to parent validation
        """
        # Extract learning_language before validation
        self._learning_language = attrs.pop('learning_language', 'RU')
        # Call parent validation without learning_language
        return super().validate(attrs)

    def create(self, validated_data):
        """
        Create user with profile and progress
        """
        user = super().create(validated_data)

        # Create user profile with learning_language
        UserProfile.objects.create(
            user=user,
            learning_language=self._learning_language
        )

        # Create user progress
        UserCourseProgress.objects.create(user=user)

        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Detailed user serializer for profile endpoint
    """
    profile = UserProfileSerializer(read_only=True)
    progress = UserCourseProgressSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'profile', 'progress', 'date_joined'
        ]
        read_only_fields = ['date_joined']
