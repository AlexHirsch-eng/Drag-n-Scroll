import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from course.models import Lesson, LessonStep
from vocab.models import Word
import random

# Get Lesson 2
lesson2 = Lesson.objects.filter(id=2).first()
if not lesson2:
    print('Lesson 2 not found!')
    exit(1)

# Get all available words for distractors
all_words = list(Word.objects.all())
words_6_10 = list(Word.objects.filter(id__in=[6, 7, 8, 9, 10]))

print('Lesson 2: Vocabulary & Grammar')
print(f'Available words: {len(all_words)}')

# Get steps
steps = lesson2.steps.all().order_by('order')

# Update Step 2 - Word 6
step2 = steps.filter(order=2).first()
if step2:
    word = words_6_10[0]  # ID 6
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
    
    # Find which option has the correct answer
    for opt in options:
        if opt['text'] == word.translation_ru:
            correct_option = opt['id']
            break
    
    step2.content = {
        'question': {
            'hanzi': word.hanzi,
            'pinyin': word.pinyin
        },
        'options': options,
        'correct_answer': correct_option
    }
    step2.words.set([word.id])
    step2.save()
    print(f'\nStep 2 updated: Word ID {word.id}')
    print(f'  Correct: {word.translation_ru}')

# Update Step 3 - Word 7
step3 = steps.filter(order=3).first()
if step3:
    word = words_6_10[1]  # ID 7
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
    
    step3.content = {
        'question': {
            'hanzi': word.hanzi,
            'pinyin': word.pinyin
        },
        'options': options,
        'correct_answer': correct_option
    }
    step3.words.set([word.id])
    step3.save()
    print(f'\nStep 3 updated: Word ID {word.id}')
    print(f'  Correct: {word.translation_ru}')

# Update Step 4 - Word 8
step4 = steps.filter(order=4).first()
if step4:
    word = words_6_10[2]  # ID 8
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
    
    step4.content = {
        'question': {
            'hanzi': word.hanzi,
            'pinyin': word.pinyin
        },
        'options': options,
        'correct_answer': correct_option
    }
    step4.words.set([word.id])
    step4.save()
    print(f'\nStep 4 updated: Word ID {word.id}')
    print(f'  Correct: {word.translation_ru}')

# Update Step 5 - BUILD_PHRASE with Word 9
step5 = steps.filter(order=5).first()
if step5:
    words = words_6_10[3:4]  # ID 9
    step5.words.set(words)
    
    # For BUILD_PHRASE, we need a target phrase and word options
    word = words[0]
    step5.content = {
        'instruction': f'Build the phrase using the word',
        'target_phrase': '',
        'correct_order': [word.id],
        'words': [
            {
                'id': word.id,
                'hanzi': word.hanzi,
                'pinyin': word.pinyin,
                'translation_ru': word.translation_ru
            }
        ]
    }
    step5.save()
    print(f'\nStep 5 updated: BUILD_PHRASE with Word ID {word.id}')

print('\nAll steps updated successfully!')
