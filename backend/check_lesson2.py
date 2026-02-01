import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from course.models import Lesson, LessonStep

# Get Lesson 2
lesson2 = Lesson.objects.filter(id=2).first()
if lesson2:
    print(f'Lesson 2: {lesson2.title}')
    steps = lesson2.steps.all().order_by('order')
    print(f'Steps count: {steps.count()}')
    for s in steps:
        words = s.words.all()
        print(f'  Step {s.order}: {s.step_type} - {s.title}')
        print(f'    Words: {words.count()} - {list(words.values_list("id", flat=True))}')
else:
    print('Lesson 2 not found')
