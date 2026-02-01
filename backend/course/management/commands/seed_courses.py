"""
Management command to seed initial course data
"""
from django.core.management.base import BaseCommand
from course.models import Course, CourseDay, Lesson, LessonStep
from vocab.models import Word


class Command(BaseCommand):
    help = 'Create initial course data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating course data...')

        # Create HSK 1 Course
        course, created = Course.objects.get_or_create(
            hsk_level=1,
            defaults={
                'title': 'HSK 1 Complete Course',
                'title_zh': 'HSK 1 全部课程',
                'description': 'Complete HSK 1 course with vocabulary and grammar',
                'total_days': 5,  # Reduced for testing
                'order': 0,
                'is_active': True
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created course: {course.title}'))
        else:
            self.stdout.write(self.style.WARNING(f'Course already exists: {course.title}'))

        # Create Course Days
        for day_num in range(1, 6):
            course_day, created = CourseDay.objects.get_or_create(
                course=course,
                day_number=day_num,
                defaults={
                    'title': f'Day {day_num}: Basic Chinese',
                    'title_zh': f'第{day_num}天：基础中文',
                    'description': f'Learning day {day_num}',
                    'estimated_minutes': 15,
                    'order': day_num
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'  Created Day {day_num}'))

                # Create Lesson for each day
                lesson, created = Lesson.objects.get_or_create(
                    course_day=course_day,
                    order=1,
                    defaults={
                        'lesson_type': 'MIXED',
                        'hsk_level': 1,
                        'title': f'Lesson {day_num}: Vocabulary & Grammar',
                        'title_zh': f'第{day_num}课：词汇和语法',
                        'description': f'Lesson content for day {day_num}',
                        'estimated_minutes': 10
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'    Created Lesson'))

        self.stdout.write(self.style.SUCCESS('Course data created successfully!'))
