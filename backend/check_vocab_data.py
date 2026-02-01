import django
import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from vocab.models import Word, GrammarRule

# Check available words
words = Word.objects.all()
print(f'Total words: {words.count()}')
print('\nFirst 10 words (ID and translation):')
for w in words[:10]:
    print(f'  ID {w.id}: {w.translation_ru} (HSK {w.hsk_level})')

# Check grammar rules
rules = GrammarRule.objects.all()
print(f'\nTotal grammar rules: {rules.count()}')
for r in rules[:10]:
    print(f'  ID {r.id}: {r.title} (HSK {r.hsk_level})')
