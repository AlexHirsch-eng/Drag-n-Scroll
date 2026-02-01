"""
Copy grammar rules from HSK 1 to HSK 2-6
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from course.models import Course, CourseDay

def copy_grammar_rules():
    """Copy grammar rules from HSK 1 to other levels"""

    # Get HSK 1 course
    hsk1_course = Course.objects.filter(hsk_level=1).first()
    if not hsk1_course:
        print('HSK 1 course not found!')
        return

    print(f'Copying grammar rules from HSK 1...\n')

    for target_level in range(2, 7):
        target_course = Course.objects.filter(hsk_level=target_level).first()
        if not target_course:
            print(f'HSK {target_level} course not found, skipping...')
            continue

        print(f'=== HSK {target_level} ===')

        # Copy grammar rules for each day
        for hsk1_day in hsk1_course.days.all():
            target_day = target_course.days.filter(day_number=hsk1_day.day_number).first()
            if not target_day:
                continue

            # Get grammar rules from HSK 1 day
            grammar_rules = list(hsk1_day.grammar_rules.all())

            # Add them to target day
            target_day.grammar_rules.add(*grammar_rules)

            print(f'  - Copied {len(grammar_rules)} grammar rules for Day {hsk1_day.day_number}')

        print(f'  - All grammar rules copied for HSK {target_level}\n')

    print('All grammar rules copied successfully!')

if __name__ == '__main__':
    copy_grammar_rules()
