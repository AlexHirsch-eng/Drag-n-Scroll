"""
Create UserProfile and UserCourseProgress for users who don't have them
Run: python manage.py create_user_profiles
"""

import sys
import io
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

User = get_user_model()


class Command(BaseCommand):
    help = 'Create UserProfile and UserCourseProgress for users who do not have them'

    def handle(self, *args, **options):
        from core.models import UserProfile, UserCourseProgress

        self.stdout.write('[INFO] Checking users without profiles or progress...')

        # Count users missing profile or progress
        users_without_profile = User.objects.filter(profile__isnull=True)
        users_without_progress = User.objects.filter(progress__isnull=True)

        profile_count = 0
        progress_count = 0

        # Create profiles for users who don't have one
        for user in users_without_profile:
            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'learning_language': 'RU',
                    'current_hsk_level': 1,
                    'bio': f'Learning Chinese! {user.first_name if user.first_name else "Student"}'
                }
            )
            profile_count += 1
            self.stdout.write(f'  [OK] Created profile for {user.username}')

        # Create progress for users who don't have one
        for user in users_without_progress:
            UserCourseProgress.objects.get_or_create(user=user)
            progress_count += 1
            self.stdout.write(f'  [OK] Created progress for {user.username}')

        # Summary
        total_users = User.objects.count()
        users_with_profile = User.objects.filter(profile__isnull=False).count()
        users_with_progress = User.objects.filter(progress__isnull=False).count()

        self.stdout.write(self.style.SUCCESS(
            f'\n[SUMMARY]\n'
            f'Total users: {total_users}\n'
            f'Users with profile: {users_with_profile}/{total_users}\n'
            f'Users with progress: {users_with_progress}/{total_users}\n'
            f'Profiles created: {profile_count}\n'
            f'Progress records created: {progress_count}'
        ))
