import cloudinary
from pathlib import Path

from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from user.models import Follow, Message, Notification, Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a Profile for each new User."""

    if created:
        Profile.objects.create(user=instance)


@receiver(pre_save, sender=Profile)
def delete_old_profile_image(sender, instance, **kwargs):
    """
    Deletes the old profile image file from Cloudinary or local filesystem
    if a new image is being uploaded and it differs from the old one.
    """

    if not instance.pk:
        # Instance is new, no old image to check
        return

    try:
        # Fetch the existing profile from the database
        old_image = Profile.objects.get(pk=instance.pk).image
    except Profile.DoesNotExist:
        # Profile doesn't exist yet, nothing to delete
        return

    new_image = instance.image

    # Check if the new image is different from the old image
    if old_image and old_image.name != new_image.name:
        # Ensure we don't delete the default image
        if old_image.name != 'default_profile_pic.jpg':
            if settings.USE_CLOUDINARY:  # If Cloudinary is used
                # Extract the public_id from the Cloudinary URL (name part)
                public_id = old_image.name
                try:
                    # Delete image from Cloudinary
                    cloudinary.api.delete_resources([public_id])
                except cloudinary.api.Error as e:
                    print(f"Error deleting image from Cloudinary: {e}")
            else:  # If local file system is used
                old_image_path = Path(old_image.path)
                if old_image_path.is_file():  # Check if the file exists
                    old_image_path.unlink()  # Delete the file


@receiver(post_delete, sender=User)
def delete_user_profile(sender, instance, **kwargs):
    """Delete the Profile when the User is deleted."""

    Profile.objects.filter(user=instance).delete()


@receiver(post_delete, sender=Profile)
def delete_profile_image_on_profile_delete(sender, instance, **kwargs):
    """
    Deletes the profile image file from Cloudinary or local filesystem
    when the profile is deleted.
    """

    if instance.image and instance.image.name != 'default_profile_pic.jpg':
        if settings.USE_CLOUDINARY:  # If Cloudinary is used
            # Extract the public_id from the Cloudinary URL (name part)
            public_id = instance.image.name
            try:
                # Delete image from Cloudinary
                cloudinary.api.delete_resources([public_id])
            except cloudinary.api.Error as e:
                print(f"Error deleting image from Cloudinary: {e}")
        else:  # If local file system is used
            image_path = Path(instance.image.path)
            if image_path.is_file():  # Check if the file exists
                image_path.unlink()  # Delete the file


@receiver(post_save, sender=Follow)
def create_notification_on_follow(sender, instance, created, **kwargs):
    """Create a Notification when a Follow is created."""

    # Only create notification for a new follow action
    # if the followed user exists
    if created and instance.followed_user:
        Notification.objects.create(
            user=instance.followed_user,
            notification_type=Notification.NotificationType.FOLLOW,
            from_user=instance.following_user
        )


@receiver(post_delete, sender=User)
def update_user_related_models_on_user_delete(sender, instance, **kwargs):
    """Update User-related models when a User is deleted."""

    Message.objects.filter(sender=instance).update(sender=None)
    Message.objects.filter(recipient=instance).update(recipient=None)
    Notification.objects.filter(from_user=instance).update(from_user=None)
