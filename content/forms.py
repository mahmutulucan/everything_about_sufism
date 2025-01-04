from django import forms

from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Content, Comment


class ContentForm(forms.ModelForm):
    """Form for creating and editing content."""

    class Meta:
        model = Content
        fields = [
            'content_type', 'topic', 'language', 'title',
            'introduction', 'text', 'content_image',
        ]
        widgets = {
            'text': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'},
                config_name='extends',
            ),
        }


class CommentForm(forms.ModelForm):
    """Form for creating and editing comments."""

    class Meta:
        model = Comment
        fields = ['text',]
        widgets = {
            'text': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'},
                config_name='extends',
            ),
        }
