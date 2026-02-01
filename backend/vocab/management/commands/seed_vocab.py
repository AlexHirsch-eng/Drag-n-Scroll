"""
Management command to seed initial vocabulary data
"""
from django.core.management.base import BaseCommand
from vocab.models import Word


class Command(BaseCommand):
    help = 'Create initial vocabulary data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating vocabulary data...')

        # HSK 1 words
        words_data = [
            # Numbers
            {'hanzi': '一', 'pinyin': 'yī', 'ru': 'один', 'kz': 'бір', 'hsk': 1},
            {'hanzi': '二', 'pinyin': 'èr', 'ru': 'два', 'kz': 'екі', 'hsk': 1},
            {'hanzi': '三', 'pinyin': 'sān', 'ru': 'три', 'kz': 'үш', 'hsk': 1},
            {'hanzi': '四', 'pinyin': 'sì', 'ru': 'четыре', 'kz': 'төрт', 'hsk': 1},
            {'hanzi': '五', 'pinyin': 'wǔ', 'ru': 'пять', 'kz': 'бес', 'hsk': 1},
            {'hanzi': '六', 'pinyin': 'liù', 'ru': 'шесть', 'kz': 'алты', 'hsk': 1},
            {'hanzi': '七', 'pinyin': 'qī', 'ru': 'семь', 'kz': 'жеті', 'hsk': 1},
            {'hanzi': '八', 'pinyin': 'bā', 'ru': 'восемь', 'kz': 'сегіз', 'hsk': 1},
            {'hanzi': '九', 'pinyin': 'jiǔ', 'ru': 'девять', 'kz': 'тоғыз', 'hsk': 1},
            {'hanzi': '十', 'pinyin': 'shí', 'ru': 'десять', 'kz': 'он', 'hsk': 1},

            # Greetings
            {'hanzi': '你好', 'pinyin': 'nǐ hǎo', 'ru': 'привет', 'kz': 'сәлем', 'hsk': 1},
            {'hanzi': '再见', 'pinyin': 'zài jiàn', 'ru': 'до свидания', 'kz': 'сау бол', 'hsk': 1},

            # Common verbs
            {'hanzi': '是', 'pinyin': 'shì', 'ru': 'быть', 'kz': 'болу', 'hsk': 1},
            {'hanzi': '有', 'pinyin': 'yǒu', 'ru': 'иметь', 'kz': 'ие болу', 'hsk': 1},
            {'hanzi': '在', 'pinyin': 'zài', 'ru': 'находиться в', 'kz': 'болу', 'hsk': 1},
            {'hanzi': '去', 'pinyin': 'qù', 'ru': 'идти', 'kz': 'бару', 'hsk': 1},
            {'hanzi': '来', 'pinyin': 'lái', 'ru': 'приходить', 'kz': 'келу', 'hsk': 1},
            {'hanzi': '吃', 'pinyin': 'chī', 'ru': 'есть', 'kz': 'жеу', 'hsk': 1},
            {'hanzi': '喝', 'pinyin': 'hē', 'ru': 'пить', 'kz': 'ішу', 'hsk': 1},
            {'hanzi': '说', 'pinyin': 'shuō', 'ru': 'говорить', 'kz': 'айту', 'hsk': 1},
            {'hanzi': '看', 'pinyin': 'kàn', 'ru': 'смотреть', 'kz': 'қарау', 'hsk': 1},

            # Pronouns
            {'hanzi': '我', 'pinyin': 'wǒ', 'ru': 'я', 'kz': 'мен', 'hsk': 1},
            {'hanzi': '你', 'pinyin': 'nǐ', 'ru': 'ты', 'kz': 'сен', 'hsk': 1},
            {'hanzi': '他', 'pinyin': 'tā', 'ru': 'он', 'kz': 'ол', 'hsk': 1},
            {'hanzi': '她', 'pinyin': 'tā', 'ru': 'она', 'kz': 'ол', 'hsk': 1},
            {'hanzi': '我们', 'pinyin': 'wǒ men', 'ru': 'мы', 'kz': 'біз', 'hsk': 1},
            {'hanzi': '你们', 'pinyin': 'nǐ men', 'ru': 'вы', 'kz': 'сендер', 'hsk': 1},
            {'hanzi': '他们', 'pinyin': 'tā men', 'ru': 'они', 'kz': 'олар', 'hsk': 1},

            # Common nouns
            {'hanzi': '人', 'pinyin': 'rén', 'ru': 'человек', 'kz': 'адам', 'hsk': 1},
            {'hanzi': '中国', 'pinyin': 'Zhōng guó', 'ru': 'Китай', 'kz': 'Қытай', 'hsk': 1},
            {'hanzi': '中国话', 'pinyin': 'Zhōng guó huà', 'ru': 'китайский язык', 'kz': 'қытай тілі', 'hsk': 1},
            {'hanzi': '朋友', 'pinyin': 'péng you', 'ru': 'друг', 'kz': 'дос', 'hsk': 1},
            {'hanzi': '家', 'pinyin': 'jiā', 'ru': 'дом/семья', 'kz': 'үй/отбасы', 'hsk': 1},
            {'hanzi': '名字', 'pinyin': 'míng zi', 'ru': 'имя', 'kz': 'есім', 'hsk': 1},
            {'hanzi': '学生', 'pinyin': 'xué sheng', 'ru': 'студент', 'kz': 'студент', 'hsk': 1},
            {'hanzi': '老师', 'pinyin': 'lǎo shī', 'ru': 'учитель', 'kz': 'мұғалім', 'hsk': 1},
        ]

        created_count = 0
        for word_data in words_data:
            word, created = Word.objects.get_or_create(
                hanzi=word_data['hanzi'],
                defaults={
                    'pinyin': word_data['pinyin'],
                    'translation_ru': word_data['ru'],
                    'translation_kz': word_data['kz'],
                    'hsk_level': word_data['hsk'],
                    'part_of_speech': 'other',
                    'frequency_rank': created_count + 1
                }
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Created {created_count} words successfully!'))
