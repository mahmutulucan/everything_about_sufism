import uuid
from pathlib import Path

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from django_ckeditor_5.fields import CKEditor5Field


def content_image_directory_path(instance, filename):
    """
    Generate a unique file path for content images using UUID 
    
    to ensure uniqueness. Uses original filename and UUID to avoid conflicts.
    """

    base_filename, file_extension = Path(filename).stem, Path(filename).suffix

    unique_id = uuid.uuid4()

    new_filename = (
        f'content_{unique_id}_{slugify(base_filename)}{file_extension}'
    )

    return Path('content_images') / new_filename 


class Content(models.Model):
    """Model for different types of contents with metadata."""

    CONTENT_TYPE_CHOICES = [
        ('academic_article', 'Academic Article'),
        ('insightful_essay', 'Insightful Essay'),
        ('sufi_experience', 'Sufi Experience'),
        ('question_answer', 'Question-Answer'),
        ('book_review', 'Book/Article Review'),
    ]
    TOPIC_CHOICES = [
        ('history', 'History'),
        ('literature', 'Literature'),
        ('concepts', 'Concepts'),
        ('sufis', 'Sufis'),
        ('sects', 'Sects'),
        ('popular_topics', 'Popular Topics'),
    ]
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('nl', 'Dutch'),
        ('ku', 'Kurdish'),
        ('tr', 'Turkish'),
    ]

    content_type = models.CharField(
        max_length=30,
        choices=CONTENT_TYPE_CHOICES,
        verbose_name='Content Type',
        help_text='Select the type of content.',
    )
    topic = models.CharField(
        max_length=20,
        choices=TOPIC_CHOICES,
        verbose_name='Topic',
        help_text='Select the topic related to the content.',
    )
    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default='en',
        verbose_name='Language',
        help_text='Select the language of the content.',
    )
    title = models.CharField(
        max_length=100,
        verbose_name='Title',
        help_text='Enter the title of your content.',
    )
    introduction = models.TextField(
        verbose_name='Introduction',
        help_text='Write a brief introduction to your content.',
    )
    text = CKEditor5Field(
        verbose_name='Text',
        help_text='Enter the main content here.',
        config_name='extends',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # Keep content if author is deleted
        null=True,                  # Allow author to be NULL
        blank=True,                 # Allow author field to be blank in forms
        verbose_name='Author',
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created Date',
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Is Published',   
    )
    like_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Like Count',
    )
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Views Count',
    )
    content_image = models.ImageField(
        upload_to=content_image_directory_path,  # Content-specific upload path
        null=True,
        blank=True,
        verbose_name='Content Image',
        help_text='Upload an image for the content.',
    )

    def __str__(self):
        """String of content with author if available."""

        author_username = (
            self.author.username if self.author else "Deleted User"
        )

        return f"{self.title} by {author_username}"

    @property
    def get_image_url(self):
        """
        Return the corresponding image URL for the content type, 
        if no content image is provided by the user.
        """

        # Return image based on content type
        image_mapping = {
            'academic_article': 'img/academic_article.jpg',
            'insightful_essay': 'img/insightful_essay.jpg',
            'sufi_experience': 'img/sufi_experience.jpg',
            'question_answer': 'img/question_answer.jpg',
            'book_review': 'img/book_review.jpg',
        }

        # Return default image based on content type
        return image_mapping.get(self.content_type, 'img/default.jpg')

    @property
    def total_likes(self):
        """Get total likes for this content."""
        return self.likes.count()

    class Meta:
        verbose_name_plural = "Contents"
        indexes = [
            models.Index(fields=['content_type']),
            models.Index(fields=['topic']),
            models.Index(fields=['language']),
        ]


class Comment(models.Model):
    """Model for comments made on contents."""

    content = models.ForeignKey(
        Content,
        related_name='comments',
        on_delete=models.CASCADE,  # Delete comments if content is deleted
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # Keep comments if author is deleted
        null=True,                  # Allow author to be NULL
        blank=True,                 # Allow author field to be blank in forms
    )
    text = CKEditor5Field(
        verbose_name='Comment',
        help_text='Enter your comment here.',
        config_name='extends',
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created Date',
    )
    like_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Like Count',
    )

    @property
    def total_likes(self):
        """Get total likes for this comment."""
        return self.likes.count()

    class Meta:
        ordering = ['-created_date']
        indexes = [
            models.Index(fields=['content']),
            models.Index(fields=['author']),
        ]

    def __str__(self):
        """String of comment with author if available."""

        author_username = (
            self.author.username if self.author else "Deleted User"
        )

        return f'Comment by {author_username} on {self.content.title}'


class Like(models.Model):
    """Model for likes on contents or comments."""

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # Keep like if user is deleted
        null=True,                  # Allow user to be NULL
        blank=True,                 # Allow user field to be blank in forms
    )
    content = models.ForeignKey(
        Content,
        related_name='likes',
        on_delete=models.CASCADE,   # Delete likes if content is deleted
        null=True,                  # Allow content to be NULL
        blank=True,                 # Allow content field to be blank in forms
    )
    comment = models.ForeignKey(
        Comment,
        related_name='likes',
        on_delete=models.CASCADE,   # Delete likes if comment is deleted
        null=True,                  # Allow comment to be NULL
        blank=True,                 # Allow comment field to be blank in forms
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created Date',
    )

    class Meta:
        unique_together = ('user', 'content', 'comment')
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['content']),
            models.Index(fields=['comment']),
        ]

    def clean(self):
        """Validate like is for content or comment, not both."""

        if self.content and self.comment:
            raise ValidationError(
                'A like cannot be associated with both content and comment.'
            )

        if not self.content and not self.comment:
            raise ValidationError(
                'A like must be associated with either content or comment.'
            )

    def save(self, *args, **kwargs):
        """Save the like after validating with clean method."""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """String of like, showing user and target."""

        username = self.user.username if self.user else "Deleted User"
        target = self.content or self.comment

        return f"Like by {username} on {target}"
