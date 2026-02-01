from django.contrib import admin
from .models import Course, CourseDay, Lesson, LessonStep


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'hsk_level', 'total_days', 'is_active']
    list_filter = ['hsk_level', 'is_active']
    search_fields = ['title', 'description']


@admin.register(CourseDay)
class CourseDayAdmin(admin.ModelAdmin):
    list_display = ['course', 'day_number', 'title', 'estimated_minutes']
    list_filter = ['course', 'day_number']
    search_fields = ['title', 'description']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['course_day', 'lesson_type', 'title', 'hsk_level', 'estimated_minutes']
    list_filter = ['lesson_type', 'hsk_level', 'course_day__course']
    search_fields = ['title', 'description']


@admin.register(LessonStep)
class LessonStepAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'step_type', 'order', 'estimated_minutes']
    list_filter = ['step_type', 'lesson__course_day__course']
    search_fields = ['title']
    filter_horizontal = ['words', 'grammar_rules']
