"""
Serializers for course app
"""
from rest_framework import serializers
from .models import Course, CourseDay, Lesson, LessonStep


class LessonStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonStep
        fields = [
            'id', 'step_type', 'title', 'content', 'order',
            'estimated_minutes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class LessonSerializer(serializers.ModelSerializer):
    steps = LessonStepSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = [
            'id', 'lesson_type', 'hsk_level', 'title', 'title_zh',
            'description', 'order', 'estimated_minutes',
            'steps', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class CourseDaySerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = CourseDay
        fields = [
            'id', 'day_number', 'title', 'title_zh', 'description',
            'estimated_minutes', 'order', 'lessons', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class CourseSerializer(serializers.ModelSerializer):
    days = CourseDaySerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'title_zh', 'description', 'hsk_level',
            'total_days', 'order', 'is_active', 'days', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class CourseListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for course listings"""
    class Meta:
        model = Course
        fields = ['id', 'title', 'hsk_level', 'total_days', 'is_active']
