"""
Sample Data Examples for Video Models
Run this with: python manage.py shell < video_app/sample_data.py
"""

import sys
import io

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from video_app.models import (
    VideoCategory, Video, VideoView, VideoLike, VideoBookmark,
    VideoComment, VideoCommentLike, VideoShare, VideoReport,
    VideoHashtag, UserFollowing
)

User = get_user_model()


def create_sample_video_data():
    """Create sample video data with 3 examples"""

    # Create test users if they don't exist
    creator1, _ = User.objects.get_or_create(
        username='xiaoming',
        defaults={
            'email': 'xiaoming@example.com',
            'first_name': 'Xiao',
            'last_name': 'Ming'
        }
    )

    creator2, _ = User.objects.get_or_create(
        username='mei_ling',
        defaults={
            'email': 'mei@example.com',
            'first_name': 'Mei',
            'last_name': 'Ling'
        }
    )

    viewer1, _ = User.objects.get_or_create(
        username='student_tom',
        defaults={
            'email': 'tom@example.com',
            'first_name': 'Tom',
            'last_name': 'Wilson'
        }
    )

    viewer2, _ = User.objects.get_or_create(
        username='student_sarah',
        defaults={
            'email': 'sarah@example.com',
            'first_name': 'Sarah',
            'last_name': 'Johnson'
        }
    )

    # Create video categories
    vocab_cat, _ = VideoCategory.objects.get_or_create(
        name='Vocabulary',
        defaults={
            'icon': '📚',
            'description': 'Learn new words and phrases',
            'order': 1
        }
    )

    grammar_cat, _ = VideoCategory.objects.get_or_create(
        name='Grammar',
        defaults={
            'icon': '📝',
            'description': 'Grammar explanations and examples',
            'order': 2
        }
    )

    culture_cat, _ = VideoCategory.objects.get_or_create(
        name='Culture',
        defaults={
            'icon': '🏮',
            'description': 'Chinese culture and traditions',
            'order': 3
        }
    )

    # EXAMPLE 1: HSK 3 Vocabulary Video
    print("Creating Example 1: Vocabulary Video...")
    video1 = Video.objects.create(
        creator=creator1,
        video_file='videos/hsk3_vocab.mp4',
        thumbnail='video_thumbnails/hsk3_vocab.jpg',
        duration=45,
        description='Learn 10 essential HSK 3 vocabulary words about daily life! '
                    'Includes pronunciation, meaning, and example sentences. '
                    '每天学十个词汇！',
        category=vocab_cat,
        tags=['#hsk3', '#vocabulary', '#chinese', '#learnchinese', '#mandarin'],
        music_title='Happy Learning Beat',
        lesson_number=3,
        lesson_title='HSK 3 Unit 1: Daily Life',
        lesson_words=['每天', '生活', '工作', '学习', '休息', '起床', '睡觉', '吃饭', '喝水', '运动'],
        views_count=1523,
        likes_count=89,
        comments_count=12,
        shares_count=5,
        status='ready',
        is_featured=True
    )

    # Add interactions for video 1
    VideoView.objects.get_or_create(video=video1, user=viewer1)
    VideoView.objects.get_or_create(video=video1, user=viewer2)

    VideoLike.objects.get_or_create(video=video1, user=viewer1)
    VideoLike.objects.get_or_create(video=video1, user=viewer2)

    VideoBookmark.objects.get_or_create(video=video1, user=viewer1)

    # Comments for video 1
    comment1 = VideoComment.objects.create(
        video=video1,
        user=viewer1,
        text='This is so helpful! 谢谢！🙏'
    )
    VideoCommentLike.objects.create(comment=comment1, user=viewer2)

    comment2 = VideoComment.objects.create(
        video=video1,
        user=viewer2,
        text='Can you make more videos about HSK 4 vocabulary?',
        parent=None
    )

    reply1 = VideoComment.objects.create(
        video=video1,
        user=creator1,
        text='Of course! Coming next week! 👍',
        parent=comment2
    )

    VideoShare.objects.create(
        video=video1,
        user=viewer1,
        platform='whatsapp'
    )

    # EXAMPLE 2: Grammar Explanation Video
    print("Creating Example 2: Grammar Video...")
    video2 = Video.objects.create(
        creator=creator2,
        video_file='videos/grammar_ba.mp4',
        thumbnail='video_thumbnails/grammar_ba.jpg',
        duration=60,
        description='Master the "把" structure in Chinese grammar! '
                    '把 sentence structure explained with simple examples. '
                    '把字句详解！',
        category=grammar_cat,
        tags=['#grammar', '#chinese', '#mandarin', '#把structure', '#intermediate'],
        music_title='',
        lesson_number=15,
        lesson_title='Grammar: 把 Structure',
        lesson_words=['把', '给', '放在', '拿来', '带去'],
        views_count=892,
        likes_count=67,
        comments_count=8,
        shares_count=3,
        status='ready',
        is_featured=False
    )

    # Add interactions for video 2
    VideoView.objects.get_or_create(video=video2, user=viewer1)
    VideoView.objects.get_or_create(video=video2, user=viewer2)

    VideoLike.objects.get_or_create(video=video2, user=viewer2)
    VideoBookmark.objects.get_or_create(video=video2, user=viewer1)
    VideoBookmark.objects.get_or_create(video=video2, user=viewer2)

    # Comments for video 2
    VideoComment.objects.create(
        video=video2,
        user=viewer2,
        text='Finally I understand this! Great explanation 🎉'
    )

    VideoShare.objects.create(
        video=video2,
        user=viewer2,
        platform='instagram'
    )

    VideoShare.objects.create(
        video=video2,
        user=viewer1,
        platform='twitter'
    )

    # EXAMPLE 3: Cultural Video - Chinese New Year
    print("Creating Example 3: Culture Video...")
    video3 = Video.objects.create(
        creator=creator1,
        video_file='videos/cny_traditions.mp4',
        thumbnail='video_thumbnails/cny_traditions.jpg',
        duration=90,
        description='Discover Chinese New Year traditions! 🧧 '
                    'Learn about red envelopes, dumplings, and more. '
                    '春节 traditions explained! ',
        category=culture_cat,
        tags=['#culture', '#chinesenewyear', '#traditions', '#china', '#springfestival'],
        music_title='Traditional Festival Music',
        lesson_number=None,
        lesson_title='',
        lesson_words=['春节', '红包', '饺子', '烟花', '舞龙', '团圆'],
        views_count=2341,
        likes_count=156,
        comments_count=23,
        shares_count=18,
        status='ready',
        is_featured=True
    )

    # Add interactions for video 3
    VideoView.objects.get_or_create(video=video3, user=viewer1)
    VideoView.objects.get_or_create(video=video3, user=viewer2)

    VideoLike.objects.get_or_create(video=video3, user=viewer1)
    VideoLike.objects.get_or_create(video=video3, user=viewer2)

    VideoBookmark.objects.get_or_create(video=video3, user=viewer1)
    VideoBookmark.objects.get_or_create(video=video3, user=viewer2)

    # Comments for video 3
    comment3 = VideoComment.objects.create(
        video=video3,
        user=viewer1,
        text='Happy New Year! 新年快乐！🎊'
    )
    VideoCommentLike.objects.create(comment=comment3, user=viewer2)

    VideoComment.objects.create(
        video=video3,
        user=viewer2,
        text='I love learning about Chinese culture! 🥰'
    )

    VideoShare.objects.create(
        video=video3,
        user=viewer1,
        platform='facebook'
    )

    VideoShare.objects.create(
        video=video3,
        user=viewer2,
        platform='tiktok'
    )

    # Create popular hashtags
    for tag in ['#hsk3', '#vocabulary', '#chinese', '#learnchinese', '#mandarin',
                '#grammar', '#culture', '#把structure']:
        VideoHashtag.objects.get_or_create(
            tag=tag,
            defaults={'uses_count': 0}
        )

    # Update hashtag usage counts
    for video in [video1, video2, video3]:
        for tag in video.tags:
            hashtag = VideoHashtag.objects.filter(tag=tag).first()
            if hashtag:
                hashtag.uses_count += 1
                hashtag.save()

    # Create user following relationships
    UserFollowing.objects.get_or_create(
        follower=viewer1,
        following=creator1
    )
    UserFollowing.objects.get_or_create(
        follower=viewer2,
        following=creator1
    )
    UserFollowing.objects.get_or_create(
        follower=viewer2,
        following=creator2
    )

    print("\n[OK] Sample video data created successfully!")
    print(f"   - Created 3 videos (Vocabulary, Grammar, Culture)")
    print(f"   - Created 3 categories: {vocab_cat}, {grammar_cat}, {culture_cat}")
    print(f"   - Added views, likes, bookmarks, comments, and shares")
    print(f"   - Created {VideoHashtag.objects.count()} hashtags")
    print(f"   - Created {UserFollowing.objects.count()} following relationships")


def display_sample_data():
    """Display all created sample data"""
    print("\n" + "="*60)
    print("VIDEOS")
    print("="*60)

    for video in Video.objects.all():
        print(f"\n[VIDEO] Video {video.id} by {video.creator.username}")
        print(f"   Title: {video.lesson_title or 'N/A'}")
        print(f"   Category: {video.category.name if video.category else 'N/A'}")
        print(f"   Duration: {video.duration}s")
        print(f"   Description: {video.description[:60]}...")
        print(f"   Tags: {', '.join(video.tags[:3])}...")
        print(f"   Stats: Views:{video.views_count} | Likes:{video.likes_count} | Comments:{video.comments_count}")

        print(f"   Comments ({video.comments.count()}):")
        for comment in video.comments.all()[:3]:
            reply_info = f" [Reply to: {comment.parent.user.username}]" if comment.parent else ""
            print(f"      * {comment.user.username}: {comment.text[:40]}...{reply_info}")

    print("\n" + "="*60)
    print("CATEGORIES")
    print("="*60)

    for cat in VideoCategory.objects.all():
        video_count = cat.videos.count()
        icon_printable = cat.icon if cat.icon else '[ICON]'
        print(f"{icon_printable} {cat.name}: {video_count} videos")

    print("\n" + "="*60)
    print("POPULAR HASHTAGS")
    print("="*60)

    for hashtag in VideoHashtag.objects.order_by('-uses_count')[:5]:
        print(f"   {hashtag.tag} - {hashtag.uses_count} uses")

    print("\n" + "="*60)
    print("USER FOLLOWING")
    print("="*60)

    for following in UserFollowing.objects.all():
        print(f"   * {following.follower.username} -> {following.following.username}")

    print("\n" + "="*60)


if __name__ == '__main__':
    create_sample_video_data()
    display_sample_data()
