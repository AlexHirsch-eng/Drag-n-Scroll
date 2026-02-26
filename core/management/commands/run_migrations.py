"""
Django management command to run migrations programmatically
Use this for initial deployment when you can't access shell
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Run database migrations for deployment'

    def handle(self, *args, **options):
        self.stdout.write('Running migrations...')

        try:
            call_command('migrate', '--run-syncdb')
            self.stdout.write(self.style.SUCCESS('✓ Migrations completed successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Migration error: {str(e)}'))
            raise
