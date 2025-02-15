import cloudinary

from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver

from content.models import Comment, Content, Like
from user.models import Notification


@receiver(pre_delete, sender=User)
def update_content_related_models_on_user_delete(sender, instance, **kwargs):
    """Update Content-related models when a User is deleted."""

    Content.objects.filter(author=instance).update(author=None)
    Comment.objects.filter(author=instance).update(author=None)
    Like.objects.filter(user=instance).update(user=None)


@receiver(post_save, sender=Comment)
def create_notification_on_comment(sender, instance, created, **kwargs):
    """Create a Notification when a Comment is added to a Content."""

    # Only create notification for newly created comments
    # if content has an author
    if created and instance.content.author:
        Notification.objects.create(
            user=instance.content.author,
            notification_type=Notification.NotificationType.COMMENT,
            content=instance.content,
            comment=instance,
            from_user=instance.author
        )


@receiver(post_save, sender=Like)
def create_notification_on_like(sender, instance, created, **kwargs):
    """Create Notification when Like is added to Content or Comment."""

    # Target of the Like: either Content or Comment
    target = instance.content or instance.comment

    # Only create notification if new Like is created,
    # target exists, and has an author
    if created and target and target.author:
        Notification.objects.create(
            user=target.author,
            notification_type=Notification.NotificationType.LIKE,
            content=instance.content,
            comment=instance.comment,
            like=instance,
            from_user=instance.user
        )


@receiver(pre_save, sender=Content)
def delete_old_content_image(sender, instance, **kwargs):
    """
    Deletes the old content image from Cloudinary if a new image is uploaded.
    """

    if not instance.pk:
        # Instance is new, no old image to check
        return

    try:
        # Fetch the existing content from the database
        old_image = Content.objects.get(pk=instance.pk).content_image
    except Content.DoesNotExist:
        # Content doesn't exist yet, nothing to delete
        return

    new_image = instance.content_image

    # Check if the new image is different from the old image
    if old_image and new_image and old_image != new_image:
        # Only delete if a new image is being uploaded and it's different
        if old_image.public_id != 'default_content_image.jpg':  # default image check if needed
            # Extract the public_id from the Cloudinary object
            public_id = old_image.public_id
            try:
                # Delete image from Cloudinary
                cloudinary.api.delete_resources([public_id])
            except cloudinary.api.Error as e:
                print(f"Error deleting image from Cloudinary: {e}")


@receiver(post_delete, sender=Content)
def delete_content_image_on_content_delete(sender, instance, **kwargs):
    """
    Deletes the content image file from Cloudinary when the content is deleted.
    """
    if instance.content_image and instance.content_image.public_id != 'default_content_image.jpg':
        # Extract the public_id from the Cloudinary object
        public_id = instance.content_image.public_id
        try:
            # Delete image from Cloudinary
            cloudinary.api.delete_resources([public_id])
        except cloudinary.api.Error as e:
            print(f"Error deleting image from Cloudinary: {e}")
