"""
Script to add videos from media/videos folder to the database
Usage: python manage.py shell < add_videos_from_folder.py
"""
import os
from django.conf import settings
from django.core.files import File
from core.models import User
from video_app.models import Video, VideoCategory

def add_videos_from_folder():
    # Get the default user (or create one)
    user = User.objects.first()
    if not user:
        print("Error: No users found. Please create a user first.")
        return

    # Get or create default category
    category, _ = VideoCategory.objects.get_or_create(
        name='Learning',
        defaults={
            'icon': '📚',
            'description': 'Learning videos',
            'order': 1
        }
    )

    # Path to videos folder
    videos_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
    thumbnails_dir = os.path.join(settings.MEDIA_ROOT, 'video_thumbnails')

    if not os.path.exists(videos_dir):
        print(f"Error: Videos folder not found: {videos_dir}")
        print("Please create the folder and add your videos there.")
        return

    # Supported video formats
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
    thumbnail_extensions = ['.jpg', '.jpeg', '.png', '.webp']

    # Get all video files
    video_files = []
    for file in os.listdir(videos_dir):
        ext = os.path.splitext(file)[1].lower()
        if ext in video_extensions:
            video_files.append(file)

    if not video_files:
        print(f"No video files found in {videos_dir}")
        print(f"Supported formats: {', '.join(video_extensions)}")
        return

    print(f"Found {len(video_files)} video files")
    print("-" * 50)

    added_count = 0
    skipped_count = 0

    for video_file in video_files:
        video_path = os.path.join(videos_dir, video_file)
        video_name = os.path.splitext(video_file)[0]

        # Check if video already exists
        if Video.objects.filter(video_file__icontains=video_file).exists():
            print(f"⏭️  Skipping: {video_file} (already exists)")
            skipped_count += 1
            continue

        # Look for matching thumbnail
        thumbnail_path = None
        for thumb_ext in thumbnail_extensions:
            thumb_file = f"{video_name}{thumb_ext}"
            full_thumb_path = os.path.join(thumbnails_dir, thumb_file)
            if os.path.exists(full_thumb_path):
                thumbnail_path = full_thumb_path
                break

        # Get video duration (you'll need to specify or use ffprobe)
        # For now, default to 60 seconds
        duration = 60

        # Create the video
        try:
            with open(video_path, 'rb') as f:
                video = Video.objects.create(
                    creator=user,
                    video_file=File(f, name=video_file),
                    description=f"Learning video: {video_name}",
                    category=category,
                    duration=duration,
                    status='ready',
                    tags=['learning', 'chinese'],
                    is_featured=True
                )

                # Add thumbnail if found
                if thumbnail_path:
                    with open(thumbnail_path, 'rb') as thumb_f:
                        video.thumbnail.save(
                            f"{video_name}.jpg",
                            File(thumb_f),
                            save=True
                        )

                print(f"✅ Added: {video_file}")
                if thumbnail_path:
                    print(f"   with thumbnail: {os.path.basename(thumbnail_path)}")
                added_count += 1

        except Exception as e:
            print(f"❌ Error adding {video_file}: {e}")

    print("-" * 50)
    print(f"Done! Added {added_count} videos, skipped {skipped_count}")
    print(f"Total videos in database: {Video.objects.count()}")

if __name__ == '__main__':
    add_videos_from_folder()
