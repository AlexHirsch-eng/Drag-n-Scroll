"""
Create test users with passwords for login
Run: python manage.py create_test_users
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
    help = 'Create test users with known passwords for development'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating test users with passwords...'))

        # Test users with passwords
        test_users = [
            {
                'username': 'alex_chen',
                'email': 'alex@example.com',
                'password': 'test123456',
                'first_name': 'Alex',
                'last_name': 'Chen',
                'bio': 'Learning Chinese for 2 years'
            },
            {
                'username': 'emma_wang',
                'email': 'emma@example.com',
                'password': 'test123456',
                'first_name': 'Emma',
                'last_name': 'Wang',
                'bio': 'HSK 4 student'
            },
            {
                'username': 'david_liu',
                'email': 'david@example.com',
                'password': 'test123456',
                'first_name': 'David',
                'last_name': 'Liu',
                'bio': 'Love Chinese culture'
            },
            {
                'username': 'sophia_zhang',
                'email': 'sophia@example.com',
                'password': 'test123456',
                'first_name': 'Sophia',
                'last_name': 'Zhang',
                'bio': 'Native speaker helping learners'
            },
            {
                'username': 'michael_wu',
                'email': 'michael@example.com',
                'password': 'test123456',
                'first_name': 'Michael',
                'last_name': 'Wu',
                'bio': 'Business Chinese learner'
            },
            {
                'username': 'lisa_ma',
                'email': 'lisa@example.com',
                'password': 'test123456',
                'first_name': 'Lisa',
                'last_name': 'Ma',
                'bio': 'Preparing for HSK 5'
            },
            {
                'username': 'xiaoming_teacher',
                'email': 'xiaoming_t@example.com',
                'password': 'test123456',
                'first_name': 'Xiao',
                'last_name': 'Ming',
                'bio': 'Chinese teacher'
            },
            {
                'username': 'mei_ling',
                'email': 'mei_l@example.com',
                'password': 'test123456',
                'first_name': 'Mei',
                'last_name': 'Ling',
                'bio': 'Content creator'
            },
        ]

        created_count = 0
        updated_count = 0

        for user_data in test_users:
            password = user_data.pop('password')
            bio = user_data.pop('bio', '')

            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )

            # Always set/update password
            user.set_password(password)
            user.save()

            if created:
                created_count += 1
                self.stdout.write(f'  ✓ Created user: {user.username}')
            else:
                updated_count += 1
                self.stdout.write(f'  ⊙ Updated password for: {user.username}')

        self.stdout.write(self.style.SUCCESS('\n[OK] Test users created successfully!'))
        self.stdout.write('\n' + '='*60)
        self.stdout.write('LOGIN CREDENTIALS:')
        self.stdout.write('='*60)
        self.stdout.write('Username: alex_chen       | Password: test123456')
        self.stdout.write('Username: emma_wang       | Password: test123456')
        self.stdout.write('Username: david_liu       | Password: test123456')
        self.stdout.write('Username: sophia_zhang    | Password: test123456')
        self.stdout.write('Username: michael_wu      | Password: test123456')
        self.stdout.write('Username: lisa_ma         | Password: test123456')
        self.stdout.write('Username: xiaoming_teacher| Password: test123456')
        self.stdout.write('Username: mei_ling        | Password: test123456')
        self.stdout.write('='*60)
        self.stdout.write('\nAll users have the same password: test123456')
        self.stdout.write(f'\nCreated: {created_count} | Updated: {updated_count}')
        self.stdout.write('\nYou can now login and explore the chats! 加油！')
