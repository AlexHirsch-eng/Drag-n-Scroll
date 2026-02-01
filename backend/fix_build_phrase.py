import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from course.models import LessonStep

# Get BUILD_PHRASE step (Step 5)
step5 = LessonStep.objects.filter(order=5, lesson__id=2).first()
if step5:
    # Simple phrase build with one word
    step5.content = {
        'instruction_ru': 'Соберите фразу',
        'instruction_kz': 'Фразаны жиыңыз',
        'target_hanzi': '你好',
        'target_pinyin': 'nǐ hǎo',
        'options': [
            {'id': 1, 'hanzi': '你'},
            {'id': 2, 'hanzi': '好'}
        ],
        'correct_order': [1, 2]
    }
    step5.save()
    print('BUILD_PHRASE step updated successfully')
    print(f'Step 5 content: {step5.content}')
else:
    print('Step 5 not found')
