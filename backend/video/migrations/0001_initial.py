# Generated migration for Video sharing app

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('video_url', models.URLField(max_length=500)),
                ('thumbnail_url', models.URLField(blank=True, max_length=500)),
                ('hsk_level', models.IntegerField(default=1, help_text='HSK level (1-6)')),
                ('tags', models.JSONField(blank=True, default=list, help_text='List of tags')),
                ('views_count', models.IntegerField(default=0)),
                ('likes_count', models.IntegerField(default=0)),
                ('comments_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posted_videos', to='core.user')),
            ],
            options={
                'verbose_name': 'Видео',
                'verbose_name_plural': 'Видео',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='VideoLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='video.video')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_videos', to='core.user')),
            ],
            options={
                'verbose_name': 'Лайк видео',
                'verbose_name_plural': 'Лайки видео',
                'unique_together': {('video', 'user')},
            },
        ),
        migrations.CreateModel(
            name='VideoComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='video.video')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_comments', to='core.user')),
            ],
            options={
                'verbose_name': 'Комментарий видео',
                'verbose_name_plural': 'Комментарии видео',
                'ordering': ['created_at'],
            },
        ),
    ]
