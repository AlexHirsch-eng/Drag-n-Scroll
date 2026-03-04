from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import UserProfile


class Command(BaseCommand):
    help = 'Create demo chat users for testing'

    def handle(self, *args, **options):
        User = get_user_model()

        demo_users = [
            {
                'username': 'Li_Mei',
                'email': 'li.mei@example.com',
                'password': 'DemoUser123',
                'bio': 'Преподаватель китайского языка из Пекина 🇨🇳'
            },
            {
                'username': 'Wang_Wei',
                'email': 'wang.wei@example.com',
                'password': 'DemoUser123',
                'bio': 'Изучает русский язык, любит общаться 📚'
            },
            {
                'username': 'Chen_Yu',
                'email': 'chen.yu@example.com',
                'password': 'DemoUser123',
                'bio': 'Студент университета, помогает с практикой 🎓'
            }
        ]

        created_count = 0
        skipped_count = 0

        for user_data in demo_users:
            username = user_data['username']
            email = user_data['email']
            password = user_data['password']
            bio = user_data['bio']

            # Check if user exists
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f'✓ User {username} already exists, skipping...'))
                skipped_count += 1
                continue

            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Create profile
            UserProfile.objects.create(
                user=user,
                bio=bio,
                learning_language='RU',
                current_hsk_level=3
            )

            self.stdout.write(self.style.SUCCESS(f'✓ Created user: {username}'))
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f'\n✅ Created: {created_count} users'))
        if skipped_count > 0:
            self.stdout.write(self.style.WARNING(f'⚠ Skipped: {skipped_count} users (already exist)'))

        self.stdout.write('\nLogin credentials:')
        self.stdout.write('  Username: Li_Mei, Wang_Wei, or Chen_Yu')
        self.stdout.write('  Password: DemoUser123')
