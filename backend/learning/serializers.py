"""
Serializers for Session A/B learning system
"""
from rest_framework import serializers
from .models import (
    LearningSession, Dialogue, WordArrangementExercise, GrammarTask,
    NewWordLearningProgress, StepProgress, SRSReviewCard
)
from course.serializers import CourseDaySerializer
from vocab.serializers import WordSerializer, GrammarRuleSerializer
from vocab.models import Word


class DialogueSerializer(serializers.ModelSerializer):
    """Serializer for Dialogue model (Step 4)"""
    class Meta:
        model = Dialogue
        fields = [
            'id', 'course_day', 'session_type', 'lines',
            'question_hanzi', 'question_pinyin',
            'question_translation_ru', 'question_translation_kz',
            'audio_url', 'options', 'explanation_ru', 'explanation_kz'
        ]


class WordArrangementExerciseSerializer(serializers.ModelSerializer):
    """Serializer for Word Arrangement Exercise (Step 5)"""
    class Meta:
        model = WordArrangementExercise
        fields = [
            'id', 'course_day', 'session_type',
            'target_hanzi', 'target_pinyin',
            'target_translation_ru', 'target_translation_kz',
            'audio_url', 'scrambled_words', 'hint_ru', 'hint_kz'
        ]


class GrammarTaskSerializer(serializers.ModelSerializer):
    """Serializer for Grammar Task (Step 3)"""
    grammar_rule = GrammarRuleSerializer(read_only=True)

    class Meta:
        model = GrammarTask
        fields = [
            'id', 'course_day', 'session_type', 'grammar_rule',
            'task_prompt_ru', 'task_prompt_kz', 'components',
            'correct_hanzi', 'correct_pinyin',
            'correct_translation_ru', 'correct_translation_kz'
        ]


class SRSReviewCardSerializer(serializers.ModelSerializer):
    """Serializer for SRS flashcard (Step 1)"""
    word = WordSerializer(read_only=True)

    class Meta:
        model = SRSReviewCard
        fields = [
            'id', 'word', 'options', 'selected_option_id',
            'is_correct', 'is_problematic', 'time_spent_seconds'
        ]


class NewWordLearningProgressSerializer(serializers.ModelSerializer):
    """Serializer for tracking new word learning (Step 2)"""
    word = WordSerializer(read_only=True)

    class Meta:
        model = NewWordLearningProgress
        fields = [
            'id', 'word', 'is_correct', 'attempts',
            'time_spent_seconds', 'pronunciation_attempts',
            'pronunciation_ok_count', 'completed_at'
        ]


class StepProgressSerializer(serializers.ModelSerializer):
    """Serializer for step progress tracking"""
    class Meta:
        model = StepProgress
        fields = [
            'id', 'step_type', 'data', 'started_at',
            'completed_at', 'time_spent_seconds',
            'is_correct', 'attempts'
        ]


class LearningSessionSerializer(serializers.ModelSerializer):
    """Serializer for Learning Session (A/B)"""
    course_day = CourseDaySerializer(read_only=True)
    accuracy = serializers.ReadOnlyField()
    accuracy_percentage = serializers.ReadOnlyField()
    total_time_minutes = serializers.ReadOnlyField()

    class Meta:
        model = LearningSession
        fields = [
            'id', 'course_day', 'session_type', 'current_step',
            'is_completed', 'started_at', 'completed_at',
            'words_learned', 'problematic_words', 'total_questions',
            'correct_answers', 'xp_earned', 'accuracy',
            'accuracy_percentage', 'total_time_minutes',
            'step_1_started_at', 'step_1_completed_at',
            'step_2_started_at', 'step_2_completed_at',
            'step_3_started_at', 'step_3_completed_at',
            'step_4_started_at', 'step_4_completed_at',
            'step_5_started_at', 'step_5_completed_at',
        ]
        read_only_fields = ['started_at', 'current_step']


class StartSessionSerializer(serializers.Serializer):
    """Serializer for starting a new session"""
    course_day_id = serializers.IntegerField()
    session_type = serializers.ChoiceField(choices=['A', 'B'])


class Step1DataSerializer(serializers.Serializer):
    """Serializer for Step 1 (SRS Review) data"""
    cards = SRSReviewCardSerializer(many=True)
    current_card_index = serializers.IntegerField(default=0)
    total_cards = serializers.IntegerField()
    time_remaining_seconds = serializers.IntegerField()


class Step2WordSerializer(serializers.Serializer):
    """Serializer for a single word in Step 2"""
    id = serializers.IntegerField()
    hanzi = serializers.CharField()
    pinyin = serializers.CharField()
    translation_ru = serializers.CharField()
    translation_kz = serializers.CharField()
    audio_url = serializers.CharField(allow_blank=True)
    audio_slow_url = serializers.CharField(allow_blank=True, required=False)


class Step2DataSerializer(serializers.Serializer):
    """Serializer for Step 2 (New Words) data"""
    words = Step2WordSerializer(many=True)
    current_word_index = serializers.IntegerField(default=0)
    total_words = serializers.IntegerField()
    time_remaining_seconds = serializers.IntegerField()


class Step3DataSerializer(serializers.Serializer):
    """Serializer for Step 3 (Grammar) data"""
    grammar_rule = GrammarTaskSerializer(read_only=True)
    time_remaining_seconds = serializers.IntegerField()


class Step4DataSerializer(serializers.Serializer):
    """Serializer for Step 4 (Dialogue) data"""
    dialogue = DialogueSerializer(read_only=True)
    time_remaining_seconds = serializers.IntegerField()


class Step5DataSerializer(serializers.Serializer):
    """Serializer for Step 5 (Word Arrangement) data"""
    exercise = WordArrangementExerciseSerializer(read_only=True)
    time_remaining_seconds = serializers.IntegerField()


class SessionStepSerializer(serializers.Serializer):
    """Serializer for getting step data"""
    step = serializers.IntegerField()
    step_type = serializers.CharField()
    data = serializers.DictField()
    session = LearningSessionSerializer(read_only=True)


class SubmitAnswerSerializer(serializers.Serializer):
    """Base serializer for submitting answers"""
    session_id = serializers.IntegerField()


class Step1AnswerSerializer(SubmitAnswerSerializer):
    """Serializer for submitting Step 1 (SRS card) answer"""
    card_id = serializers.IntegerField()
    selected_option_id = serializers.IntegerField()
    time_spent_seconds = serializers.IntegerField()


class Step2WordAnswerSerializer(serializers.Serializer):
    """Serializer for answering a single word in Step 2"""
    word_id = serializers.IntegerField()
    selected_option_id = serializers.IntegerField()  # For mini-test
    is_correct = serializers.BooleanField()
    time_spent_seconds = serializers.IntegerField()
    pronunciation_attempts = serializers.IntegerField(default=0)
    pronunciation_ok_count = serializers.IntegerField(default=0)


class Step2AnswerSerializer(SubmitAnswerSerializer):
    """Serializer for completing Step 2 (all words)"""
    words = Step2WordAnswerSerializer(many=True)


class Step3AnswerSerializer(SubmitAnswerSerializer):
    """Serializer for submitting Step 3 (Grammar task) answer"""
    selected_components = serializers.ListField(child=serializers.IntegerField())
    built_sentence_hanzi = serializers.CharField()
    time_spent_seconds = serializers.IntegerField()


class Step4AnswerSerializer(SubmitAnswerSerializer):
    """Serializer for submitting Step 4 (Dialogue) answer"""
    selected_option_index = serializers.IntegerField()
    time_spent_seconds = serializers.IntegerField()


class Step5AnswerSerializer(SubmitAnswerSerializer):
    """Serializer for submitting Step 5 (Word Arrangement) answer"""
    arranged_word_ids = serializers.ListField(child=serializers.IntegerField())
    time_spent_seconds = serializers.IntegerField()


class AnswerResponseSerializer(serializers.Serializer):
    """Response serializer for answer submission"""
    is_correct = serializers.BooleanField()
    is_step_completed = serializers.BooleanField()
    xp_earned = serializers.IntegerField()
    correct_answer = serializers.DictField(required=False)
    explanation = serializers.CharField(required=False)
    next_step = serializers.IntegerField(required=False)
    session = LearningSessionSerializer(read_only=True)


class SessionSummarySerializer(serializers.Serializer):
    """Serializer for session completion summary"""
    session_id = serializers.IntegerField()


class SessionSummaryResponseSerializer(serializers.Serializer):
    """Response serializer for session summary"""
    session = LearningSessionSerializer(read_only=True)
    words_learned = serializers.IntegerField()
    accuracy_percentage = serializers.CharField()
    problematic_words_count = serializers.IntegerField()
    problematic_words = WordSerializer(many=True, required=False)
    time_spent_minutes = serializers.FloatField()
    xp_earned = serializers.IntegerField()
    is_day_completed = serializers.BooleanField()


class MainScreenSerializer(serializers.Serializer):
    """Serializer for main screen data"""
    current_course_day = CourseDaySerializer(read_only=True)
    session_a = LearningSessionSerializer(read_only=True, required=False)
    session_b = LearningSessionSerializer(read_only=True, required=False)
    due_for_review = serializers.IntegerField()
    total_learning_words = serializers.IntegerField()
    streak_days = serializers.IntegerField()
    xp_total = serializers.IntegerField()
