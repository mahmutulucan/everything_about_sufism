import random
import string

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from cloudinary.models import CloudinaryField
from django_ckeditor_5.fields import CKEditor5Field

from content.models import Comment, Content, Like


class Message(models.Model):
    """Model for messages between users."""

    sender = models.ForeignKey(
        User,
        related_name='sent_messages',
        on_delete=models.SET_NULL,  # Keep message if sender is deleted
        null=True,                  # Allow sender to be NULL in the database
        blank=True,                 # Allow sender field to be blank in forms
        verbose_name='Sender',
        help_text='The user who sent the message.',
    )
    recipient = models.ForeignKey(
        User,
        related_name='received_messages',
        on_delete=models.SET_NULL,  # Keep message if recipient is deleted
        null=True,                  # Allow NULL recipient in the database
        blank=True,                 # Allow recipient to be blank in forms
        verbose_name='Recipient',
        help_text=(
        'Select the user who will receive the message. '
        'If not listed, they may be unregistered or have deactivated.'
        ),
    )
    subject = models.CharField(
        max_length=40,
        verbose_name='Subject',
        help_text='Enter the subject of the message.',
    )
    message = CKEditor5Field(
        verbose_name='Message',
        help_text='Enter the main message content here.',
        config_name='extends',
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created Date',
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name='Is Read',
    )
    is_deleted_by_sender = models.BooleanField(
        default=False,
        verbose_name='Is Deleted by Sender',
    )
    is_deleted_by_recipient = models.BooleanField(
        default=False,
        verbose_name='Is Deleted by Recipient',
    )

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['-created_date']
        indexes = [
            models.Index(fields=['sender']),
            models.Index(fields=['recipient']),
        ]

    def __str__(self):
        """String of message, showing sender and recipient."""

        if self.sender and self.recipient:
            return (
                f"{self.subject} ({self.sender.username} to "
                f"{self.recipient.username})"
            )

        if self.sender:
            return f"{self.subject} ({self.sender.username} to Deleted User)"

        if self.recipient:
            return (
                f"{self.subject} "
                f"(Deleted User to {self.recipient.username})"
            )

        return f"{self.subject} (Deleted User to Deleted User)"


class Profile(models.Model):
    """Model for user profiles with additional information."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,  # Delete profile if user is deleted
        verbose_name='User',
        help_text='The user this profile belongs to.',
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Birth Date',
        help_text=(
            'Enter your birth date in the format YYYY-MM-DD '
            '(e.g., 1990-01-01).'
        ),
    )
    birth_place = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Birth Place',
        help_text='Enter the place where you were born.',
    )
    current_location = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Current Location',
        help_text='Enter your current location.',
    )
    education = models.TextField(
        max_length=1000,
        null=True, 
        blank=True,
        verbose_name='Education',
        help_text='Provide details about your educational background.',
    )
    profession = models.CharField(
        max_length=100, 
        null=True, 
        blank=True,
        verbose_name='Profession',
        help_text='Specify your current profession or occupation.',
    )
    about = CKEditor5Field(
        null=True, 
        blank=True,
        verbose_name='About',
        help_text='Write a brief description about yourself.',
        config_name='extends',
    )
    image = CloudinaryField(
        'image',
        null=True,
        blank=True,
    )

    def __str__(self):
        """String of the associated user's username."""
        return self.user.username


class Follow(models.Model):
    """Model for following relationships between users."""

    following_user = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,  # Delete follow if user is removed
        verbose_name='Following User',
    )
    followed_user = models.ForeignKey(
        User,
        related_name='followers',
        on_delete=models.CASCADE,  # Delete follow if user is removed
        verbose_name='Followed User',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Followed At',
    )

    class Meta:
        # Ensure unique following relationships.
        unique_together = ('following_user', 'followed_user')


class Notification(models.Model):
    """Model for notifications sent to users."""

    class NotificationType(models.TextChoices):
        COMMENT = 'comment', _('Comment')
        LIKE = 'like', _('Like')
        FOLLOW = 'follow', _('Follow')

    user = models.ForeignKey(
        User,
        related_name='notifications',
        on_delete=models.SET_NULL,  # Set user to null if deleted
        null=True,              # Allow this field to be NULL in the database
        blank=False,         # Required in form; notification needs a recipient
        verbose_name='User',
    )
    notification_type = models.CharField(
        max_length=10,
        choices=NotificationType.choices,
        verbose_name='Notification Type',
    )
    content = models.ForeignKey(
        Content,
        related_name='notifications',
        on_delete=models.CASCADE,  # Remove notifications if content is deleted
        null=True,                # Allow this field to be NULL in the database
        blank=True,              # Allow this field to be blank in forms
        verbose_name='Content',
    )
    comment = models.ForeignKey(
        Comment,
        related_name='notifications',
        on_delete=models.CASCADE,  # Remove notifications if comment is deleted
        null=True,                # Allow this field to be NULL in the database
        blank=True,              # Allow this field to be blank in forms
        verbose_name='Comment',
    )
    like = models.ForeignKey(
        Like,
        related_name='notifications',
        on_delete=models.CASCADE,  # Remove notifications if like is deleted
        null=True,                # Allow this field to be NULL in the database
        blank=True,              # Allow this field to be blank in forms
        verbose_name='Like',
    )
    from_user = models.ForeignKey(
        User,
        related_name='sent_notifications',
        on_delete=models.SET_NULL,  # Set from_user to null if deleted
        null=True,                 # Allow this field to be NULL in the database
        blank=True,               # Allow this field to be blank in forms
        verbose_name='From User',
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created Date',
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name='Is Read',
    )

    class Meta:
        ordering = ['-created_date']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['content']),
            models.Index(fields=['comment']),
            models.Index(fields=['like']),
            models.Index(fields=['from_user']),
        ]

    def __str__(self):
        """String representation of notification."""
        
        username = (
            self.from_user.username if self.from_user else "Deleted User"
        )

        if self.notification_type == Notification.NotificationType.COMMENT:
            return f'Comment by {username} on {self.content.title}'
        elif self.notification_type == Notification.NotificationType.LIKE:
            target = self.content if self.content else self.comment
            return f'{username} liked your {target}'
        elif self.notification_type == Notification.NotificationType.FOLLOW:
            return f'{username} followed you'
        else:
            return 'Unknown Notification'


class EmailVerification(models.Model):
    """Model for managing email verification for users."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    verification_code = models.CharField(
        max_length=6,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        default=timezone.now,
    )
    is_verified = models.BooleanField(
        default=False,
    )

    def save(self, *args, **kwargs):
        """Generate verification code if needed and save instance."""

        if not self.is_verified and not self.verification_code:
            # Generate a random verification code.
            self.verification_code = ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=6)
            )

        super().save(*args, **kwargs)  # Call the parent save method.

    def send_verification_email(self):
        """Send an email with the verification code to the user."""

        # Prepare the email subject and message
        subject = 'Email Verification'
        message = (
            f'Please use the following code to verify your email: '
            f'{self.verification_code}'
        )

        # Send the email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # Sender's email address.
            [self.user.email],           # Recipient's email address.
            fail_silently=False,        # Raise an error if sending fails.
        )
