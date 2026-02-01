"""
Add icons to video categories
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from video_app.models import VideoCategory

# Update categories with icons
categories_data = [
    ('Vocabulary', '📖'),
    ('Grammar', '📝'),
    ('Listening', '🎧'),
    ('Speaking', '🗣️'),
    ('Writing', '✍️'),
    ('Culture', '🏮'),
    ('Tips', '💡'),
    ('Reading', '📚'),
]

for name, icon in categories_data:
    category = VideoCategory.objects.filter(name=name).first()
    if category:
        category.icon = icon
        category.save()
        print(f'Updated {name} with icon {icon}')
    else:
        print(f'Category {name} not found')

print('All categories updated!')
