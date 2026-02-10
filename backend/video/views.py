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
    """
    from django.contrib.auth import get_user_model

    User = get_user_model()

    # Get user or return 404
    user = get_object_or_404(User, id=user_id)

    # Get all videos by this user
    videos = Video.objects.filter(user=user).select_related('user').order_by('-created_at')

    serializer = VideoSerializer(videos, many=True, context={'request': request})

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def upload_video(request):
    """
    Upload a video file (supports multipart/form-data)
    Use this for uploading video files from device
    CSRF exempt because multipart/form-data doesn't work well with CSRF headers
    """
    # Debug logging
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f'Upload video request data keys: {request.data.keys()}')
    logger.info(f'Upload video request FILES keys: {request.FILES.keys()}')

    serializer = VideoCreateSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        video = serializer.save(user=request.user)
        # Return full video details
        response_serializer = VideoSerializer(video, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    logger.error(f'Upload video validation errors: {serializer.errors}')
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
