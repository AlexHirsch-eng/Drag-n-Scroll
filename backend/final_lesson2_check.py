import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from course.models import Lesson

lesson2 = Lesson.objects.filter(id=2).first()
steps = lesson2.steps.all().order_by('order')

print('=== Lesson 2 Final Structure ===\n')
for s in steps:
    print(f'Step {s.order}: {s.step_type} - {s.title}')
    
    if s.step_type == 'GRAMMAR_INTRO':
        rules = s.grammar_rules.all()
        print(f'  Grammar rules: {rules.count()}')
        for r in rules:
            print(f'    - {r.pattern}')
            ex_count = r.examples.count()
            print(f'    Examples: {ex_count}')
    
    elif s.step_type == 'BUILD_PHRASE':
        content = s.content
        if 'words' in content:
            print(f'  Phrase building exercise')
            print(f'  Target: {content.get("target_hanzi", "")}')
            print(f'  Words: {len(content.get("words", []))}')

print('\n=== Ready for Learning! ===')
