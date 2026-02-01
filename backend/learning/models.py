"""
New Learning Session Models - Session A/B Structure with 5 Steps
Replaces the existing lesson system
"""
from django.db import models
from django.utils import timezone
from django.conf import settings


class Dialogue(models.Model):
    """
    Short dialogue for Step 4 listening comprehension
    """
    course_day = models.ForeignKey(
        'course.CourseDay',
        on_delete=models.CASCADE,
        related_name='dialogues'
    )
    session_type = models.CharField(
        max_length=1,
        choices=[('A', 'Session A'), ('B', 'Session B')]
    )

    # Dialogue content (2-3 lines)
    lines = models.JSONField(default=list)  # [{speaker, hanzi, pinyin, translation_ru, translation_kz, audio_url}]

    # Question and options
    question_hanzi = models.TextField()
    question_pinyin = models.TextField()
    question_translation_ru = models.TextField()
    question_translation_kz = models.TextField()
    audio_url = models.URLField(blank=True)

    # Three reply options (one correct)
    options = models.JSONField(default=list)  # [{hanzi, pinyin, translation_ru, translation_kz, is_correct}]
    explanation_ru = models.TextField(blank=True)
    explanation_kz = models.TextField(blank=True)

    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Dialogue'
        verbose_name_plural = 'Dialogues'
        ordering = ['course_day', 'session_type', 'order']
        unique_together = [['course_day', 'session_type', 'order']]

    def __str__(self):
        return f"Day {self.course_day.day_number} - {self.session_type} - Dialogue {self.order}"


class WordArrangementExercise(models.Model):
    """
    Word arrangement exercise for Step 5 active practice
    """
    course_day = models.ForeignKey(
        'course.CourseDay',
        on_delete=models.CASCADE,
        related_name='arrangement_exercises'
    )
    session_type = models.CharField(
        max_length=1,
        choices=[('A', 'Session A'), ('B', 'Session B')]
    )

    # Target sentence
    target_hanzi = models.TextField()
    target_pinyin = models.TextField()
    target_translation_ru = models.TextField()
    target_translation_kz = models.TextField()
    audio_url = models.URLField(blank=True)

    # Scrambled words for user to arrange
    scrambled_words = models.JSONField(default=list)  # [{id, hanzi, pinyin}]

    # Hints (optional)
    hint_ru = models.TextField(blank=True)
    hint_kz = models.TextField(blank=True)

    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Word Arrangement Exercise'
        verbose_name_plural = 'Word Arrangement Exercises'
        ordering = ['course_day', 'session_type', 'order']
        unique_together = [['course_day', 'session_type', 'order']]

    def __str__(self):
        return f"Day {self.course_day.day_number} - {self.session_type} - Arrangement {self.order}"


class GrammarTask(models.Model):
    """
    Grammar task for Step 3 sentence building
    """
    course_day = models.ForeignKey(
        'course.CourseDay',
        on_delete=models.CASCADE,
        related_name='grammar_tasks'
    )
    session_type = models.CharField(
        max_length=1,
        choices=[('A', 'Session A'), ('B', 'Session B')]
    )

    grammar_rule = models.ForeignKey(
        'vocab.GrammarRule',
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    # Task description
    task_prompt_ru = models.TextField()
    task_prompt_kz = models.TextField()

    # Required sentence components (user builds from these)
    components = models.JSONField(default=list)  # [{id, hanzi, pinyin, translation_ru, translation_kz, type}]

    # Correct answer
    correct_hanzi = models.TextField()
    correct_pinyin = models.TextField()
    correct_translation_ru = models.TextField()
    correct_translation_kz = models.TextField()

    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Grammar Task'
        verbose_name_plural = 'Grammar Tasks'
        ordering = ['course_day', 'session_type', 'order']
        unique_together = [['course_day', 'session_type', 'order']]

    def __str__(self):
        return f"Day {self.course_day.day_number} - {self.session_type} - Grammar Task {self.order}"


class LearningSession(models.Model):
    """
    Track Session A or Session B progress
    Replaces SessionProgress model
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='learning_sessions'
    )
    course_day = models.ForeignKey(
        'course.CourseDay',
        on_delete=models.CASCADE,
        related_name='learning_sessions'
    )

    SESSION_TYPES = [
        ('A', 'Session A'),
        ('B', 'Session B'),
    ]
    session_type = models.CharField(max_length=1, choices=SESSION_TYPES)

    STEPS = [
        (1, 'Step 1: SRS Review'),
        (2, 'Step 2: New Words'),
        (3, 'Step 3: Grammar'),
        (4, 'Step 4: Dialogue'),
        (5, 'Step 5: Word Arrangement'),
    ]

    # Current step (1-5), 6 means completed
    current_step = models.IntegerField(default=1)
    is_completed = models.BooleanField(default=False)

    # Step completion times (for tracking time spent on each step)
    step_1_started_at = models.DateTimeField(null=True, blank=True)
    step_1_completed_at = models.DateTimeField(null=True, blank=True)
    step_2_started_at = models.DateTimeField(null=True, blank=True)
    step_2_completed_at = models.DateTimeField(null=True, blank=True)
    step_3_started_at = models.DateTimeField(null=True, blank=True)
    step_3_completed_at = models.DateTimeField(null=True, blank=True)
    step_4_started_at = models.DateTimeField(null=True, blank=True)
    step_4_completed_at = models.DateTimeField(null=True, blank=True)
    step_5_started_at = models.DateTimeField(null=True, blank=True)
    step_5_completed_at = models.DateTimeField(null=True, blank=True)

    # Session timing
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Progress tracking
    words_learned = models.IntegerField(default=0)  # New words introduced in Step 2
    problematic_words = models.JSONField(default=list)  # IDs of words marked as problematic
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)

    # XP earned
    xp_earned = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Learning Session'
        verbose_name_plural = 'Learning Sessions'
        ordering = ['-started_at']
        unique_together = [['user', 'course_day', 'session_type']]

    def __str__(self):
        return f"{self.user.username} - Day {self.course_day.day_number} - Session {self.session_type}"

    @property
    def accuracy(self):
        """Calculate session accuracy"""
        if self.total_questions == 0:
            return 0.0
        return round(self.correct_answers / self.total_questions, 2)

    @property
    def accuracy_percentage(self):
        """Accuracy as percentage string"""
        return f"{int(self.accuracy * 100)}%"

    @property
    def total_time_minutes(self):
        """Calculate total time spent"""
        if self.completed_at:
            delta = self.completed_at - self.started_at
        else:
            delta = timezone.now() - self.started_at
        return round(delta.total_seconds() / 60, 1)

    def get_step_time(self, step_number):
        """Get time spent on a specific step in seconds"""
        started = getattr(self, f'step_{step_number}_started_at')
        completed = getattr(self, f'step_{step_number}_completed_at')

        if started and completed:
            return int((completed - started).total_seconds())
        return 0


class NewWordLearningProgress(models.Model):
    """
    Track progress for individual new words in Step 2
    """
    session = models.ForeignKey(
        LearningSession,
        on_delete=models.CASCADE,
        related_name='new_word_progress'
    )
    word = models.ForeignKey(
        'vocab.Word',
        on_delete=models.CASCADE,
        related_name='learning_progress'
    )

    # Mini-test result
    is_correct = models.BooleanField(null=True)  # null if not yet tested
    attempts = models.IntegerField(default=0)
    time_spent_seconds = models.IntegerField(default=0)

    # Pronunciation practice
    pronunciation_attempts = models.IntegerField(default=0)
    pronunciation_ok_count = models.IntegerField(default=0)

    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'New Word Learning Progress'
        verbose_name_plural = 'New Word Learning Progress'
        ordering = ['session', 'created_at']
        unique_together = [['session', 'word']]

    def __str__(self):
        return f"{self.session} - {self.word.hanzi}"


class StepProgress(models.Model):
    """
    Detailed progress tracking for each step
    """
    session = models.ForeignKey(
        LearningSession,
        on_delete=models.CASCADE,
        related_name='step_progress'
    )

    STEP_TYPES = [
        ('SRS_REVIEW', 'Step 1: SRS Review'),
        ('NEW_WORDS', 'Step 2: New Words'),
        ('GRAMMAR', 'Step 3: Grammar'),
        ('DIALOGUE', 'Step 4: Dialogue'),
        ('WORD_ARRANGEMENT', 'Step 5: Word Arrangement'),
    ]

    step_type = models.CharField(max_length=30, choices=STEP_TYPES)

    # Step-specific data
    data = models.JSONField(default=dict)  # Flexible storage for step-specific answers

    # Timing
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_spent_seconds = models.IntegerField(default=0)

    # Results
    is_correct = models.BooleanField(null=True)  # For single-answer steps (3, 4, 5)
    attempts = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Step Progress'
        verbose_name_plural = 'Step Progress'
        ordering = ['session', 'started_at']

    def __str__(self):
        return f"{self.session} - {self.get_step_type_display()}"


class SRSReviewCard(models.Model):
    """
    Individual SRS flashcard for Step 1
    Links words to sessions for review
    """
    session = models.ForeignKey(
        LearningSession,
        on_delete=models.CASCADE,
        related_name='srs_cards'
    )
    word = models.ForeignKey(
        'vocab.Word',
        on_delete=models.CASCADE,
        related_name='srs_cards'
    )

    # Multiple choice options (4 options)
    options = models.JSONField(default=list)  # [{word_id, translation_ru, translation_kz}]

    # User's answer
    selected_option_id = models.IntegerField(null=True, blank=True)
    is_correct = models.BooleanField(null=True)

    # Mark as problematic
    is_problematic = models.BooleanField(default=False)

    # Timing
    time_spent_seconds = models.IntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'SRS Review Card'
        verbose_name_plural = 'SRS Review Cards'
        ordering = ['session', 'created_at']

    def __str__(self):
        return f"{self.session} - {self.word.hanzi} - {'Problematic' if self.is_problematic else 'OK'}"
