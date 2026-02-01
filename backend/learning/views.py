"""
Views for Session A/B Learning System
5 Steps per session: SRS Review, New Words, Grammar, Dialogue, Word Arrangement
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404
import random
import uuid

from core.models import UserCourseProgress, UserProfile
from course.models import Course, CourseDay
from vocab.models import Word, WordProgress, GrammarRule
from .models import (
    LearningSession, Dialogue, WordArrangementExercise, GrammarTask,
    NewWordLearningProgress, StepProgress, SRSReviewCard
)
from .serializers import (
    LearningSessionSerializer, StartSessionSerializer,
    Step1DataSerializer, Step2DataSerializer, Step3DataSerializer,
    Step4DataSerializer, Step5DataSerializer, AnswerResponseSerializer,
    SessionSummaryResponseSerializer, MainScreenSerializer
)
from .srs import update_srs, get_srs_batch, get_due_count, initialize_word_progress


# ============================================================================
# MAIN SCREEN
# ============================================================================

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def main_screen(request):
    """
    Get main screen data with Session A/B cards
    Query params:
    - day (optional): override current day (1-5)
    - hsk (optional): override user's HSK level (1-6)
    """
    user = request.user
    user_profile = user.profile

    # Get or create user progress
    user_progress = user.progress
    if not user_progress:
        # Create progress record if it doesn't exist
        user_progress = UserCourseProgress.objects.create(user=user)

    # Check if specific HSK level requested
    hsk_level = request.query_params.get('hsk')
    if hsk_level:
        try:
            hsk_level = int(hsk_level)
            if hsk_level < 1 or hsk_level > 6:
                return Response({'error': 'HSK level must be between 1 and 6'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'Invalid HSK level'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        hsk_level = user_profile.current_hsk_level

    # Check if specific day requested
    day_number = request.query_params.get('day')
    if day_number:
        try:
            day_number = int(day_number)
            if day_number < 1 or day_number > 5:
                return Response({'error': 'Day must be between 1 and 5'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'Invalid day number'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        day_number = user_progress.current_day

    # Get course
    course = Course.objects.filter(
        hsk_level=hsk_level,
        is_active=True
    ).first()

    if not course:
        return Response({'error': 'No active course found'}, status=status.HTTP_404_NOT_FOUND)

    # Get course day
    course_day = course.days.filter(day_number=day_number).first()
    if not course_day:
        return Response({'error': 'Course day not found'}, status=status.HTTP_404_NOT_FOUND)

    # Get or create sessions
    session_a = LearningSession.objects.filter(
        user=user,
        course_day=course_day,
        session_type='A'
    ).first()

    session_b = LearningSession.objects.filter(
        user=user,
        course_day=course_day,
        session_type='B'
    ).first()

    # Get due for review count
    due_counts = get_due_count(user)

    # Get learning words count
    total_learning = WordProgress.objects.filter(
        user=user,
        srs_level__in=[1, 2, 3, 4]
    ).count()

    response_data = {
        'current_course_day': {
            'id': course_day.id,
            'day_number': course_day.day_number,
            'title': course_day.title,
            'description': course_day.description,
            'estimated_minutes': course_day.estimated_minutes
        },
        'session_a': None,
        'session_b': None,
        'due_for_review': due_counts['due_now'],
        'total_learning_words': total_learning,
        'streak_days': user_progress.streak_days,
        'xp_total': user_progress.total_xp
    }

    if session_a:
        response_data['session_a'] = LearningSessionSerializer(session_a).data

    if session_b:
        response_data['session_b'] = LearningSessionSerializer(session_b).data

    return Response(response_data)


# ============================================================================
# SESSION MANAGEMENT
# ============================================================================

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def start_session(request):
    """
    Start a new learning session (A or B)
    """
    serializer = StartSessionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    course_day_id = serializer.validated_data['course_day_id']
    session_type = serializer.validated_data['session_type']
    user = request.user

    course_day = get_object_or_404(CourseDay, id=course_day_id)

    # Check if session already exists
    existing_session = LearningSession.objects.filter(
        user=user,
        course_day=course_day,
        session_type=session_type
    ).first()

    if existing_session:
        # Resume existing session
        session = existing_session
    else:
        # Create new session
        session = LearningSession.objects.create(
            user=user,
            course_day=course_day,
            session_type=session_type,
            current_step=1
        )

    # Get step 1 data (SRS Review) - call helper directly to avoid decorator issues
    return _get_step_1_data(session)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def complete_session(request):
    """
    Complete a session and show summary
    """
    session_id = request.data.get('session_id')
    user = request.user

    session = get_object_or_404(LearningSession, id=session_id, user=user)

    # Mark as completed
    session.is_completed = True
    session.completed_at = timezone.now()
    session.current_step = 6  # 6 = completed
    session.save()

    # Check if both sessions A and B are completed
    session_a = LearningSession.objects.filter(
        user=user,
        course_day=session.course_day,
        session_type='A',
        is_completed=True
    ).exists()

    session_b = LearningSession.objects.filter(
        user=user,
        course_day=session.course_day,
        session_type='B',
        is_completed=True
    ).exists()

    is_day_completed = session_a and session_b

    # If both sessions completed, move to next day
    if is_day_completed:
        user_progress = user.progress
        if not user_progress:
            user_progress = UserCourseProgress.objects.create(user=user)
        user_progress.current_day += 1
        user_progress.save()

    # Get problematic words details
    problematic_words = []
    if session.problematic_words:
        words = Word.objects.filter(id__in=session.problematic_words)
        problematic_words = [
            {
                'id': w.id,
                'hanzi': w.hanzi,
                'pinyin': w.pinyin,
                'translation_ru': w.translation_ru,
                'translation_kz': w.translation_kz
            }
            for w in words
        ]

    response_data = {
        'session': LearningSessionSerializer(session).data,
        'words_learned': session.words_learned,
        'accuracy_percentage': session.accuracy_percentage,
        'problematic_words_count': len(session.problematic_words),
        'problematic_words': problematic_words,
        'time_spent_minutes': session.total_time_minutes,
        'xp_earned': session.xp_earned,
        'is_day_completed': is_day_completed
    }

    return Response(response_data)


# ============================================================================
# STEP DATA RETRIEVAL
# ============================================================================

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_step_data(request, session_id):
    """
    Get data for the current step of a session
    """
    user = request.user
    session = get_object_or_404(LearningSession, id=session_id, user=user)

    step = session.current_step

    if step == 1:
        return _get_step_1_data(session)
    elif step == 2:
        return _get_step_2_data(session)
    elif step == 3:
        return _get_step_3_data(session)
    elif step == 4:
        return _get_step_4_data(session)
    elif step == 5:
        return _get_step_5_data(session)
    else:
        return Response({'error': 'Session completed'}, status=status.HTTP_400_BAD_REQUEST)


def _get_step_1_data(session):
    """
    Step 1: SRS Review (2 minutes)
    Get 10 words from previous lessons for review with SRS logic
    """
    # Mark step as started
    if not session.step_1_started_at:
        session.step_1_started_at = timezone.now()
        session.save()

    # Get 10 words due for review
    word_progress_list = get_srs_batch(session.user, batch_size=10)

    # Create SRS cards for this session
    cards = []
    for wp in word_progress_list:
        # Get 3 distractor words for multiple choice
        distractors = Word.objects.filter(
            hsk_level=wp.word.hsk_level
        ).exclude(id=wp.word.id).order_by('?')[:3]

        # Create options (correct word + 3 distractors)
        options = [{'word_id': wp.word.id, 'translation_ru': wp.word.translation_ru,
                    'translation_kz': wp.word.translation_kz}]
        for d in distractors:
            options.append({'word_id': d.id, 'translation_ru': d.translation_ru,
                          'translation_kz': d.translation_kz})

        # Shuffle options
        random.shuffle(options)

        # Create card - use filter().first() to handle potential duplicates
        card = SRSReviewCard.objects.filter(
            session=session,
            word=wp.word
        ).first()

        if not card:
            # Create new card if doesn't exist
            card = SRSReviewCard.objects.create(
                session=session,
                word=wp.word,
                options=options
            )

        cards.append(card)

    # If less than 10 words available, pad with random words
    if len(cards) < 10:
        existing_word_ids = [c.word.id for c in cards]
        additional_words = Word.objects.filter(
            hsk_level=session.user.profile.current_hsk_level
        ).exclude(id__in=existing_word_ids).order_by('?')[:(10 - len(cards))]

        for word in additional_words:
            distractors = Word.objects.filter(
                hsk_level=word.hsk_level
            ).exclude(id=word.id).order_by('?')[:3]

            options = [{'word_id': word.id, 'translation_ru': word.translation_ru,
                        'translation_kz': word.translation_kz}]
            for d in distractors:
                options.append({'word_id': d.id, 'translation_ru': d.translation_ru,
                              'translation_kz': d.translation_kz})
            random.shuffle(options)

            card = SRSReviewCard.objects.create(
                session=session,
                word=word,
                options=options
            )
            cards.append(card)

    response_data = {
        'step': 1,
        'step_type': 'SRS_REVIEW',
        'data': {
            'cards': [
                {
                    'id': card.id,
                    'word': {
                        'id': card.word.id,
                        'hanzi': card.word.hanzi,
                        'pinyin': card.word.pinyin,
                        'audio_url': card.word.audio_url
                    },
                    'options': card.options
                }
                for card in cards
            ],
            'total_cards': len(cards),
            'current_card_index': 0
        },
        'session': LearningSessionSerializer(session).data
    }

    return Response(response_data)


def _get_step_2_data(session):
    """
    Step 2: New Words (8 minutes)
    Get 5 new words to learn with mini-tests
    """
    # Mark step as started
    if not session.step_2_started_at:
        session.step_2_started_at = timezone.now()
        session.save()

    # Get new words from course day (not yet learned by user)
    learned_word_ids = WordProgress.objects.filter(
        user=session.user,
        srs_level__gt=0
    ).values_list('word_id', flat=True)

    new_words = session.course_day.new_words.exclude(
        id__in=learned_word_ids
    )[:5]

    # Initialize progress for these words
    words_data = []
    for word in new_words:
        # Create progress record
        NewWordLearningProgress.objects.get_or_create(
            session=session,
            word=word
        )

        words_data.append({
            'id': word.id,
            'hanzi': word.hanzi,
            'pinyin': word.pinyin,
            'translation_ru': word.translation_ru,
            'translation_kz': word.translation_kz,
            'audio_url': word.audio_url
        })

    response_data = {
        'step': 2,
        'step_type': 'NEW_WORDS',
        'data': {
            'words': words_data,
            'total_words': len(words_data),
            'current_word_index': 0
        },
        'session': LearningSessionSerializer(session).data
    }

    return Response(response_data)


def _get_step_3_data(session):
    """
    Step 3: Grammar (2 minutes)
    Get grammar rule with sentence building task
    """
    # Mark step as started
    if not session.step_3_started_at:
        session.step_3_started_at = timezone.now()
        session.save()

    # Get grammar task for this session
    grammar_task = GrammarTask.objects.filter(
        course_day=session.course_day,
        session_type=session.session_type
    ).first()

    if not grammar_task:
        # Fallback: get any grammar rule from course day
        grammar_rule = session.course_day.grammar_rules.first()
        if grammar_rule:
            # Create a simple grammar task
            grammar_task = GrammarTask.objects.create(
                course_day=session.course_day,
                session_type=session.session_type,
                grammar_rule=grammar_rule,
                task_prompt_ru=f"Постройте предложение используя шаблон: {grammar_rule.pattern}",
                task_prompt_kz=f"Үлгіні қолдана отырып, сөйлем құрыңыз: {grammar_rule.pattern}",
                components=[],
                correct_hanzi="",
                correct_pinyin="",
                correct_translation_ru="",
                correct_translation_kz=""
            )

    task_data = None
    if grammar_task:
        # Get examples from grammar rule
        examples = []
        for ex in grammar_task.grammar_rule.examples.all()[:2]:
            examples.append({
                'hanzi': ex.sentence_hanzi,
                'pinyin': ex.sentence_pinyin,
                'translation_ru': ex.translation_ru,
                'translation_kz': ex.translation_kz
            })

        task_data = {
            'id': grammar_task.id,
            'grammar_rule': {
                'id': grammar_task.grammar_rule.id,
                'title': grammar_task.grammar_rule.title,
                'pattern': grammar_task.grammar_rule.pattern,
                'explanation_ru': grammar_task.grammar_rule.explanation_ru,
                'explanation_kz': grammar_task.grammar_rule.explanation_kz,
                'examples': examples
            },
            'task_prompt_ru': grammar_task.task_prompt_ru,
            'task_prompt_kz': grammar_task.task_prompt_kz,
            'components': grammar_task.components
        }

    response_data = {
        'step': 3,
        'step_type': 'GRAMMAR',
        'data': task_data,
        'session': LearningSessionSerializer(session).data
    }

    return Response(response_data)


def _get_step_4_data(session):
    """
    Step 4: Dialogue (2 minutes)
    Get dialogue for listening comprehension
    """
    # Mark step as started
    if not session.step_4_started_at:
        session.step_4_started_at = timezone.now()
        session.save()

    # Get dialogue for this session
    dialogue = Dialogue.objects.filter(
        course_day=session.course_day,
        session_type=session.session_type
    ).first()

    dialogue_data = None
    if dialogue:
        dialogue_data = {
            'id': dialogue.id,
            'lines': dialogue.lines,
            'question_hanzi': dialogue.question_hanzi,
            'question_pinyin': dialogue.question_pinyin,
            'question_translation_ru': dialogue.question_translation_ru,
            'question_translation_kz': dialogue.question_translation_kz,
            'audio_url': dialogue.audio_url,
            'options': dialogue.options
        }

    response_data = {
        'step': 4,
        'step_type': 'DIALOGUE',
        'data': dialogue_data,
        'session': LearningSessionSerializer(session).data
    }

    return Response(response_data)


def _get_step_5_data(session):
    """
    Step 5: Word Arrangement (1 minute)
    Get word arrangement exercise
    """
    # Mark step as started
    if not session.step_5_started_at:
        session.step_5_started_at = timezone.now()
        session.save()

    # Get arrangement exercise for this session
    exercise = WordArrangementExercise.objects.filter(
        course_day=session.course_day,
        session_type=session.session_type
    ).first()

    exercise_data = None
    if exercise:
        exercise_data = {
            'id': exercise.id,
            'target_hanzi': exercise.target_hanzi,
            'target_pinyin': exercise.target_pinyin,
            'target_translation_ru': exercise.target_translation_ru,
            'target_translation_kz': exercise.target_translation_kz,
            'audio_url': exercise.audio_url,
            'scrambled_words': exercise.scrambled_words,
            'hint_ru': exercise.hint_ru,
            'hint_kz': exercise.hint_kz
        }

    response_data = {
        'step': 5,
        'step_type': 'WORD_ARRANGEMENT',
        'data': exercise_data,
        'session': LearningSessionSerializer(session).data
    }

    return Response(response_data)


# ============================================================================
# STEP SUBMISSION
# ============================================================================

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_step_1(request):
    """
    Submit Step 1 (SRS Review) answers
    """
    session_id = request.data.get('session_id')
    card_id = request.data.get('card_id')
    selected_option_id = request.data.get('selected_option_id')
    time_spent_seconds = request.data.get('time_spent_seconds', 0)
    current_card_index = request.data.get('current_card_index', 0)  # Current 0-based index
    total_shown_cards = request.data.get('total_shown_cards', 0)  # Total cards shown to user

    user = request.user
    session = get_object_or_404(LearningSession, id=session_id, user=user)
    card = get_object_or_404(SRSReviewCard, id=card_id, session=session)

    # Check if answer is correct
    correct_word_id = card.word.id
    is_correct = (selected_option_id == correct_word_id)

    # Update card
    card.selected_option_id = selected_option_id
    card.is_correct = is_correct
    card.time_spent_seconds = time_spent_seconds
    card.completed_at = timezone.now()

    # Mark as problematic if incorrect
    if not is_correct:
        card.is_problematic = True
        if card.word.id not in session.problematic_words:
            session.problematic_words.append(card.word.id)

    card.save()
    session.save()

    # Update SRS for this word
    word_progress = WordProgress.objects.filter(
        user=user,
        word=card.word
    ).first()

    if word_progress:
        # Quality rating based on correctness
        quality = 4 if is_correct else 1
        update_srs(word_progress, quality, time_spent_seconds)

    # Update session stats
    session.total_questions += 1
    if is_correct:
        session.correct_answers += 1
        session.xp_earned += 5
    session.save()

    # Check if all cards are completed
    # Use frontend data if provided, otherwise fallback to DB check
    if total_shown_cards > 0:
        # Frontend tells us this was the last card it showed
        is_step_completed = (current_card_index + 1 >= total_shown_cards)
    else:
        # Fallback: check DB
        remaining_cards = session.srs_cards.filter(completed_at__isnull=True).count()
        is_step_completed = (remaining_cards == 0)

    if is_step_completed:
        session.step_1_completed_at = timezone.now()
        session.current_step = 2
        session.save()
        print(f"Step 1 completed! Moving to step 2")

    # Get next card or step completion
    next_data = {}
    if not is_step_completed:
        next_card = session.srs_cards.filter(completed_at__isnull=True).first()
        if next_card:
            next_data = {
                'next_card': {
                    'id': next_card.id,
                    'word': {
                        'id': next_card.word.id,
                        'hanzi': next_card.word.hanzi,
                        'pinyin': next_card.word.pinyin,
                        'audio_url': next_card.word.audio_url
                    },
                    'options': next_card.options
                }
            }

    response_data = {
        'is_correct': is_correct,
        'is_step_completed': is_step_completed,
        'xp_earned': 5 if is_correct else 0,
        'next_step': 2 if is_step_completed else None,
        'session': LearningSessionSerializer(session).data,
        **next_data
    }

    print(f"Response: is_step_completed={response_data['is_step_completed']}, next_step={response_data['next_step']}")

    return Response(response_data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_step_2(request):
    """
    Submit Step 2 (New Words) completion
    """
    session_id = request.data.get('session_id')
    words_data = request.data.get('words', [])

    user = request.user
    session = get_object_or_404(LearningSession, id=session_id, user=user)

    # Process each word
    correct_count = 0
    for word_answer in words_data:
        word_id = word_answer.get('word_id')
        is_correct = word_answer.get('is_correct')
        time_spent = word_answer.get('time_spent_seconds', 0)
        pronunciation_attempts = word_answer.get('pronunciation_attempts', 0)
        pronunciation_ok_count = word_answer.get('pronunciation_ok_count', 0)

        # Update progress
        progress = NewWordLearningProgress.objects.filter(
            session=session,
            word_id=word_id
        ).first()

        if progress:
            progress.is_correct = is_correct
            progress.time_spent_seconds = time_spent
            progress.pronunciation_attempts = pronunciation_attempts
            progress.pronunciation_ok_count = pronunciation_ok_count
            progress.completed_at = timezone.now()
            progress.save()

        if is_correct:
            correct_count += 1

        # Initialize SRS for new word
        word = Word.objects.filter(id=word_id).first()
        if word:
            initialize_word_progress(user, word)
            # Mark as learned (level 1)
            word_progress = WordProgress.objects.filter(
                user=user,
                word=word
            ).first()
            if word_progress:
                word_progress.srs_level = 1
                word_progress.next_review_date = timezone.now()
                word_progress.save()

    # Update session
    session.words_learned = len(words_data)
    session.total_questions += len(words_data)
    session.correct_answers += correct_count
    session.xp_earned += correct_count * 10
    session.step_2_completed_at = timezone.now()
    session.current_step = 3
    session.save()

    response_data = {
        'is_correct': True,  # Step is completed
        'is_step_completed': True,
        'xp_earned': correct_count * 10,
        'next_step': 3,
        'session': LearningSessionSerializer(session).data
    }

    return Response(response_data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_step_3(request):
    """
    Submit Step 3 (Grammar) answer
    """
    session_id = request.data.get('session_id')
    built_sentence = request.data.get('built_sentence_hanzi', '')
    time_spent_seconds = request.data.get('time_spent_seconds', 0)

    user = request.user
    session = get_object_or_404(LearningSession, id=session_id, user=user)

    # Get grammar task
    grammar_task = GrammarTask.objects.filter(
        course_day=session.course_day,
        session_type=session.session_type
    ).first()

    is_correct = False
    if grammar_task:
        # Simple comparison (can be enhanced for more flexible matching)
        is_correct = (built_sentence.strip() == grammar_task.correct_hanzi.strip())

    # Create step progress record
    StepProgress.objects.create(
        session=session,
        step_type='GRAMMAR',
        data={'built_sentence': built_sentence},
        is_correct=is_correct,
        time_spent_seconds=time_spent_seconds,
        completed_at=timezone.now()
    )

    # Update session
    session.total_questions += 1
    if is_correct:
        session.correct_answers += 1
        session.xp_earned += 10
    session.step_3_completed_at = timezone.now()
    session.current_step = 4
    session.save()

    response_data = {
        'is_correct': is_correct,
        'is_step_completed': True,
        'xp_earned': 10 if is_correct else 0,
        'correct_answer': {'hanzi': grammar_task.correct_hanzi} if grammar_task else None,
        'next_step': 4,
        'session': LearningSessionSerializer(session).data
    }

    return Response(response_data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_step_4(request):
    """
    Submit Step 4 (Dialogue) answer
    """
    session_id = request.data.get('session_id')
    selected_option_index = request.data.get('selected_option_index')
    time_spent_seconds = request.data.get('time_spent_seconds', 0)

    user = request.user
    session = get_object_or_404(LearningSession, id=session_id, user=user)

    # Get dialogue
    dialogue = Dialogue.objects.filter(
        course_day=session.course_day,
        session_type=session.session_type
    ).first()

    is_correct = False
    explanation = ''
    if dialogue:
        # Check if selected option is correct
        if 0 <= selected_option_index < len(dialogue.options):
            is_correct = dialogue.options[selected_option_index].get('is_correct', False)

        # Get explanation based on user language
        if user.profile.preferred_language == 'kz':
            explanation = dialogue.explanation_kz
        else:
            explanation = dialogue.explanation_ru

    # Create step progress record
    StepProgress.objects.create(
        session=session,
        step_type='DIALOGUE',
        data={'selected_option_index': selected_option_index},
        is_correct=is_correct,
        time_spent_seconds=time_spent_seconds,
        completed_at=timezone.now()
    )

    # Update session
    session.total_questions += 1
    if is_correct:
        session.correct_answers += 1
        session.xp_earned += 10
    session.step_4_completed_at = timezone.now()
    session.current_step = 5
    session.save()

    response_data = {
        'is_correct': is_correct,
        'is_step_completed': True,
        'xp_earned': 10 if is_correct else 0,
        'explanation': explanation,
        'next_step': 5,
        'session': LearningSessionSerializer(session).data
    }

    return Response(response_data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_step_5(request):
    """
    Submit Step 5 (Word Arrangement) answer
    """
    session_id = request.data.get('session_id')
    arranged_word_ids = request.data.get('arranged_word_ids', [])
    time_spent_seconds = request.data.get('time_spent_seconds', 0)

    user = request.user
    session = get_object_or_404(LearningSession, id=session_id, user=user)

    # Get exercise
    exercise = WordArrangementExercise.objects.filter(
        course_day=session.course_day,
        session_type=session.session_type
    ).first()

    is_correct = False
    if exercise:
        # Check if arrangement is correct
        # This is a simple check - can be enhanced
        correct_order = [w.get('id') for w in exercise.scrambled_words]
        # For now, just check if all words are present (order validation would be more complex)
        is_correct = (sorted(arranged_word_ids) == sorted(correct_order))

    # Create step progress record
    StepProgress.objects.create(
        session=session,
        step_type='WORD_ARRANGEMENT',
        data={'arranged_word_ids': arranged_word_ids},
        is_correct=is_correct,
        time_spent_seconds=time_spent_seconds,
        completed_at=timezone.now()
    )

    # Update session
    session.total_questions += 1
    if is_correct:
        session.correct_answers += 1
        session.xp_earned += 10
    session.step_5_completed_at = timezone.now()
    session.current_step = 6  # Completed
    session.save()

    response_data = {
        'is_correct': is_correct,
        'is_step_completed': True,
        'xp_earned': 10 if is_correct else 0,
        'correct_answer': {'target_hanzi': exercise.target_hanzi} if exercise else None,
        'next_step': None,  # Session complete
        'session': LearningSessionSerializer(session).data
    }

    return Response(response_data)
