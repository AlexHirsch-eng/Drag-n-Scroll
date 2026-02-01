import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from course.models import Lesson, LessonStep

# Get all lessons with their steps
lessons = Lesson.objects.all()
for l in lessons:
    steps = l.steps.all().order_by('order')
    print(f'\nLesson {l.id}: {l.title}')
    print(f'  Steps count: {steps.count()}')
    for s in steps:
        print(f'    Step {s.order}: {s.step_type} - {s.title}')
