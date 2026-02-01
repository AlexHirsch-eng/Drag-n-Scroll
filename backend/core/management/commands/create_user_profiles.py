"""
Create UserProfile for users who don't have one
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
    help = 'Create UserProfile for users who do not have one'

    def handle(self, *args, **options):
        from core.models import UserProfile

        users_without_profile = User.objects.filter(profile__isnull=True)
        count = 0

        for user in users_without_profile:
            UserProfile.objects.create(
                user=user,
                learning_language='RU',
                current_hsk_level=1,
                bio=f'Learning Chinese! {user.first_name if user.first_name else "Student"}'
            )
            count += 1
            self.stdout.write(f'  [OK] Created profile for {user.username}')

        self.stdout.write(self.style.SUCCESS(f'\n[OK] Created {count} user profiles'))
