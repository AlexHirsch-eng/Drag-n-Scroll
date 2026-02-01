import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from course.models import Lesson, LessonStep
from vocab.models import GrammarRule

# Get Lesson 2
lesson2 = Lesson.objects.filter(id=2).first()
if not lesson2:
    print('Lesson 2 not found')
    exit(1)

# Get grammar rule
grammar_rule = GrammarRule.objects.filter(id=3).first()
if not grammar_rule:
    print('Grammar rule not found')
    exit(1)

# Add GRAMMAR_INTRO step as Step 6
step6 = LessonStep.objects.create(
    lesson=lesson2,
    step_type='GRAMMAR_INTRO',
    title='Grammar: Wo zai + Place',
    order=6,
    estimated_minutes=5,
    content={
        'title': 'Wo Zai + Place + Action',
        'pattern': 'S + zai + Place + V',
        'explanation_ru': 'Form: Wo zai + Place + V. Translation: "Ya v ... (i) ..."',
        'explanation_kz': 'Form: Wo zai + Place + V. Translation: "Men ... (da) ..."'
    }
)
step6.grammar_rules.set([grammar_rule.id])
print(f'Created Step 6: GRAMMAR_INTRO')

# Update Step 5 (BUILD_PHRASE) with proper exercise
step5 = LessonStep.objects.filter(lesson=lesson2, order=5).first()
if step5:
    step5.content = {
        'instruction_ru': 'Sobrate: Ya v restorane yem',
        'instruction_kz': 'Zhigin: Men meiramhanada zhumin',
        'target_hanzi': 'wo zai fan dian chi fan',
        'target_pinyin': 'wo zai fan dian chi fan',
        'target_translation': 'Ya v restorane yem',
        'words': [
            {'id': 1, 'hanzi': 'wo', 'pinyin': 'wo', 'translation': 'Ya'},
            {'id': 2, 'hanzi': 'zai', 'pinyin': 'zai', 'translation': 'v'},
            {'id': 3, 'hanzi': 'fan', 'pinyin': 'fan', 'translation': 'restoran'},
            {'id': 4, 'hanzi': 'dian', 'pinyin': 'dian', 'translation': '-'},
            {'id': 5, 'hanzi': 'chi', 'pinyin': 'chi', 'translation': 'yem'},
            {'id': 6, 'hanzi': 'fan', 'pinyin': 'fan', 'translation': 'edy'}
        ],
        'correct_order': [1, 2, 3, 4, 5, 6],
        'hint': 'Ya v restorane (i) yem'
    }
    step5.save()
    print('Updated Step 5: BUILD_PHRASE with grammar exercise')

# Show lesson steps
steps = lesson2.steps.all().order_by('order')
print(f'\nLesson 2 now has {steps.count()} steps:')
for s in steps:
    print(f'  Step {s.order}: {s.step_type} - {s.title}')

print('\nDone!')
