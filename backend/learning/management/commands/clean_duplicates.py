from django.core.management.base import BaseCommand
from learning.models import SRSReviewCard
from django.db.models import Count, Q


class Command(BaseCommand):
    help = 'Clean up duplicate SRSReviewCard entries'

    def handle(self, *args, **options):
        # Find duplicates (same session and word)
        duplicates = SRSReviewCard.objects.values(
            'session', 'word'
        ).annotate(
            count=Count('id')
        ).filter(
            count__gt=1
        )

        total_duplicates = duplicates.count()
        self.stdout.write(f'Found {total_duplicates} duplicate groups')

        deleted_count = 0

        for dup in duplicates:
            # Get all cards with this session and word, ordered by created_at
            cards = SRSReviewCard.objects.filter(
                session_id=dup['session'],
                word_id=dup['word']
            ).order_by('created_at', 'id')

            # Keep the first one, delete the rest
            cards_to_keep = cards.first()
            cards_to_delete = cards[1:]

            for card in cards_to_delete:
                card.delete()
                deleted_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {deleted_count} duplicate cards')
        )
