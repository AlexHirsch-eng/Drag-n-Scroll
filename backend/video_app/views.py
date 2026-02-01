"""
API Views for Video App (TikTok-style learning videos)
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q, Count, F, Case, When, IntegerField
from django.shortcuts import get_object_or_404
from django.db import models
from django.contrib.auth import get_user_model

from .models import (
    Video, VideoCategory, VideoView, VideoLike, VideoBookmark,
    VideoComment, VideoCommentLike, VideoShare, VideoReport,
    VideoHashtag, UserFollowing
)
from .serializers import (
    VideoListSerializer, VideoDetailSerializer, VideoCreateSerializer,
    VideoCommentSerializer, VideoCommentCreateSerializer,
    VideoLikeSerializer, VideoBookmarkSerializer,
    VideoViewSerializer, VideoShareSerializer, VideoReportSerializer,
    VideoHashtagSerializer, UserFollowingSerializer, UserFollowingCreateSerializer,
    VideoCategorySerializer
)


class VideoCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """View-only endpoint for video categories"""
    queryset = VideoCategory.objects.all()
    serializer_class = VideoCategorySerializer
    permission_classes = [IsAuthenticated]


class VideoViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing videos
    Provides list, create, retrieve, update, delete operations
    """
    queryset = Video.objects.filter(status='ready').select_related('creator', 'category').prefetch_related(
        'video_likes', 'bookmarks'
    )
    serializer_class = VideoDetailSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'status']

    def get_serializer_class(self):
        if self.action == 'list':
            return VideoListSerializer
        if self.action == 'create':
            return VideoCreateSerializer
        return VideoDetailSerializer

    def perform_create(self, serializer):
        # Update hashtags count
        tags = serializer.validated_data.get('tags', [])
        for tag in tags:
            hashtag, created = VideoHashtag.objects.get_or_create(tag=tag)
            if not created:
                hashtag.uses_count += 1
                hashtag.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Track view
        if request.user.is_authenticated:
            VideoView.objects.get_or_create(
                video=instance,
                user=request.user
            )
            # Increment view count
            Video.objects.filter(id=instance.id).update(views_count=F('views_count') + 1)
            instance.refresh_from_db()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """Like/unlike a video"""
        video = self.get_object()
        user = request.user

        try:
            # Try to get existing like
            like = VideoLike.objects.get(video=video, user=user)
            # Unlike: delete and decrement count
            like.delete()
            Video.objects.filter(id=video.id).update(likes_count=F('likes_count') - 1)

            return Response({
                'is_liked': False,
                'likes_count': video.likes_count - 1
            }, status=status.HTTP_200_OK)

        except VideoLike.DoesNotExist:
            # Like: create and increment count
            VideoLike.objects.create(video=video, user=user)
            Video.objects.filter(id=video.id).update(likes_count=F('likes_count') + 1)

            return Response({
                'is_liked': True,
                'likes_count': video.likes_count + 1
            }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def bookmark(self, request, pk=None):
        """Save/unsave a video"""
        video = self.get_object()
        user = request.user

        try:
            # Try to get existing bookmark
            bookmark = VideoBookmark.objects.get(video=video, user=user)
            # Unsave: delete
            bookmark.delete()

            return Response({
                'is_saved': False
            }, status=status.HTTP_200_OK)

        except VideoBookmark.DoesNotExist:
            # Save: create
            VideoBookmark.objects.create(video=video, user=user)

            return Response({
                'is_saved': True
            }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def share(self, request, pk=None):
        """Track video shares"""
        video = self.get_object()
        user = request.user

        data = request.data.copy()
        data['video'] = video.id
        if user.is_authenticated:
            data['user'] = user.id

        serializer = VideoShareSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Increment share count
        Video.objects.filter(id=video.id).update(shares_count=F('shares_count') + 1)

        return Response({
            'shares_count': video.shares_count + 1
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get', 'post'], permission_classes=[IsAuthenticated])
    def comments(self, request, pk=None):
        """Get or create comments for a video"""
        video = self.get_object()

        if request.method == 'GET':
            comments = VideoComment.objects.filter(
                video=video,
                parent=None,  # Only top-level comments
                is_deleted=False
            ).select_related('user').order_by('-created_at')

            serializer = VideoCommentSerializer(comments, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            # Create comment with video from URL
            data = request.data.copy()
            data['video'] = video.id

            serializer = VideoCommentCreateSerializer(
                data=data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Update comment count
            Video.objects.filter(id=video.id).update(comments_count=F('comments_count') + 1)

            # Return updated comments list
            comments = VideoComment.objects.filter(
                video=video,
                parent=None,
                is_deleted=False
            ).select_related('user').order_by('-created_at')

            new_serializer = VideoCommentSerializer(comments, many=True)
            return Response(new_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def feed(self, request):
        """Get personalized video feed"""
        # Algorithm: videos from followed users + trending videos + new videos
        user = request.user

        # Get followed users' videos
        followed_user_ids = UserFollowing.objects.filter(
            follower=user
        ).values_list('following_id', flat=True)

        # Combine sources with weights
        from django.db.models import Case, When

        queryset = Video.objects.filter(status='ready').annotate(
            weight=Count('views_count') + Count('likes_count') * 2
        ).order_by('-weight', '-created_at')

        # Prioritize followed users' videos
        if followed_user_ids:
            queryset = queryset.annotate(
                priority=Case(
                    *[
                        When(creator_id__in=followed_user_ids, then=3),
                        When(creator_id=user.id, then=2),
                    ],
                    default=1,
                    output_field=IntegerField()
                )
            ).order_by('-priority', '-weight', '-created_at')
        else:
            queryset = queryset.order_by('-weight', '-created_at')

        # Pagination
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))

        start = (page - 1) * page_size
        end = start + page_size

        videos = queryset[start:end]
        serializer = VideoListSerializer(videos, many=True, context={'request': request})

        return Response({
            'videos': serializer.data,
            'page': page,
            'has_more': end < queryset.count(),
            'total': queryset.count()
        })

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def trending(self, request):
        """Get trending videos"""
        from datetime import timedelta

        # Videos from last 7 days with high engagement
        since = timezone.now() - timedelta(days=7)
        queryset = Video.objects.filter(
            status='ready',
            created_at__gte=since
        ).annotate(
            engagement_score=Count('likes_count') + Count('comments_count') + Count('shares_count')
        ).order_by('-engagement_score', '-created_at')[:20]

        serializer = VideoListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def category(self, request):
        """Get videos by category"""
        category_id = request.query_params.get('category')
        if not category_id:
            return Response(
                {'error': 'Category ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            category = VideoCategory.objects.get(id=category_id)
        except VideoCategory.DoesNotExist:
            return Response(
                {'error': 'Category not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        queryset = Video.objects.filter(
            status='ready',
            category=category
        ).order_by('-created_at')[:50]

        serializer = VideoListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def hashtag(self, request):
        """Get videos by hashtag"""
        tag = request.query_params.get('tag')
        if not tag:
            return Response(
                {'error': 'Tag is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = Video.objects.filter(
            status='ready',
            tags__contains=[tag]
        ).order_by('-created_at')[:50]

        serializer = VideoListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_videos(self, request):
        """Get current user's videos"""
        queryset = Video.objects.filter(
            creator=request.user
        ).order_by('-created_at')

        serializer = VideoListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def saved(self, request):
        """Get videos saved by current user"""
        bookmarked = VideoBookmark.objects.filter(
            user=request.user
        ).select_related('video__creator', 'video__category').order_by('-created_at')

        videos = [bookmark.video for bookmark in bookmarked]
        serializer = VideoListSerializer(videos, many=True, context={'request': request})
        return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def video_comments_detail(request, video_id):
    """Get or create comments for a specific video"""
    video = get_object_or_404(Video, id=video_id)

    if request.method == 'GET':
        # Get all comments (excluding replies for now)
        comments = VideoComment.objects.filter(
            video=video,
            parent=None,
            is_deleted=False
        ).select_related('user').order_by('-created_at')

        # Add reply counts
        for comment in comments:
            comment.replies_count = VideoComment.objects.filter(
                parent=comment,
                is_deleted=False
            ).count()

        serializer = VideoCommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Create comment with video from URL
        from .serializers import VideoCommentCreateSerializer

        data = request.data.copy()
        data['video'] = video.id  # Use video_id from URL

        serializer = VideoCommentCreateSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Update comment count
        Video.objects.filter(id=video.id).update(comments_count=F('comments_count') + 1)

        # Return updated comments list
        comments = VideoComment.objects.filter(
            video=video,
            parent=None,
            is_deleted=False
        ).select_related('user').order_by('-created_at')

        new_serializer = VideoCommentSerializer(comments, many=True)
        return Response(new_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_comment(request, comment_id):
    """Like/unlike a comment"""
    comment = get_object_or_404(VideoComment, id=comment_id)
    user = request.user

    try:
        # Try to get existing like
        like = VideoCommentLike.objects.get(comment=comment, user=user)
        # Unlike
        like.delete()
        VideoComment.objects.filter(id=comment.id).update(likes_count=F('likes_count') - 1)

        return Response({
            'is_liked': False,
            'likes_count': comment.likes_count - 1
        })

    except VideoCommentLike.DoesNotExist:
        # Like
        VideoCommentLike.objects.create(comment=comment, user=user)
        VideoComment.objects.filter(id=comment.id).update(likes_count=F('likes_count') + 1)

        return Response({
            'is_liked': True,
            'likes_count': comment.likes_count + 1
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def translate_comment(request, comment_id):
    """
    Translate a comment using LibreTranslate API
    POST /api/videos/comments/<comment_id>/translate/
    Body: {"target_language": "ru"}  # or "en"
    """
    from django.utils import timezone
    from .translation_service import translation_service

    comment = get_object_or_404(VideoComment, id=comment_id)
    target_language = request.data.get('target_language', 'ru')

    # Validate target language
    if target_language not in ['ru', 'en']:
        return Response({
            'error': 'Invalid target language. Use "ru" or "en".'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Check if comment is Chinese (or auto-detect)
    if not translation_service.is_chinese(comment.text):
        return Response({
            'error': 'This comment does not appear to be in Chinese.',
            'text': comment.text
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Perform translation
        if target_language == 'ru':
            translated_text = translation_service.translate_to_ru(comment.text)
            comment.translation_ru = translated_text
        else:  # en
            translated_text = translation_service.translate_to_en(comment.text)
            comment.translation_en = translated_text

        # Update translation timestamp
        comment.translated_at = timezone.now()
        comment.save(update_fields=['translation_ru', 'translation_en', 'translated_at'])

        # Return updated comment with translation
        serializer = VideoCommentSerializer(comment, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': f'Translation failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_feed(request, user_id):
    """Get videos from a specific user (for profile viewing)"""
    user = get_object_or_404(get_user_model(), id=user_id)
    queryset = Video.objects.filter(
        creator=user,
        status='ready'
    ).order_by('-created_at')

    serializer = VideoListSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    """Follow/unfollow a user"""
    target_user = get_object_or_404(get_user_model(), id=user_id)
    current_user = request.user

    if target_user == current_user:
        return Response(
            {'error': 'You cannot follow yourself'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if already following
    existing = UserFollowing.objects.filter(
        follower=current_user,
        following=target_user
    )

    if existing.exists():
        # Unfollow
        existing.delete()
        return Response({'is_following': False})

    else:
        # Follow
        UserFollowing.objects.create(
            follower=current_user,
            following=target_user
        )
        return Response({'is_following': True}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report_video(request, video_id):
    """Report a video"""
    video = get_object_or_404(Video, id=video_id)

    # Check if already reported
    existing = VideoReport.objects.filter(
        video=video,
        reporter=request.user
    )

    if existing.exists():
        return Response(
            {'error': 'You have already reported this video'},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = VideoReportSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # Mark video as reported
    VideoReport.objects.create(
        video=video,
        reporter=request.user,
        **serializer.validated_data
    )

    # Update video status
    video.is_reported = True
    video.save()

    return Response(
        {'message': 'Video reported successfully. Thank you for helping keep our community safe.'},
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def import_videos_from_folder(request):
    """
    Admin endpoint to import all videos from Downloads/v folder
    POST /api/videos/admin/import-videos/
    """
    from pathlib import Path
    import shutil
    from django.core.files import File
    import os

    # Check if user is admin
    if not request.user.is_staff:
        return Response(
            {'error': 'Admin access required'},
            status=status.HTTP_403_FORBIDDEN
        )

    VIDEO_EXTENSIONS = ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv']
    DOWNLOADS_FOLDER = r'C:\Users\aibat\Downloads\v'

    folder = Path(DOWNLOADS_FOLDER)
    if not folder.exists():
        return Response({
            'error': f'Folder not found: {DOWNLOADS_FOLDER}'
        }, status=400)

    # Find all video files
    video_files_set = set()  # Use set to avoid duplicates
    for ext in VIDEO_EXTENSIONS:
        video_files_set.update(folder.glob(f'*{ext}'))
        video_files_set.update(folder.glob(f'*{ext.upper()}'))
    video_files = list(video_files_set)

    results = {
        'total': len(video_files),
        'imported': 0,
        'skipped': 0,
        'errors': 0,
        'videos': []
    }

    # Get or create category
    category, created = VideoCategory.objects.get_or_create(
        name='Imported',
        defaults={
            'icon': '📥',
            'description': 'Videos imported from Downloads folder',
            'order': 999
        }
    )

    for video_file in video_files:
        try:
            file_title = video_file.stem

            # Check if video with this filename already exists in video_file
            existing = Video.objects.filter(
                video_file__icontains=video_file.name
            ).first()
            if existing:
                results['skipped'] += 1
                results['videos'].append({'title': file_title, 'status': 'exists', 'id': existing.id})
                continue

            # Open the video file
            with open(video_file, 'rb') as f:
                # Create video with proper File object
                # Note: Video model uses 'description' as the title/display text
                video = Video.objects.create(
                    creator=request.user,
                    description=file_title,  # Use filename as description/title
                    category=category,
                    video_file=File(f, name=f'{video_file.name}'),
                    duration=0,
                    status='ready',
                    tags=['imported'],
                    music_title=f'Импортировано из {video_file.name}'
                )

            results['imported'] += 1
            results['videos'].append({'title': file_title, 'status': 'imported', 'id': video.id})

        except Exception as e:
            import traceback
            results['errors'] += 1
            results['videos'].append({
                'title': video_file.stem,
                'status': 'error',
                'error': str(e),
                'traceback': traceback.format_exc()
            })

    return Response(results)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def categories_list(request):
    """Get all video categories (non-paginated for frontend dropdown)"""
    categories = VideoCategory.objects.all()
    serializer = VideoCategorySerializer(categories, many=True)
    return Response(serializer.data)
