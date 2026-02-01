"""
Create HSK 2-6 courses with days and basic data
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from course.models import Course, CourseDay

def create_hsk_courses():
    """Create HSK 2-6 courses with 5 days each"""

    for hsk_level in range(2, 7):
        # Check if course already exists
        existing = Course.objects.filter(hsk_level=hsk_level).first()
        if existing:
            print(f'HSK {hsk_level} already exists, skipping...')
            continue

        # Create course
        course = Course.objects.create(
            hsk_level=hsk_level,
            title=f'HSK {hsk_level} Course',
            description=f'Complete HSK {hsk_level} Chinese course',
            is_active=True,
            total_days=5
        )

        print(f'Created HSK {hsk_level} course')

        # Create 5 days for each course
        for day_num in range(1, 6):
            day = CourseDay.objects.create(
                course=course,
                day_number=day_num,
                title=f'Day {day_num}: HSK {hsk_level} Chinese',
                description=f'Learning HSK {hsk_level} - Day {day_num}',
                estimated_minutes=15
            )
            print(f'  - Created Day {day_num}')

        print(f'HSK {hsk_level} complete with 5 days\n')

    print('\nAll HSK courses created successfully!')

if __name__ == '__main__':
    create_hsk_courses()
