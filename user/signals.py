import cloudinary

from django.contrib.auth.models import User
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
    Deletes the old profile image file from Cloudinary if a new image is uploaded.
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
    if old_image and new_image and old_image != new_image:
        # Only delete if a new image is being uploaded and it's different
        if old_image.public_id != 'default_profile_pic.jpg':
            # Extract the public_id from the Cloudinary object
            public_id = old_image.public_id
            try:
                # Delete image from Cloudinary
                cloudinary.api.delete_resources([public_id])
            except cloudinary.api.Error as e:
                print(f"Error deleting image from Cloudinary: {e}")


@receiver(post_delete, sender=User)
def delete_user_profile(sender, instance, **kwargs):
    """Delete the Profile when the User is deleted."""

    Profile.objects.filter(user=instance).delete()


@receiver(post_delete, sender=Profile)
def delete_profile_image_on_profile_delete(sender, instance, **kwargs):
    """
    Deletes the profile image file from Cloudinary when the profile is deleted.
    """

    if instance.image and instance.image.public_id != 'default_profile_pic.jpg':
        # Extract the public_id from the Cloudinary object
        public_id = instance.image.public_id
        try:
            # Delete image from Cloudinary
            cloudinary.api.delete_resources([public_id])
        except cloudinary.api.Error as e:
            print(f"Error deleting image from Cloudinary: {e}")


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
