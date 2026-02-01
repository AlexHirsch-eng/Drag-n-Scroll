import django
import os
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from course.models import Lesson
from learning.views import lesson_steps

# Mock request object
class MockRequest:
    def __init__(self, user_id=1):
        self.user_id = user_id
        self.query_params = {'lesson_id': '2'}
    
    def get(self, key, default=None):
        return self.query_params.get(key, default)

# Get lesson
lesson = Lesson.objects.filter(id=2).first()
if lesson:
    steps = lesson.steps.all().order_by('order')
    
    print('Lesson 2 steps:')
    for s in steps:
        print(f'\nStep {s.order}: {s.step_type}')
        
        # Simulate API response for grammar step
        if s.step_type == 'GRAMMAR_INTRO':
            rules = s.grammar_rules.all()
            print(f'  Grammar rules: {rules.count()}')
            for r in rules:
                print(f'    Rule: {r.title}')
                print(f'    Pattern: {r.pattern}')
                examples = r.examples.all()
                print(f'    Examples: {examples.count()}')
                for ex in examples[:3]:
                    print(f'      - {ex.sentence_hanzi[:30]}...')

# Check content for BUILD_PHRASE
step5 = lesson.steps.filter(order=5).first()
if step5:
    print(f'\n\nBUILD_PHRASE Step 5 content:')
    print(json.dumps(step5.content, indent=2, ensure_ascii=False))

print('\nDone!')
