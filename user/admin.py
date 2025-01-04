from django.contrib import admin
from django.utils.html import format_html

from .models import EmailVerification, Follow, Message, Notification, Profile 


def delete_selected(modeladmin, request, queryset):
    """Delete selected items from the admin interface."""
    queryset.delete()

delete_selected.short_description = "Delete selected items"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin interface for managing messages between users."""

    list_display = (
        'id', 'subject', 'sender', 'recipient', 'created_date', 'is_read',
        'is_deleted_by_sender', 'is_deleted_by_recipient',
    )
    list_display_links = ('id', 'subject')
    list_filter = (
        'is_read', 'created_date', 'is_deleted_by_sender',
        'is_deleted_by_recipient',
    )
    search_fields = ('subject', 'sender__username', 'recipient__username',)
    list_per_page = 20
    actions = ['delete_selected']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin interface for managing user profiles."""

    list_display = ('image_tag', 'user', 'birth_date')
    list_display_links = ('user',)
    search_fields = (
        'user__username', 'birth_place', 'current_location',
        'education', 'profession'
    )
    list_filter = ('birth_date',)
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        """Return an HTML tag for the profile image."""

        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" />', obj.image.url
            )

        return "No Image"
    
    image_tag.short_description = 'Profile Image'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Admin interface for managing follow relationships."""

    list_display = ('following_user', 'followed_user', 'created_at',)
    list_display_links = ('following_user', 'followed_user',)
    list_filter = ('created_at', 'following_user', 'followed_user',)
    search_fields = ('following_user__username', 'followed_user__username',)
    ordering = ('-created_at',)
    list_per_page = 20


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin interface for managing notifications."""

    list_display = (
        'user', 'notification_type', 'content', 'comment',
        'like', 'from_user', 'created_date', 'is_read',
    )
    list_display_links = ('user', 'notification_type',)
    list_filter = (
        'notification_type', 'created_date', 'is_read', 'user', 'from_user',
    )
    search_fields = (
        'user__username', 'from_user__username', 'content__title',
        'comment__text', 'notification_type',
    )
    ordering = ('-created_date',)
    list_per_page = 20
    actions = ['mark_as_read', 'delete_selected']

    def mark_as_read(self, request, queryset):
        """Mark selected notifications as read."""
        queryset.update(is_read=True)
    
    mark_as_read.short_description = "Mark selected notifications as read"


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    """Admin interface for managing email verifications."""

    list_display = ('user', 'verification_code', 'created_at', 'is_verified')
    list_display_links = (
        'user', 'verification_code', 'created_at', 'is_verified'
    )
    ordering = ('-created_at',)
    list_per_page = 20
