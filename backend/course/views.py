"""
Views for course app
"""
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course, CourseDay, Lesson, LessonStep
from .serializers import (
    CourseSerializer,
    CourseListSerializer,
    CourseDaySerializer,
    LessonSerializer,
    LessonStepSerializer
)


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing courses
    """
    queryset = Course.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CourseSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        return CourseSerializer

    @action(detail=False, methods=['get'])
    def by_hsk(self, request):
        """Get courses by HSK level"""
        hsk_level = request.query_params.get('hsk_level')
        if hsk_level:
            courses = self.queryset.filter(hsk_level=hsk_level)
        else:
            courses = self.queryset
        serializer = CourseListSerializer(courses, many=True)
        return Response(serializer.data)


class CourseDayViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing course days
    """
    queryset = CourseDay.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CourseDaySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        course_id = self.request.query_params.get('course_id')
        day_number = self.request.query_params.get('day_number')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        if day_number:
            queryset = queryset.filter(day_number=day_number)
        return queryset


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing lessons
    """
    queryset = Lesson.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LessonSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        course_day_id = self.request.query_params.get('course_day_id')
        if course_day_id:
            queryset = queryset.filter(course_day_id=course_day_id)
        return queryset


class LessonStepViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing lesson steps
    """
    queryset = LessonStep.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LessonStepSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        lesson_id = self.request.query_params.get('lesson_id')
        if lesson_id:
            queryset = queryset.filter(lesson_id=lesson_id).order_by('order')
        return queryset
