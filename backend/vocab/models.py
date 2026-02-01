"""
Vocabulary models for Word, GrammarRule, GrammarExample, WordProgress
"""
from django.db import models
from django.utils import timezone
from django.conf import settings


class Word(models.Model):
    """
    Chinese word/character with translations
    """
    PART_OF_SPEECH_CHOICES = [
        ('noun', 'Noun'),
        ('verb', 'Verb'),
        ('adjective', 'Adjective'),
        ('adverb', 'Adverb'),
        ('pronoun', 'Pronoun'),
        ('preposition', 'Preposition'),
        ('conjunction', 'Conjunction'),
        ('particle', 'Particle'),
        ('measure', 'Measure Word'),
        ('other', 'Other'),
    ]

    hanzi = models.CharField(max_length=50)  # Chinese characters
    pinyin = models.CharField(max_length=100)  # Pinyin romanization
    translation_ru = models.CharField(max_length=255)  # Russian translation
    translation_kz = models.CharField(max_length=255)  # Kazakh translation
    audio_url = models.URLField(blank=True)  # Link to audio file
    hsk_level = models.IntegerField(default=1)  # HSK 1-6
    frequency_rank = models.IntegerField(null=True, blank=True)  # Frequency ranking
    part_of_speech = models.CharField(
        max_length=20,
        choices=PART_OF_SPEECH_CHOICES,
        default='other'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Word'
        verbose_name_plural = 'Words'
        ordering = ['hsk_level', 'frequency_rank', 'hanzi']
        unique_together = [['hanzi', 'pinyin']]

    def __str__(self):
        return f"{self.hanzi} ({self.pinyin}) - {self.translation_ru}"


class GrammarRule(models.Model):
    """
    Grammar rule with explanations and examples
    """
    title = models.CharField(max_length=255)
    pattern = models.CharField(max_length=255, blank=True)  # e.g., "Subject + 把 + Object + Verb"
    explanation_ru = models.TextField()
    explanation_kz = models.TextField()
    hsk_level = models.IntegerField(default=1)  # HSK 1-6
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Grammar Rule'
        verbose_name_plural = 'Grammar Rules'
        ordering = ['hsk_level', 'title']

    def __str__(self):
        return f"{self.title} (HSK {self.hsk_level})"


class GrammarExample(models.Model):
    """
    Example sentences for grammar rules
    """
    grammar_rule = models.ForeignKey(
        GrammarRule,
        on_delete=models.CASCADE,
        related_name='examples'
    )
    sentence_hanzi = models.TextField()
    sentence_pinyin = models.TextField()
    translation_ru = models.TextField()
    translation_kz = models.TextField()
    audio_url = models.URLField(blank=True)
    word_examples = models.ManyToManyField(
        Word,
        blank=True,
        related_name='grammar_examples'
    )
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Grammar Example'
        verbose_name_plural = 'Grammar Examples'
        ordering = ['grammar_rule', 'order']

    def __str__(self):
        return f"{self.sentence_hanzi} - {self.translation_ru}"


class WordProgress(models.Model):
    """
    Track user's progress with individual words (SRS data)
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='word_progress'
    )
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name='progress'
    )

    # SRS fields (SuperMemo SM-2 algorithm)
    srs_level = models.IntegerField(default=0)  # 0-8 (new → mastered)
    ease_factor = models.FloatField(default=2.5)  # EF (1.3 - 2.5+)
    interval_days = models.IntegerField(default=0)
    next_review_date = models.DateTimeField(null=True, blank=True)

    # Statistics
    total_reviews = models.IntegerField(default=0)
    correct_reviews = models.IntegerField(default=0)
    last_reviewed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Word Progress'
        verbose_name_plural = 'Word Progress'
        unique_together = [['user', 'word']]
        ordering = ['user', 'next_review_date']

    def __str__(self):
        return f"{self.user.username} - {self.word.hanzi} (Level {self.srs_level})"

    @property
    def accuracy(self):
        """Calculate accuracy rate"""
        if self.total_reviews == 0:
            return 0.0
        return round(self.correct_reviews / self.total_reviews, 2)


class ReviewHistory(models.Model):
    """
    Track SRS review history for analytics
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='review_history'
    )
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name='review_history'
    )

    # SM-2 quality rating (0-5)
    quality = models.IntegerField()

    # SRS state before and after review
    old_srs_level = models.IntegerField()
    new_srs_level = models.IntegerField()
    old_interval = models.IntegerField()
    new_interval = models.IntegerField()
    old_ease_factor = models.FloatField()
    new_ease_factor = models.FloatField()

    # Timing
    review_time_seconds = models.IntegerField()
    reviewed_at = models.DateTimeField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Review History'
        verbose_name_plural = 'Review History'
        ordering = ['-reviewed_at']

    def __str__(self):
        return f"{self.user.username} - {self.word.hanzi} - Q{self.quality}"
