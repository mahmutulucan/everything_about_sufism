from django.contrib import admin
from django.utils.html import format_html

from .models import Comment, Content, Like


def delete_selected(modeladmin, request, queryset):
    """Delete selected items from the admin interface."""
    queryset.delete()

delete_selected.short_description = "Delete selected items"


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    """Admin interface for managing contents."""

    list_display = (
        'image_tag', 'id', 'title', 'author', 'is_published', 'created_date',
        'topic', 'content_type', 'language', 'like_count', 'views_count',
    )
    list_display_links = ('id', 'title',)
    list_filter = ('created_date', 'topic', 'content_type', 'language',)
    list_editable = ('is_published',)
    search_fields = ('title', 'text',)
    list_per_page = 20
    actions = ['delete_selected']

    def image_tag(self, obj):
        """Return an HTML tag for the content image."""

        if obj.content_image:
            return format_html(
                '<img src="{}" width="100" height="100" />', obj.content_image.url 
            )

        return "No Image"
    
    image_tag.short_description = 'Content Image'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin interface for managing comments."""

    list_display = ('id', 'content', 'author', 'created_date', 'like_count',)
    list_display_links = ('id', 'content',)
    list_filter = ('created_date',)
    search_fields = ('text',)
    list_per_page = 20
    actions = ['delete_selected']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """Admin interface for managing likes on contents or comments."""

    list_display = ('id', 'user', 'content', 'comment', 'created_date',)
    list_display_links = ('id',)
    list_filter = ('created_date', 'user', 'content', 'comment',)
    search_fields = ('user__username', 'content__title', 'comment__text',)
    list_per_page = 20
    actions = ['delete_selected']
