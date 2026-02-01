"""
Create test user with known password
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create or update test user
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={
        'email': 'test@example.com'
    }
)

user.set_password('testpass123')
user.save()

print(f'User {"created" if created else "updated"}: testuser / testpass123')
print('Use these credentials to login')
