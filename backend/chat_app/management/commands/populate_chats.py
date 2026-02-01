"""
Django management command to populate chat data with realistic conversations
Run: python manage.py populate_chats
"""

import sys
import io
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta, datetime
from chat_app.models import (
    ChatRoom, ChatParticipant, ChatMessage, MessageReadStatus,
    Story, StoryView, StoryReaction
)

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate chat database with realistic conversations'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting chat population...'))

        # Create users
        users_data = [
            {'username': 'alex_chen', 'email': 'alex@example.com', 'first_name': 'Alex', 'last_name': 'Chen', 'bio': 'Learning Chinese for 2 years'},
            {'username': 'emma_wang', 'email': 'emma@example.com', 'first_name': 'Emma', 'last_name': 'Wang', 'bio': 'HSK 4 student'},
            {'username': 'david_liu', 'email': 'david@example.com', 'first_name': 'David', 'last_name': 'Liu', 'bio': 'Love Chinese culture'},
            {'username': 'sophia_zhang', 'email': 'sophia@example.com', 'first_name': 'Sophia', 'last_name': 'Zhang', 'bio': 'Native speaker helping learners'},
            {'username': 'michael_wu', 'email': 'michael@example.com', 'first_name': 'Michael', 'last_name': 'Wu', 'bio': 'Business Chinese learner'},
            {'username': 'lisa_ma', 'email': 'lisa@example.com', 'first_name': 'Lisa', 'last_name': 'Ma', 'bio': 'Preparing for HSK 5'},
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

        # Create chat rooms with realistic conversations
        conversations = [
            {
                'type': 'direct',
                'participants': ['alex_chen', 'emma_wang'],
                'messages': [
                    ('alex_chen', 'Hey! How did your HSK 4 exam go? 你好！HSK4考得怎么样？'),
                    ('emma_wang', 'Pretty good! I think I passed. Just need to wait for results. 还不错！我觉得能过。等成绩出来。'),
                    ('alex_chen', 'That is awesome! Which part was the most difficult? 太棒了！哪部分最难？'),
                    ('emma_wang', 'The reading section definitely. But writing was okay. 阅读部分最难点。写作还行。'),
                    ('alex_chen', 'Same for me! Do you want to practice reading together? 我也是！想一起练习阅读吗？'),
                    ('emma_wang', 'Yes! That would be great. When are you free? 好啊！你什么时候有空？'),
                    ('alex_chen', 'How about this Saturday at 2pm? We can do it on Zoom. 这周六下午2点怎么样？Zoom上练习。'),
                    ('emma_wang', 'Perfect! See you then. I will send you the invite. 完美！到时候见。我发邀请给你。'),
                    ('alex_chen', 'Great! 加油！'),
                    ('emma_wang', '加油！See you Saturday!'),
                ]
            },
            {
                'type': 'direct',
                'participants': ['david_liu', 'sophia_zhang'],
                'messages': [
                    ('david_liu', 'Hi Sophia! Can you help me with something? 你好！能帮我个忙吗？'),
                    ('sophia_zhang', 'Of course! What do you need? 当然可以！需要什么帮助？'),
                    ('david_liu', 'I am trying to understand the difference between 他和它. Can you explain? 我在搞懂他和它的区别。能解释一下吗？'),
                    ('sophia_zhang', 'Sure! 他 is for people (he/him), 它 is for animals or objects. 当然可以！他是用于人，它是用于动物或物体。'),
                    ('david_liu', 'Ah, that makes sense! So "my friend" would be 他? 啊，明白了！"我的朋友"会用他？'),
                    ('sophia_zhang', 'Yes, exactly! For example: 我的朋友，他很高。对！比如：我的朋友，他很高。'),
                    ('david_liu', 'And for my dog I would say 它? 我的狗就用它？'),
                    ('sophia_zhang', 'Correct! 我的狗，它很可爱。对！我的狗，它很可爱。'),
                    ('david_liu', 'Thank you so much! You are the best teacher! 谢谢！你是最棒的老师！'),
                    ('sophia_zhang', 'You are welcome! Keep practicing! 不客气！继续加油！'),
                ]
            },
            {
                'type': 'direct',
                'participants': ['michael_wu', 'lisa_ma'],
                'messages': [
                    ('michael_wu', 'Hey Lisa! Are you ready for the business Chinese presentation? 嘿Lisa！商务中文演讲准备好了吗？'),
                    ('lisa_ma', 'Almost! Just reviewing my notes. 差不多了！正在复习笔记。'),
                    ('michael_wu', 'Do you want to practice together? I can help you with the business terms. 要一起练习吗？我可以帮你练商务词汇。'),
                    ('lisa_ma', 'That would be amazing! I am struggling with some vocabulary. 太好了！有些词汇我还在纠结。'),
                    ('michael_wu', 'Which words are difficult? 哪些词难？'),
                    ('lisa_ma', 'Like 业绩, 利润, and 投资. I always mix them up. 比如"业绩"、"利润"和"投资"。我老是搞混。'),
                    ('michael_wu', 'I can help! 业绩 is performance/results, 利润 is profit, and 投资 is investment. 我来帮你！业绩是表现/成果，利润是profit，投资是investment。'),
                    ('lisa_ma', 'Oh! That is much clearer now. Thanks Michael! 哦！现在清楚多了。谢谢Michael！'),
                    ('michael_wu', 'No problem! We will ace this presentation! 没问题！我们的演讲一定成功！'),
                    ('lisa_ma', 'I feel much more confident now. Thanks! 我现在更有信心了。谢谢！'),
                ]
            },
            {
                'type': 'group',
                'name': 'Chinese Study Group',
                'participants': ['alex_chen', 'emma_wang', 'david_liu', 'michael_wu', 'lisa_ma'],
                'messages': [
                    ('alex_chen', 'Hey everyone! Welcome to our study group! 大家好！欢迎来到学习小组！'),
                    ('emma_wang', 'Thanks for setting this up Alex! 谢谢Alex建这个群！'),
                    ('david_liu', 'Great to be here! When do we start? 很高兴加入！什么时候开始？'),
                    ('alex_chen', 'I was thinking we could start with HSK 3 vocabulary this week. 我在想我们可以从HSK3词汇开始。'),
                    ('michael_wu', 'Sounds good! I need to review those words. 听起来不错！我要复习那些词。'),
                    ('lisa_ma', 'Count me in! I can share my notes if you want. 我算一个！我可以分享笔记。'),
                    ('emma_wang', 'That would be super helpful Lisa! Thanks! 那太有帮助了Lisa！谢谢！'),
                    ('david_liu', 'Should we set a regular study time? 我们要定个固定学习时间吗？'),
                    ('alex_chen', 'How about every Tuesday and Thursday at 7pm? 每周二和周四晚上7点怎么样？'),
                    ('emma_wang', 'Works for me! 我可以！'),
                    ('michael_wu', 'Same here! 我也是！'),
                    ('lisa_ma', 'Me too! See you all Tuesday! 我也是！周二见！'),
                    ('david_liu', 'Perfect! Looking forward to it! 完美！期待！'),
                ]
            },
            {
                'type': 'direct',
                'participants': ['alex_chen', 'sophia_zhang'],
                'messages': [
                    ('alex_chen', 'Sophia, can you help me with pronunciation? Sophia，能帮我练发音吗？'),
                    ('sophia_zhang', 'Of course! Which sounds are difficult? 当然可以！哪些音难？'),
                    ('alex_chen', 'I cannot get the difference between zh, ch, and sh. 我搞不清zh、ch、sh的区别。'),
                    ('sophia_zhang', 'Those are tricky! zh is like "j" in "judge" but with your tongue curled back. 这个很难！zh像judge的j但舌头卷回去。'),
                    ('alex_chen', 'And ch? 那ch呢？'),
                    ('sophia_zhang', 'ch is like "ch" in "church" but tongue curled. ch像church的ch但舌头卷起。'),
                    ('alex_chen', 'Let me try... zh... ch... sh... 我试试...zh...ch...sh...'),
                    ('sophia_zhang', 'Good! Now try saying: 吃饭. 好！现在试试：吃饭。'),
                    ('alex_chen', 'Chīfàn! Like that? 这样对吗？'),
                    ('sophia_zhang', 'Perfect! Your pronunciation is improving! 完美！你的发音在进步！'),
                    ('alex_chen', 'Thanks for your help! 谢谢你的帮助！'),
                ]
            },
            {
                'type': 'direct',
                'participants': ['emma_wang', 'lisa_ma'],
                'messages': [
                    ('emma_wang', 'Lisa! Did you watch that new Chinese drama? Lisa！你看了那个新国产剧吗？'),
                    ('lisa_ma', 'Yes! The one with the historical setting? 看了！那个历史背景的？'),
                    ('emma_wang', 'Yes! It is so good for learning Chinese! 对！对学中文太有用了！'),
                    ('lisa_ma', 'I know! I picked up so many new words. 我知道！我学了很多新词。'),
                    ('emma_wang', 'What was your favorite part? 你最喜欢哪部分？'),
                    ('lisa_ma', 'The dialogue between the emperor and his advisor. 皇帝和顾问的对话。'),
                    ('emma_wang', 'Same! The formal language is so interesting. 我也是！正式语言很有意思。'),
                    ('lisa_ma', 'Should we watch together next time and discuss? 下次我们一起看然后讨论？'),
                    ('emma_wang', 'Great idea! Let me know when you are free. 好主意！有空告诉我。'),
                    ('lisa_ma', 'Will do! Deal! 一定！一言为定！'),
                ]
            },
            {
                'type': 'group',
                'name': 'Beijing expats',
                'participants': ['david_liu', 'michael_wu', 'sophia_zhang'],
                'messages': [
                    ('david_liu', 'Hey! Has anyone been to that new restaurant in Sanlitun? 嘿！有人去过三里屯那个新餐厅吗？'),
                    ('michael_wu', 'Yes! The hot pot place? 去了！火锅店那个？'),
                    ('david_liu', 'That is the one! Is it good? 对！好吃吗？'),
                    ('michael_wu', 'Amazing! A bit spicy but worth it. 好吃！有点辣但值得。'),
                    ('sophia_zhang', 'I can recommend some dishes if you go! 我可以推荐一些菜！'),
                    ('david_liu', 'Please do! I am still learning the menu names. 请推荐！我还在学菜单名字。'),
                    ('sophia_zhang', 'Try 毛肚 and 鸭血. They are classic Beijing style. 试试毛肚和鸭血。经典的北京风味。'),
                    ('michael_wu', 'Oh yes! Do not forget the 豆皮! 是的！别忘了豆皮！'),
                    ('david_liu', 'Thanks! I will try them all. 谢谢！我都试试。'),
                    ('sophia_zhang', 'Let me know if you want me to come along! 想我一起去就告诉我！'),
                    ('david_liu', 'That would be great! Next weekend maybe? 太好了！下周末可能？'),
                ]
            },
        ]

        # Create chat rooms and messages
        user_map = {u.username: u for u in users}
        now = timezone.now()

        for idx, conv in enumerate(conversations):
            if conv['type'] == 'direct':
                # Direct message room
                room = ChatRoom.objects.create(
                    room_type='direct',
                    created_by=user_map[conv['participants'][0]]
                )
                for username in conv['participants']:
                    ChatParticipant.objects.create(
                        room=room,
                        user=user_map[username]
                    )
            else:
                # Group chat
                room = ChatRoom.objects.create(
                    name=conv['name'],
                    room_type='group',
                    created_by=user_map[conv['participants'][0]]
                )
                for i, username in enumerate(conv['participants']):
                    role = 'admin' if i == 0 else 'member'
                    ChatParticipant.objects.create(
                        room=room,
                        user=user_map[username],
                        role=role
                    )

            # Add messages
            base_time = now - timedelta(hours=24)
            message_interval = timedelta(minutes=5)

            for msg_idx, msg_data in enumerate(conv['messages']):
                username, text = msg_data
                message_time = base_time + (message_interval * msg_idx)

                message = ChatMessage.objects.create(
                    room=room,
                    sender=user_map[username],
                    message_type='text',
                    text=text,
                    status='read',
                    created_at=message_time,
                    updated_at=message_time
                )

                # Mark as read by other participants
                for participant in conv['participants']:
                    if participant != username:
                        try:
                            MessageReadStatus.objects.create(
                                message=message,
                                user=user_map[participant],
                                read_at=message_time + timedelta(seconds=30)
                            )
                        except:
                            pass

            self.stdout.write(f'  Created chat: {room}')

        # Create stories
        self.stdout.write('\nCreating stories...')

        stories_data = [
            ('alex_chen', 'image', 'Just finished my daily Chinese practice! 今天的中文练习完成了！'),
            ('emma_wang', 'video', 'New personal best: 50 words learned today! 今天新学了50个单词！'),
            ('david_liu', 'image', 'Found this great Chinese textbook in a bookstore! 在书店发现这本好教材！'),
            ('sophia_zhang', 'video', 'Tip of the day: Practice tones every single day! 每天都要练声调！'),
            ('michael_wu', 'image', 'Business Chinese meeting went great! 商务中文会议很成功！'),
            ('lisa_ma', 'video', 'HSK 5 prep starts now! HSK5备考开始！'),
        ]

        for idx, (username, media_type, description) in enumerate(stories_data):
            story = Story.objects.create(
                user=user_map[username],
                media_file=f'stories/user_{username}_{idx}.{"mp4" if media_type == "video" else "jpg"}',
                media_type=media_type,
                duration=15 if media_type == 'video' else None,
                expires_at=now + timedelta(hours=24)
            )

            # Add views and reactions from other users
            for viewer in users:
                if viewer.username != username:
                    if idx % 2 == 0:  # Not everyone views every story
                        StoryView.objects.create(story=story, user=viewer)
                        story.views_count += 1

                        # Add reactions
                        if idx % 3 == 0:
                            emojis = ['❤️', '🔥', '👏', '🎯']
                            StoryReaction.objects.create(
                                story=story,
                                user=viewer,
                                emoji=emojis[idx % 4]
                            )

            self.stdout.write(f'  Created story for {username}')

        self.stdout.write(self.style.SUCCESS('\n[OK] Chat population completed successfully!'))
        self.stdout.write(f'  - Created {len(users)} users')
        self.stdout.write(f'  - Created {len(conversations)} chat rooms with realistic conversations')
        self.stdout.write(f'  - Created {sum(len(c["messages"]) for c in conversations)} messages')
        self.stdout.write(f'  - Created {len(stories_data)} stories')
