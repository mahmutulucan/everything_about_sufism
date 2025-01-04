from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, ContentForm
from .models import Comment, Content, Like


def content_detail(request, content_id):
    """Displays content and comments with pagination."""

    # Retrieve content or return 404 if not found
    content = get_object_or_404(Content, pk=content_id)

    # Increment views count
    Content.objects.filter(pk=content_id).update(
        views_count=F('views_count') + 1
    )

    # Fetch comments and paginate them
    comments_list = content.comments.order_by('-created_date')
    paginator = Paginator(comments_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Track user likes for content and comments if authenticated
    existing_content_like = None
    existing_comment_likes = []
    if request.user.is_authenticated:
        existing_content_like = Like.objects.filter(
            user=request.user, content=content
        ).exists()
        comment_ids = page_obj.object_list.values_list('id', flat=True)
        existing_comment_likes = Like.objects.filter(
            user=request.user, comment_id__in=comment_ids
        ).values_list('comment_id', flat=True)

    # Handle comment form submission
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must log in to comment.')
            return redirect('login')
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.content = content
            new_comment.save()
            messages.success(
                request, 'Your comment has been added successfully.'
            )
            return redirect('content_detail', content_id=content.id)
    else:
        comment_form = CommentForm()

    # Render detail template with context
    context = {
        'content': content,
        'page_obj': page_obj,
        'comment_form': comment_form,
        'existing_content_like': existing_content_like,
        'existing_comment_likes': existing_comment_likes,
    }
    return render(request, 'content/content_detail.html', context)


@login_required
def add_content(request):
    """Allows authenticated users to submit new content."""

    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.save(commit=False)
            content.author = request.user
            content.save()
            messages.success(
                request, 'Your content has been added successfully.'
            )
            return redirect('dashboard') 
    else:
        form = ContentForm()

    context = {'form': form}
    return render(request, 'content/add_content.html', context)


@login_required
def edit_content(request, content_id):
    """Allows authenticated users to edit existing content."""

    content = get_object_or_404(Content, pk=content_id)

    # Verify that the request user is the content author
    if request.user != content.author:
        messages.error(request, 'Only the author can edit this content.')
        return redirect('content_detail', content_id=content.id)

    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, 'Content updated successfully.')
            return redirect('dashboard')
    else:
        form = ContentForm(instance=content)

    context = {'form': form, 'content': content}
    return render(request, 'content/edit_content.html', context)


@login_required
def delete_content(request, content_id):
    """Allows authors to delete their content."""

    content = get_object_or_404(Content, pk=content_id)

    # Verify that the request user is the content author
    if request.user != content.author:
        messages.error(request, 'Only the author can delete this content.')
        return redirect('content_detail', content_id=content.id)

    # Confirm and delete content if POST request
    if request.method == 'POST':
        content.delete()
        messages.success(request, 'Content deleted successfully.')
        return redirect('dashboard')

    context = {'content': content}
    return render(request, 'content/delete_content.html', context)


@login_required
def delete_comment(request, comment_id):
    """Allows authors to delete their comments."""

    comment = get_object_or_404(Comment, pk=comment_id)

    # Verify that the request user is the comment author
    if request.user != comment.author:
        messages.error(request, 'Only the comment author can delete it.')
        return redirect('content_detail', content_id=comment.content.id)

    # Confirm and delete comment if POST request
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
        return redirect('content_detail', content_id=comment.content.id)

    context = {'comment': comment}
    return render(request, 'content/delete_comment.html', context)


@login_required
def like_content(request, content_id):
    """Handles liking/unliking content by authenticated users."""

    content = get_object_or_404(Content, pk=content_id)

    if request.method == 'POST':
        existing_content_like = Like.objects.filter(
            user=request.user, content=content
        ).first()

        # Toggle like status
        if existing_content_like:
            action = 'unliked'
            existing_content_like.delete()
            update_count = -1
        else:
            action = 'liked'
            like = Like(user=request.user, content=content)
            like.save()
            update_count = 1

        # Update like count
        Content.objects.filter(pk=content_id).update(
            like_count=F('like_count') + update_count
        )
        messages.success(request, f'You {action} this content.')

    return redirect('content_detail', content_id=content.id)


@login_required
def like_comment(request, comment_id):
    """Handles liking/unliking comments by authenticated users."""

    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == 'POST':
        existing_comment_like = Like.objects.filter(
            user=request.user, comment=comment
        ).first()

        # Toggle like status
        if existing_comment_like:
            action = 'unliked'
            existing_comment_like.delete()
            update_count = -1
        else:
            action = 'liked'
            like = Like(user=request.user, comment=comment)
            like.save()
            update_count = 1

        # Update like count
        Comment.objects.filter(pk=comment_id).update(
            like_count=F('like_count') + update_count
        )
        messages.success(request, f'You {action} this comment.')

    return redirect('content_detail', content_id=comment.content.id)
