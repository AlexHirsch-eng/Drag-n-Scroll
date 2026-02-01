"""
Course models for Course, CourseDay, Lesson, LessonStep
"""
from django.db import models


class Course(models.Model):
    """
    Main course framework (e.g., "HSK 1 Complete Course")
    """
    title = models.CharField(max_length=255)
    title_zh = models.CharField(max_length=255, blank=True)  # Chinese title
    description = models.TextField(blank=True)
    hsk_level = models.IntegerField()  # 1-6
    total_days = models.IntegerField(default=30)  # Total course days
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['hsk_level', 'order']

    def __str__(self):
        return f"{self.title} (HSK {self.hsk_level})"


class CourseDay(models.Model):
    """
    A single day in the course (e.g., "Day 8: Basic Verbs")
    Contains two sessions: Session A and Session B
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='days')
    day_number = models.IntegerField()
    title = models.CharField(max_length=255)
    title_zh = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    estimated_minutes = models.IntegerField(default=15)  # Total time for the day
    order = models.IntegerField(default=0)

    # New words for this day (assigned to Session A or B)
    new_words = models.ManyToManyField(
        'vocab.Word',
        blank=True,
        related_name='course_days'
    )

    # Grammar rules for this day
    grammar_rules = models.ManyToManyField(
        'vocab.GrammarRule',
        blank=True,
        related_name='course_days'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Course Day'
        verbose_name_plural = 'Course Days'
        ordering = ['course', 'day_number']
        unique_together = [['course', 'day_number']]

    def __str__(self):
        return f"Day {self.day_number}: {self.title}"


class Lesson(models.Model):
    """
    A lesson within a course day
    """
    LESSON_TYPES = [
        ('VOCABULARY', 'Vocabulary'),
        ('GRAMMAR', 'Grammar'),
        ('MIXED', 'Mixed'),
    ]

    course_day = models.ForeignKey(CourseDay, on_delete=models.CASCADE, related_name='lessons')
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPES, default='MIXED')
    hsk_level = models.IntegerField(default=1)  # 1-6
    title = models.CharField(max_length=255)
    title_zh = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    estimated_minutes = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
        ordering = ['course_day', 'order']

    def __str__(self):
        return f"{self.course_day} - {self.title}"


class LessonStep(models.Model):
    """
    Individual step within a lesson
    """
    STEP_TYPES = [
        ('VOCAB_INTRO', 'Vocabulary Introduction'),
        ('VOCAB_RECOGNIZE', 'Vocabulary Recognition'),
        ('VOCAB_MATCH', 'Vocabulary Matching'),
        ('GRAMMAR_INTRO', 'Grammar Introduction'),
        ('BUILD_PHRASE', 'Build Phrase'),
        ('FILL_BLANK', 'Fill in the Blank'),
        ('SRS_REVIEW', 'SRS Review'),
    ]

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='steps')
    step_type = models.CharField(max_length=30, choices=STEP_TYPES)
    title = models.CharField(max_length=255, blank=True)
    content = models.JSONField(default=dict)  # Flexible content structure
    order = models.IntegerField(default=0)
    estimated_minutes = models.IntegerField(default=2)
    words = models.ManyToManyField(
        'vocab.Word',
        blank=True,
        related_name='lesson_steps'
    )
    grammar_rules = models.ManyToManyField(
        'vocab.GrammarRule',
        blank=True,
        related_name='lesson_steps'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Lesson Step'
        verbose_name_plural = 'Lesson Steps'
        ordering = ['lesson', 'order']

    def __str__(self):
        return f"{self.lesson} - Step {self.order}: {self.get_step_type_display()}"
