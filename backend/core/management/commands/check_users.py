"""
Check and fix user data integrity
Run: python manage.py check_users
"""

import sys
import io
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection
from django.core.management import call_command

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

User = get_user_model()


class Command(BaseCommand):
    help = 'Check and fix user data integrity'

    def handle(self, *args, **options):
        from core.models import UserProfile, UserCourseProgress

        self.stdout.write('\n' + '='*50)
        self.stdout.write('[USER DATA INTEGRITY CHECK]')
        self.stdout.write('='*50)

        # Check database connection
        self.stdout.write('\n[1] Checking database connection...')
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            self.stdout.write(self.style.SUCCESS('    ✓ Database connection OK'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'    ✗ Database connection failed: {e}'))
            return

        # Count total users
        total_users = User.objects.count()
        self.stdout.write(f'\n[2] Total users in database: {total_users}')

        # Check active users
        active_users = User.objects.filter(is_active=True).count()
        inactive_users = total_users - active_users
        self.stdout.write(f'    Active users: {active_users}')
        self.stdout.write(f'    Inactive users: {inactive_users}')

        # Check users without profile
        users_without_profile = User.objects.filter(profile__isnull=True).count()
        self.stdout.write(f'\n[3] Users without profile: {users_without_profile}')

        if users_without_profile > 0:
            self.stdout.write(f'    Creating profiles for {users_without_profile} users...')
            for user in User.objects.filter(profile__isnull=True):
                UserProfile.objects.get_or_create(
                    user=user,
                    defaults={'learning_language': 'RU'}
                )
            self.stdout.write(self.style.SUCCESS(f'    ✓ Created {users_without_profile} profiles'))

        # Check users without progress
        users_without_progress = User.objects.filter(progress__isnull=True).count()
        self.stdout.write(f'\n[4] Users without progress: {users_without_progress}')

        if users_without_progress > 0:
            self.stdout.write(f'    Creating progress for {users_without_progress} users...')
            for user in User.objects.filter(progress__isnull=True):
                UserCourseProgress.objects.get_or_create(user=user)
            self.stdout.write(self.style.SUCCESS(f'    ✓ Created {users_without_progress} progress records'))

        # Verify all users have profile and progress
        users_with_profile = User.objects.filter(profile__isnull=False).count()
        users_with_progress = User.objects.filter(progress__isnull=False).count()

        self.stdout.write(f'\n[5] Final verification:')
        self.stdout.write(f'    Users with profile: {users_with_profile}/{total_users}')
        self.stdout.write(f'    Users with progress: {users_with_progress}/{total_users}')

        if users_with_profile == total_users and users_with_progress == total_users:
            self.stdout.write(self.style.SUCCESS('\n✓ All users have complete data!'))
        else:
            self.stdout.write(self.style.WARNING('\n⚠ Some users are missing data'))

        # Show recent users
        self.stdout.write(f'\n[6] Recent users (last 5):')
        for user in User.objects.order_by('-created_at')[:5]:
            has_profile = hasattr(user, 'profile') and user.profile is not None
            has_progress = hasattr(user, 'progress') and user.progress is not None
            status = '✓' if (has_profile and has_progress) else '✗'
            self.stdout.write(
                f'    {status} {user.username} '
                f'({user.email}) - '
                f'Profile: {"Yes" if has_profile else "No"}, '
                f'Progress: {"Yes" if has_progress else "No"}'
            )

        self.stdout.write('\n' + '='*50)
        self.stdout.write('[CHECK COMPLETE]')
        self.stdout.write('='*50 + '\n')
