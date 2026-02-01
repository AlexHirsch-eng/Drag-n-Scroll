"""
Import videos from Downloads folder automatically
"""
import os
import django
import json
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from video_app.models import Video, VideoCategory, VideoComment
from django.core.files import File
from django.utils.text import slugify

VIDEO_EXTENSIONS = ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv']
DOWNLOADS_FOLDER = r'C:\Users\aibat\Downloads\v'

def import_single_video(video_path: Path) -> dict:
    """Import a single video file"""
    print(f"Processing: {video_path.name}")

    # Get video info
    stat = video_path.stat()
    size_mb = stat.st_size / (1024 * 1024)

    # Basic info from filename
    # You can enhance this with actual video metadata extraction
    title = video_path.stem  # filename without extension

    # Generate slug
    slug = slugify(title)

    # Try to get duration and other metadata using ffmpeg (optional)
    duration = None
    thumbnail = None

    # Check if video already exists
    existing = Video.objects.filter(title=title).first()
    if existing:
        print(f"  - Video already exists, skipping")
        return {'status': 'exists', 'title': title}

    # Get or create default category
    category, _ = VideoCategory.objects.get_or_create(
        name='Imported',
        defaults={'slug': 'imported'}
    )

    # Create video
    try:
        video = Video.objects.create(
            title=title,
            slug=slug,
            description=f'Автоматически импортировано из {video_path.name}',
            category=category,
            video_file=f'videos/{slug}{video_path.suffix}',
            duration=duration or 0,
            views=0,
            is_active=True
        )

        # Copy file to media directory
        media_path = Path('media/videos') / f'{slug}{video_path.suffix}'
        media_path.parent.mkdir(parents=True, exist_ok=True)

        import shutil
        shutil.copy2(video_path, media_path)

        print(f"  ✓ Imported: {title}")
        return {'status': 'success', 'title': title, 'id': video.id}

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return {'status': 'error', 'title': title, 'error': str(e)}

def scan_folder():
    """Scan Downloads/v folder and import all videos"""
    folder = Path(DOWNLOADS_FOLDER)

    if not folder.exists():
        print(f"Folder not found: {DOWNLOADS_FOLDER}")
        return

    print(f"Scanning folder: {folder}")

    # Find all video files
    video_files = []
    for ext in VIDEO_EXTENSIONS:
        video_files.extend(folder.glob(f'*{ext}'))
        video_files.extend(folder.glob(f'*{ext.upper()}'))

    print(f"Found {len(video_files)} video files")

    results = {
        'total': len(video_files),
        'imported': 0,
        'skipped': 0,
        'errors': 0
    }

    for video_file in video_files:
        try:
            result = import_single_video(video_file)
            if result['status'] == 'success':
                results['imported'] += 1
            elif result['status'] == 'exists':
                results['skipped'] += 1
            else:
                results['errors'] += 1
        except Exception as e:
            print(f"Error processing {video_file.name}: {e}")
            results['errors'] += 1

    print(f"\nResults:")
    print(f"  Imported: {results['imported']}")
    print(f"  Skipped (already exists): {results['skipped']}")
    print(f"  Errors: {results['errors']}")

    return results

if __name__ == '__main__':
    scan_folder()
