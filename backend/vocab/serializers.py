"""
Serializers for vocab app
"""
from rest_framework import serializers
from .models import Word, GrammarRule, GrammarExample, WordProgress, ReviewHistory


class GrammarExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrammarExample
        fields = [
            'id', 'sentence_hanzi', 'sentence_pinyin',
            'translation_ru', 'translation_kz', 'audio_url', 'order'
        ]


class GrammarRuleSerializer(serializers.ModelSerializer):
    examples = GrammarExampleSerializer(many=True, read_only=True)

    class Meta:
        model = GrammarRule
        fields = [
            'id', 'title', 'pattern', 'explanation_ru', 'explanation_kz',
            'hsk_level', 'examples', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = [
            'id', 'hanzi', 'pinyin', 'translation_ru', 'translation_kz',
            'audio_url', 'hsk_level', 'frequency_rank', 'part_of_speech',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class WordProgressSerializer(serializers.ModelSerializer):
    word = WordSerializer(read_only=True)
    accuracy = serializers.ReadOnlyField()

    class Meta:
        model = WordProgress
        fields = [
            'id', 'word', 'srs_level', 'ease_factor', 'interval_days',
            'next_review_date', 'total_reviews', 'correct_reviews',
            'accuracy', 'last_reviewed_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class WordDetailSerializer(serializers.ModelSerializer):
    """Detailed word serializer with user progress"""
    user_progress = serializers.SerializerMethodField()
    related_words = serializers.SerializerMethodField()

    class Meta:
        model = Word
        fields = [
            'id', 'hanzi', 'pinyin', 'translation_ru', 'translation_kz',
            'audio_url', 'hsk_level', 'frequency_rank', 'part_of_speech',
            'user_progress', 'related_words', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_user_progress(self, obj):
        """Get user's progress for this word"""
        user = self.context['request'].user
        try:
            progress = obj.progress.get(user=user)
            return WordProgressSerializer(progress).data
        except WordProgress.DoesNotExist:
            return None

    def get_related_words(self, obj):
        """Get related words (same HSK level, same part of speech)"""
        related = Word.objects.filter(
            hsk_level=obj.hsk_level,
            part_of_speech=obj.part_of_speech
        ).exclude(id=obj.id)[:5]
        return WordSerializer(related, many=True).data


class MyWordsSerializer(serializers.ModelSerializer):
    """Serializer for user's words with progress"""
    word = WordSerializer(read_only=True)
    progress = serializers.SerializerMethodField()

    class Meta:
        model = WordProgress
        fields = ['word', 'progress']

    def get_progress(self, obj):
        return {
            'srs_level': obj.srs_level,
            'interval_days': obj.interval_days,
            'next_review_date': obj.next_review_date,
            'total_reviews': obj.total_reviews,
            'correct_reviews': obj.correct_reviews,
            'accuracy': obj.accuracy
        }


class ReviewHistorySerializer(serializers.ModelSerializer):
    word = WordSerializer(read_only=True)

    class Meta:
        model = ReviewHistory
        fields = [
            'id', 'word', 'quality', 'old_srs_level', 'new_srs_level',
            'old_interval', 'new_interval', 'old_ease_factor',
            'new_ease_factor', 'review_time_seconds', 'reviewed_at'
        ]
        read_only_fields = ['created_at']
