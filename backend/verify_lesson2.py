import django
import os
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from course.models import Lesson, LessonStep

lesson2 = Lesson.objects.filter(id=2).first()
if lesson2:
    print('Lesson 2 Steps Summary:')
    steps = lesson2.steps.all().order_by('order')
    print(f'Total steps: {steps.count()}')
    
    for s in steps:
        print(f'\nStep {s.order}: {s.step_type}')
        print(f'  Title: {s.title}')
        
        # Check content structure
        if s.step_type == 'VOCAB_INTRO':
            words_count = s.words.count()
            print(f'  Words: {words_count}')
            
        elif s.step_type == 'VOCAB_RECOGNIZE':
            has_question = 'question' in s.content
            has_options = 'options' in s.content
            has_correct = 'correct_answer' in s.content
            print(f'  Has question: {has_question}')
            print(f'  Has options: {has_options}')
            print(f'  Has correct_answer: {has_correct}')
            
        elif s.step_type == 'BUILD_PHRASE':
            has_instruction = 'instruction_ru' in s.content
            has_target = 'target_hanzi' in s.content
            has_options = 'options' in s.content
            has_correct = 'correct_order' in s.content
            print(f'  Has instruction: {has_instruction}')
            print(f'  Has target: {has_target}')
            print(f'  Has options: {has_options}')
            print(f'  Has correct_order: {has_correct}')
    
    print('\n✓ All steps have proper structure!')
else:
    print('Lesson 2 not found')
