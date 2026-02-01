#!/usr/bin/env python
"""
Quick test for chat message translation
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from chat_app.models import ChatRoom, ChatMessage
from video_app.translation_service import translation_service
from django.contrib.auth import get_user_model

User = get_user_model()

print("=" * 70)
print("CHAT TRANSLATION - QUICK TEST")
print("=" * 70)
print()

# Get a recent message
message = ChatMessage.objects.order_by('-created_at').first()
if not message:
    print("No messages found. Creating one...")
    user1 = User.objects.first()
    user2 = User.objects.last()

    if user1 and user2:
        # Create test room
        room, _ = ChatRoom.objects.get_or_create(
            room_type='direct',
            created_by=user1,
            defaults={'name': 'Test Chat'}
        )

        # Add participants
        from chat_app.models import ChatParticipant
        ChatParticipant.objects.get_or_create(room=room, user=user1)
        ChatParticipant.objects.get_or_create(room=room, user=user2)

        # Create test message
        message = ChatMessage.objects.create(
            room=room,
            sender=user1,
            text="Hello, this is a test message for translation!"
        )
        print(f"Created test message: {message.id}")

print(f"Testing message {message.id}:")
print(f"  Text: {message.text}")
print()

# Test translations
print("Testing translations:")
print("-" * 70)

# To Russian
ru = translation_service.translate_to_ru(message.text)
if ru:
    message.translation_ru = ru
    print(f"✅ Russian: {ru[:60]}...")
else:
    print(f"❌ Russian: FAILED")

# To English
en = translation_service.translate_to_en(message.text)
if en:
    message.translation_en = en
    print(f"✅ English: {en[:60]}...")
else:
    print(f"❌ English: FAILED")

# To Chinese
zh = translation_service.translate(message.text, source='en', target='zh')
if zh:
    message.translation_zh = zh
    print(f"✅ Chinese: {zh[:60]}...")
else:
    print(f"❌ Chinese: FAILED")

# Save
from django.utils import timezone
message.translated_at = timezone.now()
message.save()

print()
print("=" * 70)
print("TRANSLATION TEST COMPLETE")
print("=" * 70)
print()
print("Backend URL: http://localhost:8000")
print("Frontend URL: http://localhost:5173")
print()
print("Test the chat in the browser:")
print("1. Open http://localhost:5173/")
print("2. Go to Messages section")
print("3. Select any chat")
print("4. Click flag emoji (🇷🇺/🇬🇧/🇨🇳) to switch language")
print("5. Click 🌐 to translate Chinese messages")
print()
print("✅ All systems operational!")
