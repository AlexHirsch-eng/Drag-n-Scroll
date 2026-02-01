import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from course.models import Lesson, LessonStep

# Get Lesson 1
lesson1 = Lesson.objects.filter(id=1).first()
if lesson1:
    print(f'Lesson 1: {lesson1.title}')
    steps = lesson1.steps.all().order_by('order')
    for s in steps:
        print(f'\n  Step {s.order}: {s.step_type} - {s.title}')
        words = s.words.all()
        print(f'    Words: {words.count()}')
        for w in words:
            print(f'      ID {w.id}')
