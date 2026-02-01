"""
Admin views for video import
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import os
from pathlib import Path

VIDEO_EXTENSIONS = ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv']
DOWNLOADS_FOLDER = r'C:\Users\aibat\Downloads\v'

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
@csrf_exempt
def import_videos_from_folder(request):
    """
    Import all videos from Downloads/v folder
    Admin only endpoint
    """
    from django.contrib.auth import get_user_model
    from video_app.models import Video, VideoCategory
    from django.core.files import File
        from django.utils.text import slugify
    import shutil

    User = get_user_model()

    folder = Path(DOWNLOADS_FOLDER)
    if not folder.exists():
        return Response({
            'error': f'Folder not found: {DOWNLOADS_FOLDER}'
        }, status=400)

    # Find all video files
    video_files = []
    for ext in VIDEO_EXTENSIONS:
        video_files.extend(folder.glob(f'*{ext}'))
        video_files.extend(folder.glob(f'*{ext.upper()}'))

    results = {
        'total': len(video_files),
        'imported': 0,
        'skipped': 0,
        'errors': 0,
        'videos': []
    }

    for video_file in video_files:
        try:
            title = video_file.stem
            slug = slugify(title)

            # Check if exists
            existing = Video.objects.filter(slug=slug).first()
            if existing:
                results['skipped'] += 1
                results['videos'].append({'title': title, 'status': 'exists'})
                continue

            # Get category
            category, _ = VideoCategory.objects.get_or_create(
                name='Imported',
                defaults={'slug': 'imported'}
            )

            # Create video
            video = Video.objects.create(
                title=title,
                slug=slug,
                description=f'Импортировано из {video_file.name}',
                category=category,
                video_file=f'videos/{slug}{video_file.suffix}',
                duration=0,
                views=0,
                is_active=True
            )

            # Copy file
            media_path = Path('media/videos') / f'{slug}{video_file.suffix}'
            media_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(video_file, media_path)

            results['imported'] += 1
            results['videos'].append({'title': title, 'status': 'imported', 'id': video.id})

        except Exception as e:
            results['errors'] += 1
            results['videos'].append({'title': video_file.stem, 'status': 'error', 'error': str(e)})

    return Response(results)
