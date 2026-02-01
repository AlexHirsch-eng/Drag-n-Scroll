from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, UserCourseProgress


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'created_at', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'created_at']
    search_fields = ['username', 'email']
    ordering = ['-created_at']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'learning_language', 'current_hsk_level']
    list_filter = ['learning_language', 'current_hsk_level']
    search_fields = ['user__username']


@admin.register(UserCourseProgress)
class UserCourseProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_day', 'total_xp', 'streak_days', 'last_study_date']
    list_filter = ['current_day', 'streak_days', 'last_study_date']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at']
