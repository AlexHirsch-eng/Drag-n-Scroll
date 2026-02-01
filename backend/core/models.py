"""
Core models for User and Profile
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Custom User model extending AbstractUser
    """
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    """
    User profile with learning preferences
    """
    LANGUAGE_CHOICES = [
        ('RU', 'Russian'),
        ('KZ', 'Kazakh'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    learning_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='RU')
    current_hsk_level = models.IntegerField(default=1)  # HSK 1-6
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username}'s profile"


class UserCourseProgress(models.Model):
    """
    Track user's progress through the course
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='progress')

    # Current position in course
    current_day = models.IntegerField(default=1)
    current_lesson = models.IntegerField(default=1)
    current_step = models.IntegerField(default=1)

    # Progress metrics
    total_xp = models.IntegerField(default=0)
    streak_days = models.IntegerField(default=0)
    last_study_date = models.DateField(null=True, blank=True)

    # Completed days tracking
    completed_days = models.JSONField(default=list, blank=True)  # [1, 2, 3, ...]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Course Progress'
        verbose_name_plural = 'User Course Progress'

    def __str__(self):
        return f"{self.user.username}'s progress - Day {self.current_day}"

    def add_xp(self, xp: int):
        """Add XP and update total"""
        self.total_xp += xp
        self.save()

    def update_streak(self):
        """Update streak based on last study date"""
        today = timezone.now().date()
        if self.last_study_date:
            delta = (today - self.last_study_date).days
            if delta == 1:
                # Studied yesterday, increment streak
                self.streak_days += 1
            elif delta > 1:
                # Missed days, reset streak
                self.streak_days = 1

        self.last_study_date = today
        self.save()

    def mark_day_complete(self, day_number: int):
        """Mark a day as completed"""
        if day_number not in self.completed_days:
            self.completed_days.append(day_number)
            # Move to next day
            self.current_day = day_number + 1
            self.current_lesson = 1
            self.current_step = 1
            self.save()
