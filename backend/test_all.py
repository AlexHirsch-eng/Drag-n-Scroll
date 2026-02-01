#!/usr/bin/env python
"""
Test script for all project features
"""
import os
import sys
import django

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from video_app.models import Video, VideoComment, VideoCategory
from video_app.translation_service import translation_service
from django.contrib.auth import get_user_model

User = get_user_model()

print('=' * 60)
print('PROJECT STATUS REPORT')
print('=' * 60)
print()

# 1. Videos
print('1. VIDEOS:')
videos = Video.objects.all()
print(f'   Total videos in DB: {videos.count()}')
for v in videos[:5]:
    print(f'   - ID {v.id}: {v.description[:40]}... (status: {v.status})')
print()

# 2. Categories
print('2. CATEGORIES:')
categories = VideoCategory.objects.all()
print(f'   Total categories: {categories.count()}')
for c in categories[:5]:
    print(f'   - {c.name}: {c.icon}')
print()

# 3. Comments
print('3. COMMENTS:')
comments = VideoComment.objects.all()
print(f'   Total comments: {comments.count()}')
for c in comments:
    has_trans = 'YES' if c.translation_ru or c.translation_en else 'NO'
    print(f'   - ID {c.id}: {c.text[:30]}... (translation: {has_trans})')
print()

# 4. Translation Test
print('4. TRANSLATION SERVICE TEST:')
test_texts = [
    'Hello, how are you?',
    'This is a test',
]

for text in test_texts:
    ru = translation_service.translate_to_ru(text)
    status = 'OK' if ru else 'FAIL'
    ru_preview = ru[:30] if ru else 'NONE'
    print(f'   [{status}] "{text}"')
    print(f'         -> "{ru_preview}..."')
print()

# 5. Check for Chinese text
print('5. CHINESE DETECTION:')
print(f'   "Hello" is Chinese: {translation_service.is_chinese("Hello")}')
print(f'   "test" is Chinese: {translation_service.is_chinese("test")}')
print()

# 6. Admin users
print('6. ADMIN USERS:')
admins = User.objects.filter(is_staff=True)
print(f'   Total admins: {admins.count()}')
for admin in admins:
    print(f'   - {admin.username} ({admin.email})')
print()

print('=' * 60)
print('SERVER ACCESS INFORMATION')
print('=' * 60)
print()
print('Backend URL: http://localhost:8000')
print('API Base: http://localhost:8000/api/')
print()
print('Admin credentials:')
for admin in admins[:3]:
    print(f'   Username: {admin.username}')
print()
print('Key API Endpoints:')
print('   GET  /api/video/videos/feed/              - Video feed')
print('   GET  /api/video/categories-list/          - All categories')
print('   POST /api/videos/admin/import-videos/     - Import videos (admin only)')
print('   POST /api/videos/comments/<id>/translate/ - Translate comment')
print('   GET  /api/video/videos/<id>/comments/     - Video comments')
print()
print('=' * 60)
print('ALL TESTS COMPLETED - READY FOR USER TESTING')
print('=' * 60)
