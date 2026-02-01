"""
Django management command to populate video data with diverse content
Run: python manage.py populate_videos
"""

import sys
import io
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta, datetime
from video_app.models import (
    VideoCategory, Video, VideoView, VideoLike, VideoBookmark,
    VideoComment, VideoCommentLike, VideoShare, VideoHashtag, UserFollowing
)

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate video database with diverse content'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting video population...'))

        # Get or create users
        users_data = [
            {'username': 'xiaoming_teacher', 'email': 'xiaoming_t@example.com', 'first_name': 'Xiao', 'last_name': 'Ming'},
            {'username': 'mei_ling', 'email': 'mei_l@example.com', 'first_name': 'Mei', 'last_name': 'Ling'},
            {'username': 'wang_wei', 'email': 'wang_w@example.com', 'first_name': 'Wang', 'last_name': 'Wei'},
            {'username': 'li_hua', 'email': 'lihua_l@example.com', 'first_name': 'Li', 'last_name': 'Hua'},
            {'username': 'zhang_le', 'email': 'zhang_z@example.com', 'first_name': 'Zhang', 'last_name': 'Le'},
        ]

        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                }
            )
            users.append(user)
            if created:
                self.stdout.write(f'  Created user: {user.username}')

        # Get or create categories
        categories_data = [
            {'name': 'Vocabulary', 'icon': '📚', 'description': 'Learn new words and phrases', 'order': 1},
            {'name': 'Grammar', 'icon': '📝', 'description': 'Grammar explanations and examples', 'order': 2},
            {'name': 'Culture', 'icon': '🏮', 'description': 'Chinese culture and traditions', 'order': 3},
            {'name': 'Listening', 'icon': '🎧', 'description': 'Listening practice exercises', 'order': 4},
            {'name': 'Speaking', 'icon': '🗣️', 'description': 'Speaking and pronunciation tips', 'order': 5},
            {'name': 'Writing', 'icon': '✍️', 'description': 'Chinese writing and characters', 'order': 6},
            {'name': 'Tips', 'icon': '💡', 'description': 'Learning tips and strategies', 'order': 7},
        ]

        categories = []
        for cat_data in categories_data:
            cat, created = VideoCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories.append(cat)

        # Create diverse videos
        videos_data = [
            # HSK 3 Vocabulary videos
            {
                'creator': 'xiaoming_teacher',
                'category': 'Vocabulary',
                'title': 'HSK 3 Unit 1: Daily Routine Vocabulary',
                'description': 'Learn essential words for daily routines! 每天、起床、睡觉、吃饭. Master these 10 HSK 3 vocabulary words with examples and pronunciation. Perfect for beginners! 学习日常生活的必备词汇！',
                'tags': ['#hsk3', '#vocabulary', '#daily', '#chinese', '#beginner'],
                'duration': 45,
                'lesson_number': 1,
                'lesson_words': ['每天', '起床', '睡觉', '吃饭', '喝水', '运动', '工作', '学习', '休息'],
                'music': 'Upbeat Learning Beat',
            },
            {
                'creator': 'mei_ling',
                'category': 'Vocabulary',
                'title': 'Food Vocabulary in Chinese',
                'description': 'Learn to talk about food! 饺子、面条、米饭. Order at restaurants like a local! HSK 3 vocabulary. Let me know your favorite Chinese dish! 学习食物词汇！在餐厅点菜像本地人！',
                'tags': ['#vocabulary', '#food', '#restaurant', '#hsk3', '#practical'],
                'duration': 52,
                'lesson_number': 2,
                'lesson_words': ['饺子', '面条', '米饭', '包子', '豆腐', '蔬菜', '水果', '鸡肉', '牛肉'],
                'music': 'Happy Chinese Tune',
            },
            {
                'creator': 'wang_wei',
                'category': 'Vocabulary',
                'title': 'Weather Words in Chinese',
                'description': 'Talk about the weather! 下雨、晴天、刮风. Essential HSK 3 vocabulary for everyday conversations. What is the weather like today? 谈论天气！日常对话必备词汇。',
                'tags': ['#vocabulary', '#weather', '#hsk3', '#conversation', '#daily'],
                'duration': 38,
                'lesson_number': 3,
                'lesson_words': ['下雨', '晴天', '刮风', '下雪', '多云', '热', '冷', '温暖', '凉快'],
                'music': 'Weather Vibes',
            },
            # Grammar videos
            {
                'creator': 'mei_ling',
                'category': 'Grammar',
                'title': 'Master the 把 (bǎ) Structure',
                'description': 'The 把 structure explained simply! 把书给我、把门关上. Learn one of the most important Chinese grammar patterns. With clear examples and practice sentences. Have you mastered this? 把字句详解！最重要的中文语法之一。',
                'tags': ['#grammar', '#把structure', '#intermediate', '#sentencestructure', '#explain'],
                'duration': 68,
                'lesson_number': 10,
                'lesson_words': ['把', '给', '放在', '拿来', '带去'],
                'music': 'Grammar Groove',
            },
            {
                'creator': 'xiaoming_teacher',
                'category': 'Grammar',
                'title': 'Using 被 (bèi) for Passive Voice',
                'description': 'Learn the passive voice! 我的钱包被偷了. 被字句讲解. Essential for HSK 4 and above. Examples and common mistakes to avoid. 被动语态讲解！HSK4必备。',
                'tags': ['#grammar', '#passive', '#被', '#hsk4', '#advanced'],
                'duration': 72,
                'lesson_number': 15,
                'lesson_words': ['被', '偷', '打破', '找到', '看见'],
                'music': 'Passive Flow',
            },
            {
                'creator': 'li_hua',
                'category': 'Grammar',
                'title': 'Chinese Question Words Explained',
                'description': 'Master question words! 什么、谁、哪里、什么时候、为什么. Form questions like a native speaker. Essential for everyday conversations! 疑问词详解！像本地人一样提问。',
                'tags': ['#grammar', '#questions', '#hsk3', '#basics', '#conversation'],
                'duration': 55,
                'lesson_number': 8,
                'lesson_words': ['什么', '谁', '哪里', '什么时候', '为什么', '怎么', '多少'],
                'music': 'Question Time',
            },
            # Culture videos
            {
                'creator': 'xiaoming_teacher',
                'category': 'Culture',
                'title': 'Chinese New Year Traditions',
                'description': 'Discover Spring Festival! 🧧 红包、饺子、舞龙. Learn about the most important Chinese holiday. Traditions, food, and customs. Do you celebrate Chinese New Year? 春节传统！最重要的中国节日。',
                'tags': ['#culture', '#chinesenewyear', '#springfestival', '#traditions', '#春节'],
                'duration': 95,
                'lesson_words': ['春节', '红包', '饺子', '烟花', '舞龙', '团圆'],
                'music': 'Traditional Festival',
            },
            {
                'creator': 'mei_ling',
                'category': 'Culture',
                'title': 'Chinese Tea Culture 🍵',
                'description': 'Explore the art of Chinese tea! 茶道、功夫茶、龙井. History, types of tea, and tea ceremonies. What is your favorite tea? 中国茶文化！茶的艺术。',
                'tags': ['#culture', '#tea', '#茶道', '#traditions', '#lifestyle'],
                'duration': 82,
                'lesson_words': ['茶', '绿茶', '红茶', '乌龙茶', '功夫茶', '龙井'],
                'music': 'Zen Tea Music',
            },
            {
                'creator': 'zhang_le',
                'category': 'Culture',
                'title': 'Chinese Table Manners',
                'description': 'Dining etiquette in China! 筷子、敬酒、座次. How to behave at formal dinners. Impress your Chinese friends! 中国餐桌礼仪！正式宴会注意事项。',
                'tags': ['#culture', '#etiquette', '#dining', '#manners', '#customs'],
                'duration': 76,
                'lesson_words': ['筷子', '敬酒', '座位', '长辈', '礼貌'],
                'music': 'Dinner Ambience',
            },
            # Listening videos
            {
                'creator': 'wang_wei',
                'category': 'Listening',
                'title': 'Listening Practice: At the Restaurant',
                'description': 'Real-life conversation practice! Ordering food, asking for the bill, making requests. HSK 3 level. Listen and repeat. Can you understand? 听力练习：在餐厅。真实对话练习！',
                'tags': ['#listening', '#restaurant', '#practice', '#hsk3', '#realconversation'],
                'duration': 88,
                'lesson_number': 5,
                'lesson_words': ['菜单', '点菜', '服务员', '结账', '打包'],
                'music': 'Restaurant Background',
            },
            {
                'creator': 'li_hua',
                'category': 'Listening',
                'title': 'Chinese Numbers Practice',
                'description': 'Master Chinese numbers! 一、二、三...百、千、万. Phone numbers, prices, dates. Essential listening practice. Repeat after me! 中文数字练习！电话号码、价格、日期。',
                'tags': ['#listening', '#numbers', '#basics', '#practice', '#essentials'],
                'duration': 62,
                'lesson_number': 1,
                'lesson_words': list(map(str, range(1, 11))) + ['百', '千', '万', '零'],
                'music': 'Counting Beat',
            },
            # Speaking videos
            {
                'creator': 'xiaoming_teacher',
                'category': 'Speaking',
                'title': 'Tone Practice: The Four Tones',
                'description': 'Master the four tones! mā, má, mǎ, mà. The foundation of Chinese pronunciation. Practice with me every day. Can you hear the difference? 声调练习：四声。中文发音的基础。',
                'tags': ['#speaking', '#tones', '#pronunciation', '#basics', '#practice'],
                'duration': 58,
                'lesson_number': 1,
                'lesson_words': ['妈', '麻', '马', '骂'],
                'music': 'Tone Practice',
            },
            {
                'creator': 'mei_ling',
                'category': 'Speaking',
                'title': 'Common Greetings and Phrases',
                'description': 'Speak like a local! 你好、谢谢、再见. Essential greetings for everyday conversations. Perfect for beginners! Practice along! 常用问候语。日常对话必备。',
                'tags': ['#speaking', '#greetings', '#beginner', '#phrases', '#conversation'],
                'duration': 48,
                'lesson_number': 2,
                'lesson_words': ['你好', '再见', '谢谢', '不客气', '对不起', '没关系'],
                'music': 'Friendly Greetings',
            },
            # Writing videos
            {
                'creator': 'zhang_le',
                'category': 'Writing',
                'title': 'Stroke Order Basics',
                'description': 'Learn proper stroke order! 横、竖、撇、捺. Essential for writing Chinese characters correctly. Foundation of calligraphy. Start here! 笔顺基础。正确书写汉字的基础。',
                'tags': ['#writing', '#strokeorder', '#characters', '#basics', '#calligraphy'],
                'duration': 65,
                'lesson_number': 1,
                'lesson_words': ['一', '二', '三', '十', '人', '大', '天'],
                'music': 'Writing Meditation',
            },
            {
                'creator': 'li_hua',
                'category': 'Writing',
                'title': 'Common Radicals: 氵(water) and 扌(hand)',
                'description': 'Learn character components! 水、河、海 | 手、打、提. Understanding radicals helps you memorize characters. Learn the most common ones! 偏旁部首。理解偏旁帮助记忆汉字。',
                'tags': ['#writing', '#radicals', '#characters', '#hsk3', '#learningtips'],
                'duration': 71,
                'lesson_number': 3,
                'lesson_words': ['水', '河', '海', '洋', '手', '打', '提', '抱'],
                'music': 'Character Study',
            },
            # Tips videos
            {
                'creator': 'xiaoming_teacher',
                'category': 'Tips',
                'title': 'How I Memorize 50 Words Daily',
                'description': 'My vocabulary learning method! Flashcards, spaced repetition, context. Learn the techniques I use to memorize efficiently. Consistency is key! Share your tips! 我的词汇记忆方法。高效记忆技巧。',
                'tags': ['#tips', '#vocabulary', '#studymethods', '#productivity', '#learning'],
                'duration': 78,
                'lesson_words': [],
                'music': 'Motivational Beat',
            },
            {
                'creator': 'mei_ling',
                'category': 'Tips',
                'title': 'Stay Motivated Learning Chinese',
                'description': 'How to keep going! Set goals, track progress, celebrate wins. Learning Chinese is a marathon, not a sprint. You can do this! 加油！保持学习动力。',
                'tags': ['#tips', '#motivation', '#mindset', '#encouragement', '#加油'],
                'duration': 84,
                'lesson_words': [],
                'music': 'Inspiring Music',
            },
            {
                'creator': 'wang_wei',
                'category': 'Tips',
                'title': 'Best FREE Chinese Learning Resources',
                'description': 'My top free resources! Apps, websites, YouTube channels. Learn Chinese without spending money. Quality resources that work! Share yours! 最好的免费学习资源。',
                'tags': ['#tips', '#resources', '#free', '#apps', '#websites'],
                'duration': 92,
                'lesson_words': [],
                'music': 'Discovery Beat',
            },
        ]

        now = timezone.now()
        user_map = {u.username: u for u in users}
        category_map = {c.name: c for c in categories}

        # Create videos with interactions
        for idx, video_data in enumerate(videos_data):
            creator = user_map[video_data['creator']]
            category = category_map[video_data['category']]

            video = Video.objects.create(
                creator=creator,
                video_file=f'videos/{video_data["category"].lower()}_{idx}.mp4',
                thumbnail=f'video_thumbnails/{video_data["category"].lower()}_{idx}.jpg',
                duration=video_data['duration'],
                description=video_data['description'],
                category=category,
                tags=video_data['tags'],
                music_title=video_data['music'],
                lesson_number=video_data.get('lesson_number'),
                lesson_title=video_data.get('title', ''),
                lesson_words=video_data.get('lesson_words', []),
                views_count=0,
                likes_count=0,
                comments_count=0,
                shares_count=0,
                status='ready',
                is_featured=(idx % 3 == 0),  # Every 3rd video is featured
                created_at=now - timedelta(hours=idx)
            )

            # Add views from random users
            for viewer in users:
                if viewer != creator and idx % 2 == 0:
                    VideoView.objects.get_or_create(video=video, user=viewer)
                    video.views_count += 1

                    # Add likes
                    if idx % 3 == 0:
                        VideoLike.objects.get_or_create(video=video, user=viewer)
                        video.likes_count += 1

                    # Add bookmarks
                    if idx % 4 == 0:
                        VideoBookmark.objects.get_or_create(video=video, user=viewer)

            # Add comments
            comments_data = [
                'This is so helpful! 谢谢！',
                'Can you make more videos about this topic?',
                'Finally I understand this! Great explanation 🎉',
                'Your teaching style is amazing!',
                'I have been looking for this! 你太棒了！',
                'Please do HSK 4 next!',
                'This helped me so much with my exam',
                'Could you slow down a bit next time?',
                '最好的中文教学视频！',
                'Subscribed and liked! 加油！',
            ]

            for i, comment_text in enumerate(comments_data[:5]):
                commenter = users[i % len(users)]
                if commenter != creator:
                    comment = VideoComment.objects.create(
                        video=video,
                        user=commenter,
                        text=comment_text
                    )
                    video.comments_count += 1

                    # Add comment likes
                    if i % 2 == 0:
                        for liker in users[1:3]:
                            if liker != commenter:
                                VideoCommentLike.objects.get_or_create(
                                    comment=comment,
                                    user=liker
                                )
                                comment.likes_count += 1
                                comment.save()

            # Add shares
            for sharer in users[:2]:
                if sharer != creator:
                    VideoShare.objects.create(
                        video=video,
                        user=sharer,
                        platform=['whatsapp', 'instagram', 'tiktok', 'twitter'][idx % 4]
                    )
                    video.shares_count += 1

            video.save()
            self.stdout.write(f'  Created video: {video_data["title"][:40]}...')

        # Create hashtags
        all_tags = set()
        for video_data in videos_data:
            all_tags.update(video_data['tags'])

        for tag in sorted(all_tags):
            hashtag, created = VideoHashtag.objects.get_or_create(
                tag=tag,
                defaults={'uses_count': 0}
            )
            # Update usage count
            count = sum(1 for v in videos_data if tag in v['tags'])
            hashtag.uses_count = count
            hashtag.save()

        # Create following relationships
        following_pairs = [
            ('xiaoming_teacher', 'mei_ling'),
            ('xiaoming_teacher', 'wang_wei'),
            ('mei_ling', 'xiaoming_teacher'),
            ('mei_ling', 'li_hua'),
            ('wang_wei', 'zhang_le'),
            ('li_hua', 'xiaoming_teacher'),
            ('zhang_le', 'mei_ling'),
        ]

        for follower_username, following_username in following_pairs:
            try:
                UserFollowing.objects.get_or_create(
                    follower=user_map[follower_username],
                    following=user_map[following_username]
                )
            except:
                pass

        self.stdout.write(self.style.SUCCESS('\n[OK] Video population completed successfully!'))
        self.stdout.write(f'  - Created {len(users)} creators')
        self.stdout.write(f'  - Created {len(categories)} categories')
        self.stdout.write(f'  - Created {len(videos_data)} diverse videos')
        self.stdout.write(f'  - Created {len(all_tags)} hashtags')
        self.stdout.write(f'  - Created {len(following_pairs)} following relationships')
        self.stdout.write(f'  - Added views, likes, comments, and shares')
