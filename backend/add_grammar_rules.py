import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from vocab.models import GrammarRule, GrammarExample, Word
from course.models import Lesson, LessonStep

# Create GrammarRule: wo zai + place + action
rule = GrammarRule.objects.create(
    title='Wo Zai + Place + Action',
    pattern='S + zai + Place + V',
    hsk_level=1,
    explanation_ru='Form: Wo zai + Place + V. Translation: "Ya v ... (i) ..."',
    explanation_kz='Form: Wo zai + Place + V. Translation: "Men ... (da) ..."'
)

# Create examples with ASCII-safe content
examples_data = [
    {
        'hanzi': 'wo zai fan dian chi fan',
        'pinyin': 'wo zai fan dian chi fan',
        'ru': 'Ya v restorane yem',
        'kz': 'Men meiramhanada',
        'words': ['wo', 'zai', 'fan', 'dian', 'chi', 'fan']
    },
    {
        'hanzi': 'wo zai jia',
        'pinyin': 'wo zai jia',
        'ru': 'Ya doma',
        'kz': 'Men uyde',
        'words': ['wo', 'zai', 'jia']
    },
    {
        'hanzi': 'wo zai xue xiao xue xi',
        'pinyin': 'wo zai xue xiao xue xi',
        'ru': 'Ya v shkole uchus',
        'kz': 'Men mektepte okymyn',
        'words': ['wo', 'zai', 'xue', 'xiao', 'xue', 'xi']
    },
    {
        'hanzi': 'ta zai gong yuan pao bu',
        'pinyin': 'ta zai gong yuan pao bu',
        'ru': 'On v parke begaet',
        'kz': 'Ol saybakta zhygiredi',
        'words': ['ta', 'zai', 'gong', 'yuan', 'pao', 'bu']
    },
    {
        'hanzi': 'ta zai gong si gong zuo',
        'pinyin': 'ta zai gong si gong zuo',
        'ru': 'Ona na rabote',
        'kz': 'Ol kompaniyda zhumis isteydi',
        'words': ['ta', 'zai', 'gong', 'si', 'gong', 'zuo']
    },
]

print('Rule ID:', rule.id)

for i, ex_data in enumerate(examples_data):
    example = GrammarExample.objects.create(
        grammar_rule=rule,
        sentence_hanzi=ex_data['hanzi'],
        sentence_pinyin=ex_data['pinyin'],
        translation_ru=ex_data['ru'],
        translation_kz=ex_data['kz'],
        order=i + 1
    )

    # Add words to example
    for word_pinyin in ex_data['words']:
        words = Word.objects.filter(pinyin__icontains=word_pinyin)
        if words.exists():
            example.word_examples.add(words.first())

    print(f'  Example {i + 1}: ID {example.id}')

print(f'Total examples: {rule.examples.count()}')
print('Done!')
