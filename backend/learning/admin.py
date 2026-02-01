from django.contrib import admin
from .models import (
    LearningSession,
    Dialogue,
    WordArrangementExercise,
    GrammarTask,
    NewWordLearningProgress,
    StepProgress,
    SRSReviewCard
)


@admin.register(LearningSession)
class LearningSessionAdmin(admin.ModelAdmin):
    """Admin for Learning Sessions (A/B)"""
    list_display = ['user', 'course_day', 'session_type', 'current_step',
                    'is_completed', 'accuracy_percentage', 'xp_earned', 'started_at']
    list_filter = ['session_type', 'is_completed', 'started_at']
    search_fields = ['user__username', 'course_day__title']
    readonly_fields = ['started_at', 'completed_at', 'accuracy', 'accuracy_percentage']


@admin.register(Dialogue)
class DialogueAdmin(admin.ModelAdmin):
    """Admin for Dialogues (Step 4)"""
    list_display = ['course_day', 'session_type', 'order', 'created_at']
    list_filter = ['session_type', 'course_day']
    search_fields = ['course_day__title', 'question_hanzi']


@admin.register(WordArrangementExercise)
class WordArrangementExerciseAdmin(admin.ModelAdmin):
    """Admin for Word Arrangement Exercises (Step 5)"""
    list_display = ['course_day', 'session_type', 'order', 'target_hanzi', 'created_at']
    list_filter = ['session_type', 'course_day']
    search_fields = ['course_day__title', 'target_hanzi']


@admin.register(GrammarTask)
class GrammarTaskAdmin(admin.ModelAdmin):
    """Admin for Grammar Tasks (Step 3)"""
    list_display = ['course_day', 'session_type', 'grammar_rule', 'order', 'created_at']
    list_filter = ['session_type', 'course_day', 'grammar_rule']
    search_fields = ['course_day__title', 'grammar_rule__title']


@admin.register(NewWordLearningProgress)
class NewWordLearningProgressAdmin(admin.ModelAdmin):
    """Admin for New Word Learning Progress"""
    list_display = ['session', 'word', 'is_correct', 'attempts',
                    'pronunciation_attempts', 'completed_at']
    list_filter = ['is_correct', 'completed_at']
    search_fields = ['session__user__username', 'word__hanzi']


@admin.register(StepProgress)
class StepProgressAdmin(admin.ModelAdmin):
    """Admin for Step Progress"""
    list_display = ['session', 'step_type', 'is_correct', 'attempts',
                    'time_spent_seconds', 'completed_at']
    list_filter = ['step_type', 'is_correct', 'completed_at']
    search_fields = ['session__user__username']


@admin.register(SRSReviewCard)
class SRSReviewCardAdmin(admin.ModelAdmin):
    """Admin for SRS Review Cards (Step 1)"""
    list_display = ['session', 'word', 'is_correct', 'is_problematic',
                    'time_spent_seconds', 'completed_at']
    list_filter = ['is_correct', 'is_problematic', 'completed_at']
    search_fields = ['session__user__username', 'word__hanzi']
