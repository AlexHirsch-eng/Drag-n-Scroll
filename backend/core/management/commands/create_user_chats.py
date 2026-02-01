"""
Create chat for user aibatyr111 with realistic Chinese conversations
Run: python manage.py create_user_chats
"""

import sys
import io
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from chat_app.models import ChatRoom, ChatParticipant, ChatMessage, MessageReadStatus

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

User = get_user_model()


class Command(BaseCommand):
    help = 'Create chats for aibatyr111 with Chinese conversations'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating chats for aibatyr111...'))

        # Create or get aibatyr111 user
        aibatyr, created = User.objects.get_or_create(
            username='aibatyr111',
            defaults={
                'email': 'aibatyr@example.com',
                'first_name': 'Aibatyr',
                'last_name': ''
            }
        )
        aibatyr.set_password('test123456')
        aibatyr.save()

        if created:
            self.stdout.write(f'  ✓ Created user: aibatyr111')
        else:
            self.stdout.write(f'  ⊙ User exists: aibatyr111')

        # Get or create conversation partners
        partners_data = [
            {
                'username': 'mei_ling',
                'email': 'mei_l@example.com',
                'first_name': 'Mei',
                'last_name': 'Ling'
            },
            {
                'username': 'xiaoming_teacher',
                'email': 'xiaoming_t@example.com',
                'first_name': 'Xiao',
                'last_name': 'Ming'
            },
            {
                'username': 'wang_wei',
                'email': 'wang_w@example.com',
                'first_name': 'Wang',
                'last_name': 'Wei'
            }
        ]

        partners = []
        for partner_data in partners_data:
            partner, created = User.objects.get_or_create(
                username=partner_data['username'],
                defaults=partner_data
            )
            partner.set_password('test123456')
            partner.save()
            partners.append(partner)
            self.stdout.write(f'  ✓ Partner ready: {partner.username}')

        # Conversation 1: Aibatyr & Mei Ling - Learning Chinese
        self.stdout.write('\nCreating chat: Aibatyr + Mei Ling...')
        room1 = ChatRoom.objects.create(
            room_type='direct',
            created_by=aibatyr
        )
        ChatParticipant.objects.create(room=room1, user=aibatyr)
        ChatParticipant.objects.create(room=room1, user=partners[0])

        messages1 = [
            (partners[0], '你好！欢迎来到我们的中文学习群！你好！'),
            (aibatyr, '你好！我想学习中文。你好！我想学习中文。'),
            (partners[0], '太好了！你学中文多久了？太好了！你学中文多久了？'),
            (aibatyr, '我才刚开始。刚开始学。我才刚开始。刚开始学。'),
            (partners[0], '没关系！我们从基础开始。没关系！我们从基础开始。'),
            (aibatyr, '好的！谢谢你的帮助。好的！谢谢你的帮助。'),
            (partners[0], '不客气！今天我们先学几个基本词汇。不客气！今天我们先学几个基本词汇。'),
            (aibatyr, '好的，我准备好了。好的，我准备好了。'),
            (partners[0], '第一个词：你好。意思是 "hello"。第一个词：你好。意思是 "hello"。'),
            (aibatyr, '你好。你好。'),
            (partners[0], '很好！发音很标准！很好！发音很标准！'),
            (aibatyr, '谢谢！那第二个词是什么？谢谢！那第二个词是什么？'),
            (partners[0], '第二个词：谢谢。意思是 "thank you"。第二个词：谢谢。意思是 "thank you"。'),
            (aibatyr, '谢谢！谢谢！'),
            (partners[0], '哈哈，用对了！我们继续学习吧。哈哈，用对了！我们继续学习吧。'),
        ]

        self.create_messages(room1, messages1, [aibatyr, partners[0]])

        # Conversation 2: Aibatyr & Xiao Ming - Grammar Lesson
        self.stdout.write('Creating chat: Aibatyr + Xiao Ming (Teacher)...')
        room2 = ChatRoom.objects.create(
            room_type='direct',
            created_by=partners[1]
        )
        ChatParticipant.objects.create(room=room2, user=aibatyr)
        ChatParticipant.objects.create(room=room2, user=partners[1])

        messages2 = [
            (partners[1], '你好！我是小明老师。你好！我是小明老师。'),
            (aibatyr, '你好老师！我想学习语法。你好老师！我想学习语法。'),
            (partners[1], '好的！今天我们学"把"字句。好的！今天我们学"把"字句。'),
            (aibatyr, '把字句？什么是把字句？把字句？什么是把字句？'),
            (partners[1], '把字句用来表示对物体的处理。比如：我把书放在桌子上。把字句用来表示对物体的处理。比如：我把书放在桌子上。'),
            (aibatyr, '我明白了吗？让我试试...我把作业做完了。我明白了吗？让我试试...我把作业做完了。'),
            (partners[1], '非常好！就是这个结构！非常好！就是这个结构！'),
            (aibatyr, '那"我吃了饭"可以改成把字句吗？那"我吃了饭"可以改成把字句吗？'),
            (partners[1], '可以！你可以说：我把饭吃了。可以！你可以说：我把饭吃了。'),
            (aibatyr, '我明白了！谢谢老师！我明白了！谢谢老师！'),
            (partners[1], '不客气！多练习就会更熟练。不客气！多练习就会更熟练。'),
            (aibatyr, '我会每天练习的！我会每天练习的！'),
            (partners[1], '加油！你一定可以的！加油！你一定可以的！'),
        ]

        self.create_messages(room2, messages2, [aibatyr, partners[1]])

        # Conversation 3: Aibatyr & Wang Wei - Casual Chat
        self.stdout.write('Creating chat: Aibatyr + Wang Wei...')
        room3 = ChatRoom.objects.create(
            room_type='direct',
            created_by=aibatyr
        )
        ChatParticipant.objects.create(room=room3, user=aibatyr)
        ChatParticipant.objects.create(room=room3, user=partners[2])

        messages3 = [
            (aibatyr, '嗨！你在吗？嗨！你在吗？'),
            (partners[2], '在的！怎么了？在的！怎么了？'),
            (aibatyr, '我想问你一个中文问题。我想问你一个中文问题。'),
            (partners[2], '当然！请问吧。当然！请问吧。'),
            (aibatyr, '"吃饭了没有"是什么意思？"吃饭了没有"是什么意思？'),
            (partners[2], '意思是"Have you eaten yet?"。这是中国人常用的问候语。意思是"Have you eaten yet?"。这是中国人常用的问候语。'),
            (aibatyr, '真的吗？那怎么回答？真的吗？那怎么回答？'),
            (partners[2], '如果你吃了，就说"吃了"。如果你吃了，就说"吃了"。'),
            (aibatyr, '如果没吃呢？如果没吃呢？'),
            (partners[2], '就说"还没吃"。就说"还没吃"。'),
            (aibatyr, '原来是这样！原来是这样！'),
            (partners[2], '对！这是中国人表示关心的方式。对！这是中国人表示关心的方式。'),
            (aibatyr, '太有意思了！我学到了很多。太有意思了！我学到了很多。'),
            (partners[2], '很高兴能帮助你！还有什么问题吗？很高兴能帮助你！还有什么问题吗？'),
            (aibatyr, '暂时没有了！谢谢！暂时没有了！谢谢！'),
            (partners[2], '不客气！随时问我。不客气！随时问我。'),
        ]

        self.create_messages(room3, messages3, [aibatyr, partners[2]])

        # Group chat with all
        self.stdout.write('Creating group chat: Chinese Learning Group...')
        room4 = ChatRoom.objects.create(
            name='中文学习小组',
            room_type='group',
            created_by=partners[1]
        )
        ChatParticipant.objects.create(room=room4, user=aibatyr, role='member')
        ChatParticipant.objects.create(room=room4, user=partners[0], role='admin')
        ChatParticipant.objects.create(room=room4, user=partners[1], role='admin')
        ChatParticipant.objects.create(room=room4, user=partners[2], role='member')

        messages4 = [
            (partners[0], '大家好！欢迎加入我们的学习小组！大家好！欢迎加入我们的学习小组！'),
            (partners[1], '我是老师，有问题可以问我。我是老师，有问题可以问我。'),
            (partners[2], '我是学中文的，我们一起学习吧！我是学中文的，我们一起学习吧！'),
            (aibatyr, '谢谢大家！我很高兴能加入。谢谢大家！我很高兴能加入。'),
            (partners[0], 'Aibatyr，你学中文多久了？Aibatyr，你学中文多久了？'),
            (aibatyr, '我才刚开始学一个月。我才刚开始学一个月。'),
            (partners[1], '不错！一个月能有这样的进步很好。不错！一个月能有这样的进步很好。'),
            (partners[2], '我们可以一起练习！我们可以一起练习！'),
            (aibatyr, '太好了！我需要很多练习。太好了！我需要很多练习。'),
            (partners[0], '每天练习一点，慢慢就会进步。每天练习一点，慢慢就会进步。'),
            (aibatyr, '我会努力的！加油！我会努力的！加油！'),
            (partners[1], '很好！有这个态度最重要。很好！有这个态度最重要。'),
            (partners[2], '我们建个学习计划吧？我们建个学习计划吧？'),
            (aibatyr, '好啊！每天学什么？好啊！每天学什么？'),
            (partners[0], '每天学5个新词汇，怎么样？每天学5个新词汇，怎么样？'),
            (aibatyr, '可以！我一定坚持。可以！我一定坚持。'),
            (partners[1], '太棒了！我们一起加油！太棒了！我们一起加油！'),
        ]

        self.create_messages(room4, messages4, [aibatyr, partners[0], partners[1], partners[2]])

        self.stdout.write(self.style.SUCCESS('\n✅ Chats created successfully!'))
        self.stdout.write('\n' + '='*60)
        self.stdout.write('LOGIN CREDENTIALS:')
        self.stdout.write('='*60)
        self.stdout.write('Username: aibatyr111    | Password: test123456')
        self.stdout.write('Username: mei_ling      | Password: test123456')
        self.stdout.write('Username: xiaoming_teacher| Password: test123456')
        self.stdout.write('Username: wang_wei      | Password: test123456')
        self.stdout.write('='*60)
        self.stdout.write('\nChats created:')
        self.stdout.write('  1. Aibatyr + Mei Ling (学习伙伴)')
        self.stdout.write('  2. Aibatyr + Xiao Ming (老师)')
        self.stdout.write('  3. Aibatyr + Wang Wei (朋友)')
        self.stdout.write('  4. 中文学习小组 (Group chat)')
        self.stdout.write('\n所有对话都是中文！加油！')

    def create_messages(self, room, messages, participants):
        """Helper to create messages with proper timestamps"""
        now = timezone.now()
        base_time = now - timedelta(hours=2)
        message_interval = timedelta(minutes=3)

        user_map = {u.id: u for u in participants}

        for idx, (sender_user, text) in enumerate(messages):
            message_time = base_time + (message_interval * idx)

            message = ChatMessage.objects.create(
                room=room,
                sender=sender_user,
                message_type='text',
                text=text,
                status='read',
                created_at=message_time,
                updated_at=message_time
            )

            # Mark as read by other participants
            for participant in participants:
                if participant.id != sender_user.id:
                    try:
                        MessageReadStatus.objects.create(
                            message=message,
                            user=participant,
                            read_at=message_time + timedelta(seconds=30)
                        )
                    except:
                        pass
