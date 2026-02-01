"""
Simple script to add videos to the database
Usage: python add_video.py <video_file.mp4> [thumbnail.jpg]
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.files import File
from core.models import User
from video_app.models import Video, VideoCategory

def add_video(video_path, thumbnail_path=None):
    """Add a single video to the database"""
    if not os.path.exists(video_path):
        print(f"[ERROR] Video file not found: {video_path}")
        return

    # Get default user
    user = User.objects.first()
    if not user:
        print("[ERROR] No users found. Please create a user first:")
        print("        python manage.py createsuperuser")
        return

    # Get or create category
    category, _ = VideoCategory.objects.get_or_create(
        name='Learning',
        defaults={
            'icon': '📚',
            'description': 'Learning videos',
            'order': 1
        }
    )

    video_filename = os.path.basename(video_path)
    video_name = os.path.splitext(video_filename)[0]

    # Check if already exists
    if Video.objects.filter(video_file__icontains=video_filename).exists():
        print(f"[SKIP] Video already exists: {video_filename}")
        return

    try:
        # Create video
        with open(video_path, 'rb') as f:
            video = Video.objects.create(
                creator=user,
                video_file=File(f, name=video_filename),
                description=f"Learning video: {video_name}",
                category=category,
                duration=60,  # Default duration (you can edit later)
                status='ready',
                tags=['learning', 'chinese'],
                is_featured=True
            )

        # Add thumbnail if provided
        if thumbnail_path and os.path.exists(thumbnail_path):
            thumb_filename = os.path.basename(thumbnail_path)
            with open(thumbnail_path, 'rb') as thumb_f:
                video.thumbnail.save(
                    thumb_filename,
                    File(thumb_f),
                    save=True
                )
            print(f"[OK] Video added: {video_filename}")
            print(f"     Thumbnail: {thumb_filename}")
        else:
            print(f"[OK] Video added: {video_filename}")
            print(f"     (No thumbnail)")

        print(f"     Video ID: {video.id}")
        print(f"     URL: /api/video/videos/{video.id}/")

    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python add_video.py <video_file.mp4> [thumbnail.jpg]")
        print("\nExamples:")
        print("  python add_video.py my_video.mp4")
        print("  python add_video.py my_video.mp4 my_thumbnail.jpg")
        sys.exit(1)

    video_path = sys.argv[1]
    thumbnail_path = sys.argv[2] if len(sys.argv) > 2 else None

    add_video(video_path, thumbnail_path)
