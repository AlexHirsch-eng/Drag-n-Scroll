"""
API views for Video sharing
Users can post videos, like, comment, and browse all videos
"""
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db import models as django_models
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

from .models import Video, VideoLike, VideoComment
from .serializers import (
    VideoSerializer, VideoCreateSerializer,
    VideoLikeSerializer, VideoCommentSerializer
)


class VideoViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Video model
    - list: Get all videos (public)
    - create: Post a new video (authenticated)
    - retrieve: Get single video details
    - update: Update video (owner only)
    - destroy: Delete video (owner only)
    """
    queryset = Video.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        """Use different serializers for list/create vs detail/update"""
        if self.action == 'create':
            return VideoCreateSerializer
        return VideoSerializer

    def get_queryset(self):
        """Optimize queryset with select_related"""
        queryset = Video.objects.select_related('user').all()

        # Filter by HSK level if provided
        hsk_level = self.request.query_params.get('hsk_level')
        if hsk_level:
            queryset = queryset.filter(hsk_level=hsk_level)

        # Filter by tags if provided
        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(tags__contains=tags)

        return queryset

    def perform_create(self, serializer):
        """Create video for logged in user"""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        """Like or unlike a video"""
        video = self.get_object()
        user = request.user

        # Check if already liked
        existing_like = VideoLike.objects.filter(video=video, user=user).first()

        if existing_like:
            # Unlike
            existing_like.delete()
            video.likes_count = max(0, video.likes_count - 1)
            video.save()
            return Response({
                'liked': False,
                'likes_count': video.likes_count
            })
        else:
            # Like
            VideoLike.objects.create(video=video, user=user)
            video.likes_count += 1
            video.save()
            return Response({
                'liked': True,
                'likes_count': video.likes_count
            })

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def view(self, request, pk=None):
        """Increment view count"""
        video = self.get_object()
        video.views_count += 1
        video.save()
        return Response({'views_count': video.views_count})

    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def comments(self, request, pk=None):
        """Get all comments for a video"""
        video = self.get_object()
        comments = video.comments.select_related('user').all()
        serializer = VideoCommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_comment(self, request, pk=None):
        """Add a comment to a video"""
        video = self.get_object()
        serializer = VideoCommentSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save(video=video)
            # Update comments count
            video.comments_count += 1
            video.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def upload(self, request):
        """
        Upload video action
        Uses Django ORM for simplicity and reliability
        Supports both URL and file upload
        """
        import json

        logger.info(f'ViewSet upload action called')
        logger.info(f'Request FILES: {request.FILES}')
        logger.info(f'Request DATA keys: {request.data.keys()}')

        try:
            # Parse tags
            tags_str = request.data.get('tags', '[]')
            try:
                tags = json.loads(tags_str) if isinstance(tags_str, str) else tags_str
            except:
                tags = []

            # Check if file upload or URL
            video_file = request.FILES.get('video_file') if 'video_file' in request.FILES else None
            video_url = request.data.get('video_url', '')

            logger.info(f'video_file: {video_file}, video_url: {video_url}')

            # Determine video source
            if video_file:
                # File upload - create video with file
                video = Video.objects.create(
                    user=request.user,
                    title=request.data.get('title', 'Uploaded Video').strip(),
                    description=request.data.get('description', ''),
                    video_file=video_file,
                    hsk_level=request.data.get('hsk_level', 1),
                    tags=tags,
                    views_count=0,
                    likes_count=0,
                    comments_count=0,
                    video_type='file'
                )
                # Use the video file URL
                final_url = video.video_file.url if video.video_file else ''
            elif video_url:
                # URL upload - create video with URL
                video = Video.objects.create(
                    user=request.user,
                    title=request.data.get('title', '').strip(),
                    description=request.data.get('description', ''),
                    video_url=video_url,
                    thumbnail_url=request.data.get('thumbnail_url', ''),
                    hsk_level=request.data.get('hsk_level', 1),
                    tags=tags,
                    views_count=0,
                    likes_count=0,
                    comments_count=0,
                    video_type='url'
                )
                final_url = video.video_url
            else:
                return Response(
                    {'error': 'Either video_url or video_file is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            logger.info(f"Created video with ID: {video.id}, type: {video.video_type}, url: {final_url}")

            response_data = {
                'id': video.id,
                'title': video.title,
                'description': video.description or '',
                'video_url': video.video_url or '',
                'url': final_url,  # Frontend expects 'url' field
                'video_file': final_url,  # Same as url for consistency
                'thumbnail_url': video.thumbnail_url or '',
                'thumbnail': video.thumbnail_url or '',  # Frontend expects 'thumbnail' field
                'duration': 0,  # Default duration
                'category': {  # Default category
                    'id': 1,
                    'name': 'Общее',
                    'description': 'Обучающие видео'
                },
                'tags': video.tags or [],
                'music_title': 'Оригинальный звук',
                'shares_count': 0,
                'is_saved': False,
                'is_liked': False,
                'views_count': video.views_count,
                'likes_count': video.likes_count,
                'comments_count': video.comments_count,
                'created_at': video.created_at.isoformat() if video.created_at else None,
                'creator': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'email': getattr(request.user, 'email', ''),
                    'profile': {},
                    'followers_count': 0,
                    'following_count': 0,
                    'is_following': False
                }
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f'Error in ViewSet upload: {e}', exc_info=True)
            return Response(
                {'error': f'Error uploading video: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def videos_list(request):
    """
    Get all videos with filtering options
    Query params:
    - hsk_level: filter by HSK level (1-6)
    - tags: filter by tags (comma-separated)
    - search: search in title and description
    - sort: sort by (recent, popular, views)
    """
    queryset = Video.objects.select_related('user').all()

    # Filter by HSK level
    hsk_level = request.query_params.get('hsk_level')
    if hsk_level:
        try:
            queryset = queryset.filter(hsk_level=int(hsk_level))
        except ValueError:
            pass

    # Filter by tags
    tags = request.query_params.get('tags')
    if tags:
        tag_list = tags.split(',')
        queryset = queryset.filter(tags__contains=tag_list)

    # Search
    search = request.query_params.get('search')
    if search:
        queryset = queryset.filter(
            django_models.Q(title__icontains=search) |
            django_models.Q(description__icontains=search)
        )

    # Sorting
    sort = request.query_params.get('sort', 'recent')
    if sort == 'popular':
        queryset = queryset.order_by('-likes_count', '-created_at')
    elif sort == 'views':
        queryset = queryset.order_by('-views_count', '-created_at')
    else:  # recent
        queryset = queryset.order_by('-created_at')

    # Pagination
    page_size = int(request.query_params.get('page_size', 20))
    page = int(request.query_params.get('page', 1))

    start = (page - 1) * page_size
    end = start + page_size

    videos = queryset[start:end]
    total = queryset.count()

    serializer = VideoSerializer(videos, many=True, context={'request': request})

    return Response({
        'videos': serializer.data,
        'total': total,
        'page': page,
        'page_size': page_size,
        'has_more': end < total
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def user_feed(request, user_id):
    """
    Get all videos posted by a specific user
    Used in profile page to show user's posted videos

    Uses raw SQL to avoid Django model field validation issues when
    database schema is out of sync.
    """
    from django.contrib.auth import get_user_model
    from django.db import connection

    User = get_user_model()

    logger.info(f"user_feed called for user_id={user_id}")

    # Get user or return 404
    try:
        user = User.objects.get(id=user_id)
        logger.info(f"Found user: {user.username}")
    except User.DoesNotExist:
        logger.warning(f"User not found: {user_id}")
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {e}", exc_info=True)
        return Response({'error': f'Error fetching user: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Get all videos by this user using RAW SQL to avoid model field issues
    try:
        with connection.cursor() as cursor:
            # First, check what columns exist in video_video table
            cursor.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'video_video'
                ORDER BY column_name;
            """)
            columns = [row[0] for row in cursor.fetchall()]
            logger.info(f"Available columns in video_video: {columns}")

            # Build SELECT query based on available columns
            safe_columns = ['id', 'title', 'description', 'video_url', 'video_file', 'thumbnail_url',
                          'views_count', 'likes_count', 'comments_count', 'created_at', 'user_id']
            select_columns = [col for col in safe_columns if col in columns]

            if not select_columns:
                logger.error("No safe columns available in video_video table!")
                return Response([])

            query = f"""
                SELECT {', '.join(select_columns)}
                FROM video_video
                WHERE user_id = %s
                ORDER BY created_at DESC;
            """
            cursor.execute(query, [user_id])
            rows = cursor.fetchall()
            logger.info(f"Found {len(rows)} videos for user {user_id}")

            # Build response data
            data = []
            for row in rows:
                try:
                    row_dict = dict(zip(select_columns, row))
                    # Use video_file if available, otherwise use video_url
                    video_url_val = row_dict.get('video_url', '')
                    video_file_val = row_dict.get('video_file', '') if 'video_file' in row_dict else ''
                    final_video_url = video_file_val if video_file_val else video_url_val

                    video_data = {
                        'id': row_dict.get('id'),
                        'title': row_dict.get('title', ''),
                        'description': row_dict.get('description', ''),
                        'video_url': video_url_val,
                        'url': final_video_url,  # Frontend expects 'url' field
                        'video_file': final_video_url,  # Use actual video source
                        'thumbnail_url': row_dict.get('thumbnail_url', ''),
                        'views_count': row_dict.get('views_count', 0),
                        'likes_count': row_dict.get('likes_count', 0),
                        'comments_count': row_dict.get('comments_count', 0),
                        'created_at': row_dict.get('created_at').isoformat() if row_dict.get('created_at') else None,
                        'creator': {
                            'id': user.id,
                            'username': user.username,
                            'email': getattr(user, 'email', '')
                        }
                    }
                    data.append(video_data)
                except Exception as e:
                    logger.error(f"Error processing video row: {e}", exc_info=True)
                    continue

            logger.info(f"Successfully serialized {len(data)} videos")
            return Response(data)

    except Exception as e:
        logger.error(f"Critical error in user_feed: {e}", exc_info=True)
        # Return empty array instead of crashing - allows profile to load
        return Response([])


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def upload_video(request):
    """
    Upload a video (supports URL or file upload)
    Uses Django ORM which is simpler and more reliable than raw SQL
    """
    from .models import Video
    import json

    logger.info(f'Standalone upload_video called')
    logger.info(f'Request FILES: {request.FILES}')
    logger.info(f'Request DATA keys: {request.data.keys()}')

    try:
        # Parse tags
        tags_str = request.data.get('tags', '[]')
        try:
            tags = json.loads(tags_str) if isinstance(tags_str, str) else tags_str
        except:
            tags = []

        # Check if file upload or URL
        video_file = request.FILES.get('video_file') if 'video_file' in request.FILES else None
        video_url = request.data.get('video_url', '')

        logger.info(f'video_file: {video_file}, video_url: {video_url}')

        # Determine video source
        if video_file:
            # File upload - create video with file
            video = Video.objects.create(
                user=request.user,
                title=request.data.get('title', 'Uploaded Video').strip(),
                description=request.data.get('description', ''),
                video_file=video_file,
                hsk_level=request.data.get('hsk_level', 1),
                tags=tags,
                views_count=0,
                likes_count=0,
                comments_count=0,
                video_type='file'
            )
            # Use the video file URL
            final_url = video.video_file.url if video.video_file else ''
        elif video_url:
            # URL upload - create video with URL
            video = Video.objects.create(
                user=request.user,
                title=request.data.get('title', '').strip(),
                description=request.data.get('description', ''),
                video_url=video_url,
                thumbnail_url=request.data.get('thumbnail_url', ''),
                hsk_level=request.data.get('hsk_level', 1),
                tags=tags,
                views_count=0,
                likes_count=0,
                comments_count=0,
                video_type='url'
            )
            final_url = video.video_url
        else:
            return Response(
                {'error': 'Either video_url or video_file is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        logger.info(f"Created video with ID: {video.id}, type: {video.video_type}, url: {final_url}")

        # Return response - include all fields frontend expects
        response_data = {
            'id': video.id,
            'title': video.title,
            'description': video.description or '',
            'video_url': video.video_url or '',
            'url': final_url,  # Frontend expects 'url' field
            'video_file': final_url,  # Same as url for consistency
            'thumbnail_url': video.thumbnail_url or '',
            'thumbnail': video.thumbnail_url or '',  # Frontend expects 'thumbnail' field
            'duration': 0,  # Default duration
            'category': {  # Default category
                'id': 1,
                'name': 'Общее',
                'description': 'Обучающие видео'
            },
            'tags': video.tags or [],
            'music_title': 'Оригинальный звук',
            'shares_count': 0,
            'is_saved': False,
            'is_liked': False,
            'views_count': video.views_count,
            'likes_count': video.likes_count,
            'comments_count': video.comments_count,
            'created_at': video.created_at.isoformat() if video.created_at else None,
            'creator': {
                'id': request.user.id,
                'username': request.user.username,
                'email': getattr(request.user, 'email', ''),
                'profile': {},
                'followers_count': 0,
                'following_count': 0,
                'is_following': False
            }
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error(f'Error in standalone upload_video: {e}', exc_info=True)
        return Response(
            {'error': f'Error uploading video: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def video_feed(request):
    """
    Get video feed with pagination
    Matches frontend's getFeed API call
    """
    from django.db import connection

    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 20))

    try:
        with connection.cursor() as cursor:
            # Get total count
            cursor.execute("SELECT COUNT(*) FROM video_video;")
            total = cursor.fetchone()[0]

            # Get paginated videos with user info
            offset = (page - 1) * page_size
            cursor.execute("""
                SELECT v.id, v.title, v.description, v.video_url, v.video_file, v.thumbnail_url,
                       v.views_count, v.likes_count, v.comments_count, v.created_at, v.user_id,
                       u.username, u.email
                FROM video_video v
                LEFT JOIN core_user u ON v.user_id = u.id
                ORDER BY v.created_at DESC
                LIMIT %s OFFSET %s;
            """, [page_size, offset])
            rows = cursor.fetchall()

            # Build response - include all fields frontend expects
            videos = []
            for row in rows:
                # Determine the correct video URL to use
                # row[3] = video_url, row[4] = video_file
                video_url_val = row[3] or ''
                video_file_val = row[4] or ''
                # Use video_file if available (uploaded file), otherwise use video_url
                final_video_url = video_file_val if video_file_val else video_url_val

                videos.append({
                    'id': row[0],
                    'title': row[1],
                    'description': row[2] or '',
                    'video_url': video_url_val,
                    'url': final_video_url,  # Frontend expects 'url' field
                    'video_file': final_video_url,  # Use the actual video source
                    'thumbnail_url': row[5] or '',
                    'thumbnail': row[5] or '',  # Frontend expects 'thumbnail' field
                    'duration': 0,  # Default duration
                    'category': {  # Default category
                        'id': 1,
                        'name': 'Общее',
                        'description': 'Обучающие видео'
                    },
                    'tags': [],  # Would need to parse JSON if stored
                    'music_title': 'Оригинальный звук',
                    'shares_count': 0,
                    'is_saved': False,
                    'is_liked': False,
                    'views_count': row[6],
                    'likes_count': row[7],
                    'comments_count': row[8],
                    'created_at': row[9].isoformat() if row[9] else None,
                    'creator': {
                        'id': row[10],
                        'username': row[11] or '',
                        'email': row[12] or '',
                        'profile': {},
                        'followers_count': 0,
                        'following_count': 0,
                        'is_following': False
                    }
                })

        return Response({
            'videos': videos,
            'page': page,
            'page_size': page_size,
            'total': total,
            'has_more': offset + len(rows) < total
        })

    except Exception as e:
        logger.error(f'Error in video_feed: {e}', exc_info=True)
        return Response({
            'videos': [],
            'page': page,
            'page_size': page_size,
            'total': 0,
            'has_more': False
        })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def categories_list(request):
    """
    Get video categories
    Returns a default category for now
    """
    categories = [
        {
            'id': 1,
            'name': 'Общее',
            'description': 'Обучающие видео'
        },
        {
            'id': 2,
            'name': 'Грамматика',
            'description': 'Уроки по грамматике'
        },
        {
            'id': 3,
            'name': 'Лексика',
            'description': 'Уроки по лексике'
        },
        {
            'id': 4,
            'name': 'Аудирование',
            'description': 'Практика аудирования'
        },
        {
            'id': 5,
            'name': 'Разговорный',
            'description': 'Разговорная практика'
        },
        {
            'id': 6,
            'name': 'HSK 1-2',
            'description': 'Уровень HSK 1-2'
        },
        {
            'id': 7,
            'name': 'HSK 3-4',
            'description': 'Уровень HSK 3-4'
        },
        {
            'id': 8,
            'name': 'HSK 5-6',
            'description': 'Уровень HSK 5-6'
        }
    ]

    return Response(categories)
