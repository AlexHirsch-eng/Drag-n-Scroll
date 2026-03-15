"""
Signals for user registration
Automatically creates UserProfile and UserCourseProgress when a User is created
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile, UserCourseProgress


@receiver(post_save, sender=User)
def create_user_profile_and_progress(sender, instance, created, **kwargs):
    """
    Create UserProfile and UserCourseProgress when a new User is created
    This ensures these objects always exist for every user
    """
    if created:
        # Create UserProfile if it doesn't exist
        UserProfile.objects.get_or_create(
            user=instance,
            defaults={'learning_language': 'RU'}
        )

        # Create UserCourseProgress if it doesn't exist
        UserCourseProgress.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the user profile when user is saved
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()
