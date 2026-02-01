import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from course.models import Lesson, LessonStep
from vocab.models import Word
import random

# Create steps for Lessons 3, 4, 5
for lesson_num in [3, 4, 5]:
    lesson = Lesson.objects.filter(id=lesson_num).first()
    if not lesson:
        print(f'Lesson {lesson_num} not found')
        continue
    
    # Check if lesson already has steps
    existing_steps = lesson.steps.count()
    if existing_steps > 0:
        print(f'Lesson {lesson_num} already has {existing_steps} steps')
        continue
    
    print(f'Creating steps for Lesson {lesson_num}...')
    
    # Determine word range (Lesson 1: 1-5, Lesson 2: 6-10, Lesson 3: 11-15, etc.)
    start_word = (lesson_num - 1) * 5 + 1
    end_word = lesson_num * 5
    word_ids = list(range(start_word, end_word + 1))
    words = list(Word.objects.filter(id__in=word_ids))
    
    if len(words) < 5:
        print(f'  Warning: Only found {len(words)} words, need 5')
        if len(words) == 0:
            print(f'  Skipping lesson {lesson_num}')
            continue
    
    # Get all words for distractors
    all_words = list(Word.objects.all())
    
    # Step 1: Vocabulary Introduction
    step1 = LessonStep.objects.create(
        lesson=lesson,
        step_type='VOCAB_INTRO',
        title='New Words',
        order=1,
        estimated_minutes=5,
        content={'instruction': 'Learn these new words', 'words_per_card': 5}
    )
    step1.words.set([w.id for w in words[:5]])
    print(f'  Created Step 1: VOCAB_INTRO')
    
    # Steps 2-4: Vocabulary Recognition
    for i in range(2, 5):
        if i - 2 >= len(words):
            break
        
        word = words[i - 2]
        distractors = [w for w in all_words if w.id != word.id]
        random.shuffle(distractors)
        
        correct_option = 'a'
        options = [
            {'id': 'a', 'text': word.translation_ru},
            {'id': 'b', 'text': distractors[0].translation_ru},
            {'id': 'c', 'text': distractors[1].translation_ru},
            {'id': 'd', 'text': distractors[2].translation_ru},
        ]
        random.shuffle(options)
        
        for opt in options:
            if opt['text'] == word.translation_ru:
                correct_option = opt['id']
                break
        
        step = LessonStep.objects.create(
            lesson=lesson,
            step_type='VOCAB_RECOGNIZE',
            title='Choose Translation',
            order=i,
            estimated_minutes=2,
            content={
                'question': {'hanzi': word.hanzi, 'pinyin': word.pinyin},
                'options': options,
                'correct_answer': correct_option
            }
        )
        step.words.set([word.id])
        print(f'  Created Step {i}: VOCAB_RECOGNIZE (Word ID {word.id})')
    
    # Step 5: Build Phrase
    if len(words) >= 3:
        step5 = LessonStep.objects.create(
            lesson=lesson,
            step_type='BUILD_PHRASE',
            title='Build the Phrase',
            order=5,
            estimated_minutes=3,
            content={
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
        )
        print(f'  Created Step 5: BUILD_PHRASE')
    
    print(f'  Lesson {lesson_num} now has 5 steps\n')

print('Done!')
