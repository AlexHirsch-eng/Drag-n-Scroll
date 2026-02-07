
"""
SuperMemo SM-2 Algorithm Implementation
"""
from datetime import datetime, timedelta
from typing import List
from django.utils import timezone
from vocab.models import Word, WordProgress, ReviewHistory


def update_srs(word_progress: WordProgress, quality: int, review_time_seconds: int = 0) -> WordProgress:
    """
    Update SRS state using SuperMemo SM-2 algorithm

    Args:
        word_progress: WordProgress instance to update
        quality: Quality rating (0-5)
            5: Perfect response (< 3 sec)
            4: Correct response (3-10 sec)
            3: Correct response (> 10 sec or with difficulty)
            2: Incorrect but remembered with hint
            1: Incorrect but recognized correct answer
            0: Complete failure
        review_time_seconds: Time taken to answer

    Returns:
        Updated WordProgress instance
    """
    # Store old values for history
    old_srs_level = word_progress.srs_level
    old_interval = word_progress.interval_days
    old_ease_factor = word_progress.ease_factor

    # If answer was unsuccessful (quality < 3)
    if quality < 3:
        # Reset to beginning
        word_progress.srs_level = 0
        word_progress.interval_days = 1
        word_progress.next_review_date = timezone.now() + timedelta(days=1)

        # Decrease ease factor
        word_progress.ease_factor = max(1.3, word_progress.ease_factor - 0.2)
    else:
        # Successful answer (quality >= 3)
        word_progress.srs_level += 1

        # Update ease factor using SM-2 formula
        # EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        ef = word_progress.ease_factor
        ef_new = ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        word_progress.ease_factor = max(1.3, ef_new)

        # Calculate interval
        if word_progress.srs_level == 1:
            interval = 1
        elif word_progress.srs_level == 2:
            interval = 6
        else:
            interval = round(word_progress.interval_days * word_progress.ease_factor)

        word_progress.interval_days = interval
        word_progress.next_review_date = timezone.now() + timedelta(days=interval)

    # Update statistics
    word_progress.total_reviews += 1
    if quality >= 3:
        word_progress.correct_reviews += 1
    word_progress.last_reviewed_at = timezone.now()
    word_progress.save()

    # Create review history record
    ReviewHistory.objects.create(
        user=word_progress.user,
        word=word_progress.word,
        quality=quality,
        old_srs_level=old_srs_level,
        new_srs_level=word_progress.srs_level,
        old_interval=old_interval,
        new_interval=word_progress.interval_days,
        old_ease_factor=old_ease_factor,
        new_ease_factor=word_progress.ease_factor,
        review_time_seconds=review_time_seconds
    )

    return word_progress


def get_srs_batch(user, batch_size: int = 10, hsk_level: int = None) -> List[WordProgress]:
    """
    Get a batch of words due for review

    Args:
        user: User instance
        batch_size: Number of words to return
        hsk_level: Optional HSK level filter

    Returns:
        List of WordProgress instances
    """
    queryset = WordProgress.objects.filter(
        user=user,
        next_review_date__lte=timezone.now(),
        srs_level__gt=0  # Exclude new words (level 0)
    ).select_related('word').order_by('next_review_date', 'ease_factor')

    if hsk_level is not None:
        queryset = queryset.filter(word__hsk_level=hsk_level)

    return list(queryset[:batch_size])


def get_due_count(user) -> dict:
    """
    Get statistics about words due for review

    Args:
        user: User instance

    Returns:
        Dictionary with due count statistics
    """
    now = timezone.now()
    today_end = now.replace(hour=23, minute=59, second=59)
    week_end = now + timedelta(days=7)

    # Count words due now, today, and this week
    due_now = WordProgress.objects.filter(
        user=user,
        next_review_date__lte=now,
        srs_level__gt=0
    ).count()

    due_today = WordProgress.objects.filter(
        user=user,
        next_review_date__lte=today_end,
        srs_level__gt=0
    ).count()

    due_this_week = WordProgress.objects.filter(
        user=user,
        next_review_date__lte=week_end,
        srs_level__gt=0
    ).count()

    # Count by learning status
    total_learning = WordProgress.objects.filter(
        user=user,
        srs_level__in=[1, 2, 3, 4]
    ).count()

    total_mastered = WordProgress.objects.filter(
        user=user,
        srs_level__gte=5
    ).count()

    return {
        'due_now': due_now,
        'due_today': due_today,
        'due_this_week': due_this_week,
        'total_learning': total_learning,
        'total_mastered': total_mastered
    }


def get_srs_stats(user) -> dict:
    """
    Get detailed SRS statistics for a user

    Args:
        user: User instance

    Returns:
        Dictionary with SRS statistics
    """
    # Count by SRS level
    by_srs_level = {}
    for level in range(9):  # 0-8
        count = WordProgress.objects.filter(
            user=user,
            srs_level=level
        ).count()
        by_srs_level[str(level)] = count

    # Calculate retention rate
    total_reviews = ReviewHistory.objects.filter(user=user).count()
    correct_reviews = ReviewHistory.objects.filter(
        user=user,
        quality__gte=3
    ).count()

    retention_rate = round(correct_reviews / total_reviews, 2) if total_reviews > 0 else 0.0

    # Average reviews per word
    total_words = WordProgress.objects.filter(user=user).count()
    total_review_count = sum(
        wp.total_reviews for wp in WordProgress.objects.filter(user=user)
    )
    avg_reviews_per_word = round(total_review_count / total_words, 1) if total_words > 0 else 0

    # Streak days from user progress
    streak_days = user.progress.streak_days

    # Upcoming reviews (next 7 days)
    upcoming_reviews = []
    for i in range(7):
        date = (timezone.now() + timedelta(days=i)).date()
        count = WordProgress.objects.filter(
            user=user,
            next_review_date__date=date
        ).count()
        upcoming_reviews.append({
            'date': date.isoformat(),
            'count': count
        })

    return {
        'total_words': total_words,
        'by_srs_level': by_srs_level,
        'retention_rate': retention_rate,
        'avg_reviews_per_word': avg_reviews_per_word,
        'streak_days': streak_days,
        'upcoming_reviews': upcoming_reviews
    }


def initialize_word_progress(user, word) -> WordProgress:
    """
    Initialize WordProgress for a new word

    Args:
        user: User instance
        word: Word instance

    Returns:
        Created WordProgress instance
    """
    progress, created = WordProgress.objects.get_or_create(
        user=user,
        word=word,
        defaults={
            'srs_level': 0,
            'ease_factor': 2.5,
            'interval_days': 0,
            'next_review_date': None
        }
    )
    return progress


def get_mistakes_batch(user, batch_size: int = 20, hsk_level: int = None) -> List[WordProgress]:
    """
    Get a batch of words that user struggled with (mistakes review)

    Words are considered "mistakes" if:
    - SRS level is 0, 1, or 2 (not well learned)
    - OR accuracy < 70% (struggled with this word)
    - Has been reviewed at least once

    Args:
        user: User instance
        batch_size: Number of words to return
        hsk_level: Optional HSK level filter

    Returns:
        List of WordProgress instances
    """
    from django.db.models import F, ExpressionWrapper, FloatField

    # Get words with low SRS level (0, 1, 2) that have been reviewed
    low_level_words = WordProgress.objects.filter(
        user=user,
        srs_level__in=[0, 1, 2],
        total_reviews__gte=1
    ).select_related('word')

    # Get words with poor accuracy (< 70%)
    poor_accuracy_words = WordProgress.objects.filter(
        user=user,
        total_reviews__gte=1
    ).annotate(
        accuracy=ExpressionWrapper(
            F('correct_reviews') * 1.0 / F('total_reviews'),
            output_field=FloatField()
        )
    ).filter(
        accuracy__lt=0.7
    ).select_related('word')

    # Combine both querysets and remove duplicates
    all_mistakes = (low_level_words | poor_accuracy_words).order_by('srs_level', '-total_reviews')

    if hsk_level is not None:
        all_mistakes = all_mistakes.filter(word__hsk_level=hsk_level)

    return list(all_mistakes[:batch_size])
