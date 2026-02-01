import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from vocab.models import Word

# HSK 1 Words (most basic)
hsk1_words = [
    ('你好', 'nǐ hǎo', 'Привет', 'Сәлем', 'noun'),
    ('我', 'wǒ', 'Я', 'Мен', 'pronoun'),
    ('你', 'nǐ', 'Ты', 'Сен', 'pronoun'),
    ('他', 'tā', 'Он', 'Ол', 'pronoun'),
    ('她', 'tā', 'Она', 'Ол', 'pronoun'),
    ('好', 'hǎo', 'Хороший', 'Жақсы', 'adjective'),
    ('的', 'de', 'Частица', 'Жұрнақ', 'particle'),
    ('不', 'bù', 'Не', 'Жоқ', 'adverb'),
    ('是', 'shì', 'Быть', 'Болу', 'verb'),
    ('在', 'zài', 'Находиться', 'Бару', 'verb'),
    ('有', 'yǒu', 'Иметь', 'Иеу', 'verb'),
    ('人', 'rén', 'Человек', 'Адам', 'noun'),
    ('中国', 'Zhōngguó', 'Китай', 'Қытай', 'noun'),
    ('大', 'dà', 'Большой', 'Үлкен', 'adjective'),
    ('小', 'xiǎo', 'Маленький', 'Кішкентай', 'adjective'),
]

# HSK 2 Words (elementary)
hsk2_words = [
    ('什么', 'shénme', 'Что', 'Не', 'pronoun'),
    ('时候', 'shíhou', 'Когда', 'Қашан', 'noun'),
    ('可以', 'kěyǐ', 'Мочь', 'Ала', 'verb'),
    ('这', 'zhè', 'Это', 'Бұл', 'pronoun'),
    ('那', 'nà', 'То', 'Со', 'pronoun'),
    ('个', 'gè', 'Счётное слово', 'Сан есім', 'measure'),
    ('吗', 'ma', 'Вопросительная частица', 'Сұрақ', 'particle'),
    ('呢', 'ne', 'Частица', 'Жұрнақ', 'particle'),
    ('都', 'dōu', 'Все', 'Барлық', 'adverb'),
    ('也', 'yě', 'Тоже', 'Да', 'adverb'),
    ('很', 'hěn', 'Очень', 'Тым', 'adverb'),
    ('还', 'hái', 'Ещё', 'Әлі', 'adverb'),
    ('就', 'jiù', 'Тогда', 'Сол кезде', 'conjunction'),
    ('吃', 'chī', 'Есть', 'Жеу', 'verb'),
    ('喝', 'hē', 'Пить', 'Ішу', 'verb'),
]

# HSK 3 Words (intermediate)
hsk3_words = [
    ('所以', 'suǒyǐ', 'Поэтому', 'Сондықтан', 'conjunction'),
    ('因为', 'yīnwèi', 'Потому что', 'Себебі', 'conjunction'),
    ('但是', 'dànshì', 'Но', 'Бірақ', 'conjunction'),
    ('如果', 'rúguǒ', 'Если', 'Егер', 'conjunction'),
    ('觉得', 'juéde', 'Думать', 'Ойлау', 'verb'),
    ('开始', 'kāishǐ', 'Начинать', 'Бастау', 'verb'),
    ('结束', 'jiéshù', 'Заканчивать', 'Аяқтау', 'verb'),
    ('已经', 'yǐjīng', 'Уже', 'У...', 'adverb'),
    ('正在', 'zhèngzài', 'В данный момент', 'Қазір', 'adverb'),
    ('喜欢', 'xǐhuan', 'Нравиться', 'Ұнайту', 'verb'),
    ('希望', 'xīwàng', 'Надежаться', 'Үміт', 'verb'),
    ('应该', 'yīnggāi', 'Должен', 'Тиісті', 'verb'),
    ('需要', 'xūyào', 'Нужен', 'Керек', 'verb'),
    ('知道', 'zhīdao', 'Знать', 'Білу', 'verb'),
    ('认识', 'rènshi', 'Знакомиться', 'Танысу', 'verb'),
]

# HSK 4 Words (upper intermediate)
hsk4_words = [
    ('提高', 'tígāo', 'Повышать', 'Жоғарылату', 'verb'),
    ('发展', 'fāzhǎn', 'Развиваться', 'Дамыту', 'verb'),
    ('经济', 'jīngjì', 'Экономика', 'Экономика', 'noun'),
    ('文化', 'wénhuà', 'Культура', 'Мәдениет', 'noun'),
    ('社会', 'shèhuì', 'Общество', 'Қоғам', 'noun'),
    ('影响', 'yǐngxiǎng', 'Влиять', 'Әсер ету', 'verb'),
    ('经验', 'jīngyàn', 'Опыт', 'Тәжірибе', 'noun'),
    ('情况', 'qíngkuàng', 'Ситуация', 'Жағдай', 'noun'),
    ('虽然', 'suīrán', 'Хотя', 'Хотя', 'conjunction'),
    ('即使', 'jíshǐ', 'Даже если', 'Еш', 'conjunction'),
    ('为了', 'wèile', 'Ради', 'Үшін', 'preposition'),
    ('通过', 'tōngguò', 'Через', 'Арқылы', 'preposition'),
    ('或者', 'huòzhě', 'Или', 'Немесе', 'conjunction'),
    ('除了', 'chúle', 'Кроме', 'Қоспағанда', 'preposition'),
    ('继续', 'jìxù', 'Продолжать', 'Жалғастыру', 'verb'),
]

# HSK 5 Words (advanced)
hsk5_words = [
    ('建立', 'jiànlì', 'Создавать', 'Құру', 'verb'),
    ('实现', 'shíxiàn', 'Осуществлять', 'Жүзеге асыру', 'verb'),
    ('政策', 'zhèngcè', 'Политика', 'Саясат', 'noun'),
    ('环境', 'huánjìng', 'Окружающая среда', 'Қоршаған орта', 'noun'),
    ('技术', 'jìshù', 'Технология', 'Технология', 'noun'),
    ('成功', 'chénggōng', 'Успех', 'Сәттілік', 'noun'),
    ('准备', 'zhǔnbèi', 'Готовиться', 'Дайындау', 'verb'),
    ('举办', 'jǔbàn', 'Проводить', 'Өткізу', 'verb'),
    ('参加', 'cānjiā', 'Участвовать', 'Қатысу', 'verb'),
    ('获得', 'huòdé', 'Получать', 'Алу', 'verb'),
    ('缺乏', 'quēfá', 'Нехватать', 'жетіспеу', 'verb'),
    ('无论', 'wúlùn', 'Неважно', 'Ешқандай', 'conjunction'),
    ('尽管', 'jǐnguǎn', 'Несмотря на', 'Қарамастан', 'conjunction'),
    ('假如', 'jiǎrú', 'Если', 'Егер', 'conjunction'),
    ('万一', 'wànyī', 'В случае если', 'Егер', 'conjunction'),
]

# HSK 6 Words (proficient)
hsk6_words = [
    ('确实', 'quèshí', 'Действительно', 'Рас', 'adverb'),
    ('予以', 'yǔyǐ', 'Оказать', 'Беру', 'verb'),
    ('亟待', 'jídài', 'Срочно нуждаться', 'Күткілт', 'verb'),
    ('采取', 'cǎiqǔ', 'Принять', 'Қабылдау', 'verb'),
    ('措施', 'cuòshī', 'Мера', 'Шара', 'noun'),
    ('巨大', 'jùdà', 'Огромный', 'Орасан зор', 'adjective'),
    ('日益', 'rìyì', 'С каждым днём', 'Күн санап', 'adverb'),
    ('增强', 'zēngqiáng', 'Усилять', 'Күшейту', 'verb'),
    ('改进', 'gǎijìn', 'Улучшать', 'Жақсарту', 'verb'),
    ('完善', 'wánshàn', 'Совершенствовать', 'Камилдау', 'verb'),
    ('推动', 'tuīdòng', 'Продвигать', 'Итерлеу', 'verb'),
    ('促进', 'cùjìn', 'Способствовать', 'Жетелдіру', 'verb'),
    ('以至于', 'yǐzhìyú', 'До того что', 'Дейін', 'conjunction'),
    ('岂不是', 'qǐbúshì', 'Разве не', 'Айта', 'conjunction'),
    ('不妨', 'bùfáng', 'Не вредно', 'Болмайды', 'adverb'),
]

# All HSK levels data
hsk_data = [
    (1, hsk1_words),
    (2, hsk2_words),
    (3, hsk3_words),
    (4, hsk4_words),
    (5, hsk5_words),
    (6, hsk6_words),
]

total_added = 0
for hsk_level, words in hsk_data:
    print(f'\n=== Adding HSK {hsk_level} words ===')

    for hanzi, pinyin, ru, kz, pos in words:
        # Check if word already exists
        existing = Word.objects.filter(hanzi=hanzi, pinyin=pinyin).first()
        if existing:
            print(f'  Skipped (exists): ID {existing.id}')
            continue

        # Create word
        word = Word.objects.create(
            hanzi=hanzi,
            pinyin=pinyin,
            translation_ru=ru,
            translation_kz=kz,
            hsk_level=hsk_level,
            part_of_speech=pos,
            frequency_rank=hsk_level * 100
        )
        total_added += 1
        print(f'  Added: ID {word.id}')

    # Count for this level
    count = Word.objects.filter(hsk_level=hsk_level).count()
    print(f'  Total HSK {hsk_level} words: {count}')

print(f'\n=== Summary ===')
print(f'Total words added: {total_added}')
print(f'Total words in database: {Word.objects.count()}')
print('\nDone!')
