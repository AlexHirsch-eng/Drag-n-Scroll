"""
Sample Data Examples for Chat Models
Run this with: python manage.py shell < chat_app/sample_data.py
"""

import sys
import io

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from chat_app.models import (
    ChatRoom, ChatParticipant, ChatMessage, MessageReadStatus,
    Story, StoryView, StoryReaction, UserBlock, TypingIndicator
)

User = get_user_model()


def create_sample_chat_data():
    """Create sample chat data with 3 examples"""

    # Create test users if they don't exist
    user1, _ = User.objects.get_or_create(
        username='alice',
        defaults={
            'email': 'alice@example.com',
            'first_name': 'Alice',
            'last_name': 'Wang'
        }
    )

    user2, _ = User.objects.get_or_create(
        username='bob',
        defaults={
            'email': 'bob@example.com',
            'first_name': 'Bob',
            'last_name': 'Chen'
        }
    )

    user3, _ = User.objects.get_or_create(
        username='carol',
        defaults={
            'email': 'carol@example.com',
            'first_name': 'Carol',
            'last_name': 'Liu'
        }
    )

    # EXAMPLE 1: Direct Message between Alice and Bob
    print("Creating Example 1: Direct Message...")
    dm_room = ChatRoom.objects.create(
        room_type='direct',
        created_by=user1
    )
    ChatParticipant.objects.create(room=dm_room, user=user1)
    ChatParticipant.objects.create(room=dm_room, user=user2)

    # Add messages to DM
    ChatMessage.objects.create(
        room=dm_room,
        sender=user1,
        message_type='text',
        text='Hey Bob! How is your Chinese learning going? 你好！'
    )
    msg2 = ChatMessage.objects.create(
        room=dm_room,
        sender=user2,
        message_type='text',
        text='Great! Just learned 50 new words today. 真不错！'
    )
    MessageReadStatus.objects.create(message=msg2, user=user1)

    # EXAMPLE 2: Group Chat - Chinese Study Group
    print("Creating Example 2: Group Chat...")
    group_room = ChatRoom.objects.create(
        name='Chinese Study Group',
        room_type='group',
        created_by=user1,
        avatar='chat_avatars/group1.jpg'
    )
    ChatParticipant.objects.create(
        room=group_room,
        user=user1,
        role='admin',
        nickname='Alice 老师'
    )
    ChatParticipant.objects.create(
        room=group_room,
        user=user2,
        role='member',
        nickname='Bob 同学'
    )
    ChatParticipant.objects.create(
        room=group_room,
        user=user3,
        role='member',
        nickname='Carol 学霸'
    )

    # Add messages to group chat
    ChatMessage.objects.create(
        room=group_room,
        sender=user1,
        message_type='text',
        text='Welcome everyone! Let\'s practice HSK 3 words today. 欢迎大家！'
    )
    ChatMessage.objects.create(
        room=group_room,
        sender=user2,
        message_type='image',
        text='Check out my notes!',
        attachment={'url': '/media/chat_images/notes1.jpg', 'size': 102400}
    )
    msg3 = ChatMessage.objects.create(
        room=group_room,
        sender=user3,
        message_type='text',
        text='Here\'s a tip: Use flashcards for memorizing! 用闪示卡记忆！'
    )
    MessageReadStatus.objects.create(message=msg3, user=user1)
    MessageReadStatus.objects.create(message=msg3, user=user2)

    # EXAMPLE 3: Direct Message with Reply
    print("Creating Example 3: Direct Message with Reply...")
    dm_room2 = ChatRoom.objects.create(
        room_type='direct',
        created_by=user2
    )
    ChatParticipant.objects.create(room=dm_room2, user=user2)
    ChatParticipant.objects.create(room=dm_room2, user=user3)

    # Create message chain with replies
    original_msg = ChatMessage.objects.create(
        room=dm_room2,
        sender=user2,
        message_type='text',
        text='What\'s the best way to learn characters? 怎么学汉字最好？'
    )
    reply_msg = ChatMessage.objects.create(
        room=dm_room2,
        sender=user3,
        message_type='text',
        text='I recommend writing them out by hand. Practice stroke order! 我建议手写。',
        reply_to=original_msg
    )
    MessageReadStatus.objects.create(message=reply_msg, user=user2)

    # Create Stories
    print("Creating Sample Stories...")
    now = timezone.now()

    # Story 1: Alice's vocabulary story
    story1 = Story.objects.create(
        user=user1,
        media_file='stories/alice_vocab.mp4',
        media_type='video',
        duration=15,
        expires_at=now + timedelta(hours=24)
    )
    StoryView.objects.create(story=story1, user=user2)
    StoryView.objects.create(story=story1, user=user3)
    StoryReaction.objects.create(story=story1, user=user2, emoji='🔥')

    # Story 2: Bob's progress story
    story2 = Story.objects.create(
        user=user2,
        media_file='stories/bob_progress.jpg',
        media_type='image',
        thumbnail='story_thumbnails/bob_progress.jpg',
        expires_at=now + timedelta(hours=24)
    )
    StoryView.objects.create(story=story2, user=user1)
    StoryReaction.objects.create(story=story2, user=user1, emoji='❤️')
    StoryReaction.objects.create(story=story2, user=user3, emoji='👏')

    # Story 3: Carol's tip story
    story3 = Story.objects.create(
        user=user3,
        media_file='stories/carol_tip.mp4',
        media_type='video',
        duration=20,
        thumbnail='story_thumbnails/carol_tip.jpg',
        expires_at=now + timedelta(hours=24)
    )
    StoryView.objects.create(story=story3, user=user1)
    StoryView.objects.create(story=story3, user=user2)
    StoryReaction.objects.create(story=story3, user=user1, emoji='🎯')

    print("\n[OK] Sample chat data created successfully!")
    print(f"   - Created 3 chat rooms (2 DMs, 1 group)")
    print(f"   - Created 8 messages")
    print(f"   - Created 3 stories with views and reactions")
    print(f"   - Users: {user1.username}, {user2.username}, {user3.username}")


def display_sample_data():
    """Display all created sample data"""
    print("\n" + "="*60)
    print("CHAT ROOMS")
    print("="*60)

    for room in ChatRoom.objects.all():
        print(f"\n[CHAT] {room}")
        participants = ", ".join([p.user.username for p in room.participants.all()])
        print(f"   Participants: {participants}")
        print(f"   Messages: {room.messages.count()}")

        for msg in room.messages.all()[:3]:
            reply_info = f" (Reply to: {msg.reply_to.sender.username})" if msg.reply_to else ""
            print(f"      * {msg.sender.username}: {msg.text[:50]}...{reply_info}")

    print("\n" + "="*60)
    print("STORIES")
    print("="*60)

    for story in Story.objects.all():
        print(f"\n[STORY] {story.user.username}'s story ({story.media_type})")
        print(f"   Views: {story.views_count}")
        reactions = ", ".join([r.emoji for r in story.reactions.all()])
        print(f"   Reactions: {reactions if reactions else 'None'}")

    print("\n" + "="*60)


if __name__ == '__main__':
    create_sample_chat_data()
    display_sample_data()
