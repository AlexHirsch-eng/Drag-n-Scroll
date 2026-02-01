"""
Views for vocab app
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Word, GrammarRule, WordProgress, ReviewHistory
from .serializers import (
    WordSerializer,
    WordDetailSerializer,
    MyWordsSerializer,
    GrammarRuleSerializer,
    ReviewHistorySerializer
)
import uuid


class WordViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing words
    """
    queryset = Word.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WordSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['hsk_level', 'part_of_speech']
    search_fields = ['hanzi', 'pinyin', 'translation_ru', 'translation_kz']
    ordering_fields = ['hanzi', 'pinyin', 'frequency_rank', 'hsk_level']
    ordering = ['hsk_level', 'frequency_rank']

    def retrieve(self, request, *args, **kwargs):
        """Get word details with user progress"""
        instance = self.get_object()
        serializer = WordDetailSerializer(instance, context={'request': request})
        return Response(serializer.data)


class MyWordsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for user's words with progress
    """
    serializer_class = MyWordsSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['word__hsk_level', 'srs_level']
    ordering_fields = ['next_review_date', 'srs_level', 'word__hanzi']
    ordering = ['next_review_date']

    def get_queryset(self):
        return WordProgress.objects.filter(user=self.request.user).select_related('word')

    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Filter words by learning status"""
        status_filter = request.query_params.get('status')
        queryset = self.get_queryset()

        if status_filter == 'new':
            queryset = queryset.filter(srs_level=0)
        elif status_filter == 'learning':
            queryset = queryset.filter(srs_level__in=[1, 2, 3, 4])
        elif status_filter == 'mastered':
            queryset = queryset.filter(srs_level__gte=5)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class GrammarRuleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing grammar rules
    """
    queryset = GrammarRule.objects.all()
    serializer_class = GrammarRuleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['hsk_level']
    search_fields = ['title', 'pattern', 'explanation_ru']
    ordering = ['hsk_level', 'title']


class ReviewHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing review history
    """
    serializer_class = ReviewHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ReviewHistory.objects.filter(user=self.request.user).select_related('word')
