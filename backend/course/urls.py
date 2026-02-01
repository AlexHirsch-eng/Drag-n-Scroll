"""
URL configuration for course app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, CourseDayViewSet, LessonViewSet, LessonStepViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'days', CourseDayViewSet, basename='courseday')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'steps', LessonStepViewSet, basename='lessonstep')

urlpatterns = [
    path('', include(router.urls)),
]
