#!/usr/bin/env python
"""
Create demo chat users for testing
Run with: python manage.py shell < create_demo_users.py
"""

from django.contrib.auth import get_user_model
from core.models import UserProfile

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

for user_data in demo_users:
    username = user_data['username']
    email = user_data['email']
    password = user_data['password']
    bio = user_data['bio']

    # Check if user exists
    if User.objects.filter(username=username).exists():
        print(f"✓ User {username} already exists, skipping...")
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

    print(f"✓ Created user: {username}")

print("\n✅ All demo users created successfully!")
print("\nLogin credentials:")
print("Username: Li_Mei, Wang_Wei, or Chen_Yu")
print("Password: DemoUser123")
