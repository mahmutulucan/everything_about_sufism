from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from content.models import Content
from .forms import (
    EmailVerificationForm,
    EmailVerificationRequestForm,
    MessageForm,
    ProfileForm,
    RegisterForm,
    UserUpdateForm
)
from .models import EmailVerification, Message, Notification, Profile
from .services import (
    follow_user,
    get_followers,
    get_following,
    is_following,
    unfollow_user
)


def register(request):
    """Handles user registration and sends email verification code."""

    if request.method == "POST":
        # Create a form instance with POST data
        form = RegisterForm(request.POST)

        if form.is_valid():
            # Save the user and create verification record
            user = form.save()
            verification = EmailVerification.objects.create(user=user)

            # Send email with the generated verification code
            send_mail(
                'Email Verification',
                f'Your verification code is {verification.verification_code}.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            # Notify the user that a verification code has been sent
            messages.success(
                request, "A verification code has been sent to your email."
            )

            # Redirect the user to the email verification page
            return redirect('email_verification')     
    else:
        # Create an empty form for GET requests (when the page is first loaded)
        form = RegisterForm()
    
    # Render the registration page with the form
    context = {"form": form}
    return render(request, "user/register.html", context)


def email_verification(request):
    """Handles email verification for the provided verification code."""

    if request.method == 'POST':
        # Create a form instance with POST data
        form = EmailVerificationForm(request.POST)

        if form.is_valid():
            # Retrieve the verification code from the form data
            code = form.cleaned_data['verification_code']

            try:
                # Match unverified email entry by code
                verification = EmailVerification.objects.get(
                    verification_code=code, is_verified=False
                )

                 # Mark the verification as completed
                verification.is_verified = True
                verification.save()

                # Display a success message to the user
                messages.success(
                    request, 'Your email has been verified successfully.'
                )

                # Redirect the user to the login page
                return redirect('login')

            except EmailVerification.DoesNotExist:
                # Add an error if the verification code is invalid or not found
                form.add_error(None, 'Invalid verification code.')

    else:
        # Create an empty form for GET requests (when the page is first loaded)
        form = EmailVerificationForm()

    # Render the verification page with the form
    context = {"form": form}
    return render(request, 'user/email_verification.html', context)


def request_verification(request):
    """Allows users to request a new email verification code."""

    if request.method == 'POST':
        # Create a form instance with POST data
        form = EmailVerificationRequestForm(request.POST)

        if form.is_valid():
            # Retrieve the email address from the form
            email = form.cleaned_data['email']

            try:
                # Try to find the user by email
                user = User.objects.get(email=email)

                try:
                    # Try to find the email verification record for the user
                    verification = EmailVerification.objects.get(user=user)

                    if verification.is_verified:
                        # If the email is already verified, show a message
                        messages.info(
                            request,
                            'Your email is verified. You can log in now.'
                        )
                        return redirect('login')
                    else:
                        # If not verified, send a new verification email
                        verification.send_verification_email()
                        messages.info(
                            request,
                            'A new code has been sent to your email.'
                        )
                        return redirect('email_verification')
                except EmailVerification.DoesNotExist:
                    # If no verification record exists, prompt user to register
                    messages.error(
                        request, 'No verification found. Please register.'
                    )
                    return redirect('register')
            except User.DoesNotExist:
                # If no user found with this email, prompt to register
                messages.error(
                    request,
                    'No user found with this email. Please register.'
                )
                return redirect('register')
    else:
        # Create an empty form for GET requests (when the page is first loaded)
        form = EmailVerificationRequestForm()

    # Render the request verification page with the form
    context = {"form": form}
    return render(request, 'user/request_verification.html', context)


@login_required
def dashboard(request):
    """Displays user's dashboard with their content."""

    # Retrieve the content type filter from the request (if provided)
    content_type = request.GET.get('content_type', '')

    if content_type:
        # If content type is specified, filter the content by that type
        contents = Content.objects.filter(
            author=request.user, content_type=content_type
            ).order_by('-created_date')
    else:
        # If no content type is specified, retrieve all content by the user
        contents = Content.objects.filter(author=request.user).order_by(
            '-created_date'
        )

    # Paginate the content (10 items per page)
    paginator = Paginator(contents, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pass paginated content and content type filter to the template
    context = {
        'page_obj': page_obj,  # Paginated content
        'content_type': content_type,  # Selected content type for filtering
    }
    return render(request, 'user/dashboard.html', context)


@login_required
def delete_account(request):
    """Deletes the user's account upon confirmation."""

    if request.method == "POST":
        # Delete the user's account upon POST request
        request.user.delete()

        # Display a success message after deletion
        messages.success(
            request, "Your account has been deleted successfully."
        )

        # Redirect to the home page after account deletion
        return redirect("home")

    # Render the account deletion confirmation page
    return render(request, "user/delete_account.html")


@login_required
def update_profile(request):
    """Updates user's profile information and email verification."""

    if request.method == 'POST':
        # Initialize forms with POST data and current user/profile instance
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        old_email = request.user.email

        if user_form.is_valid() and profile_form.is_valid():
            # Save the updated user and profile information
            user = user_form.save()
            profile_form.save()
            
            # Check if the email address has changed
            if user.email != old_email:
                # Get or create email verification record for the user
                email_verification = EmailVerification.objects
                verification, created = email_verification.get_or_create(
                    user=user
                )

                if created or verification.is_verified:
                    # Mark email unverified and send new verification email
                    verification.is_verified = False
                    verification.save()
                    verification.send_verification_email()

                    # Notify user to verify their new email address
                    messages.info(
                        request,
                        "Please verify your new email address."
                    )
                    return redirect('email_verification')
                else:
                    # If email is already verified, inform the user
                    messages.info(request, "Your email is already verified.")
                    return redirect('home')

            # Success message after profile update    
            messages.success(
                request, "Your profile has been updated successfully."
            )
            return redirect('home')
        else:
            # Display error message if there are form validation errors
            messages.error(request, "Please correct the errors below.")
    else:
        # Initialize forms with current user/profile data for GET request
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    # Pass the forms to the template for rendering
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'user/update_profile.html', context)


@login_required
def send_message(request):
    """Allows users to send a message to another user."""

    if request.method == "POST":
        # Initialize the form with POST data
        form = MessageForm(request.POST)

        if form.is_valid():
            # Save the message but don't commit yet
            message = form.save(commit=False)
            # Set the sender as the current user
            message.sender = request.user
            message.save()

            # Display a success message after sending the message
            messages.success(
                request, 'Your message has been sent successfully.'
            )

            # Redirect to the 'outbox' message list
            return redirect('message_list', box_type='outbox')
    else:
        # Initialize an empty form for GET request (page load)
        form = MessageForm()

    # Pass the form to the template for rendering
    context = {"form": form}
    return render(request, 'user/send_message.html', context)


@login_required
def message_list(request, box_type):
    """Displays the list of messages in the user's inbox or outbox."""

    if box_type == 'inbox':
        # Retrieve inbox messages, filter by recipient and not deleted
        messages_list = Message.objects.filter(
            recipient=request.user, 
            is_deleted_by_recipient=False
        ).select_related('sender').order_by('-created_date')

    elif box_type == 'outbox':
        # Retrieve outbox messages, filter by sender and not deleted
        messages_list = Message.objects.filter(
            sender=request.user, 
            is_deleted_by_sender=False
        ).select_related('recipient').order_by('-created_date')

    else:
        # Handle invalid box type and redirect to inbox
        messages.error(request, 'Invalid box type.')
        return redirect('message_list', box_type='inbox')
    
    # Paginate the messages (10 items per page)
    paginator = Paginator(messages_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
     # Pass the paginated messages and box type to the template
    context = {
        "page_obj": page_obj,  # Paginated messages
        "box_type": box_type  # The selected box type (inbox/outbox)
    }
    return render(request, 'user/message_list.html', context)


@login_required
def message_detail(request, pk):
    """Displays the details of a specific message."""

    # Get message by pk or return 404 if not found
    message = get_object_or_404(Message, pk=pk)

    # Mark message as read if in user's inbox and unread
    if message.recipient == request.user and not message.is_read:
        message.is_read = True
        message.save(update_fields=['is_read'])

    # Redirect to inbox if user is not sender or recipient
    if request.user != message.sender and request.user != message.recipient:
        return redirect('message_list', box_type='inbox')

    # Pass the message to the template for rendering
    context = {"message": message}
    return render(request, 'user/message_detail.html', context)


@login_required
def delete_message(request, message_id):
    """Allows users to delete a specific message."""

    # Retrieve the message by ID or return a 404 error if not found
    message = get_object_or_404(Message, id=message_id)

    # Check if the user is the sender or recipient of the message
    is_sender = request.user == message.sender
    is_recipient = request.user == message.recipient
    
    # If the user is neither the sender nor recipient,
    # show an error and redirect
    if not is_sender and not is_recipient:
        messages.error(
            request, 'You are not authorized to delete this message.'
        )
        return redirect('message_list', box_type='inbox')
    
    if request.method == 'POST':
        # Mark the message as deleted by the sender and/or recipient
        if is_sender and is_recipient:
            message.is_deleted_by_sender = True
            message.is_deleted_by_recipient = True
        elif is_sender:
            message.is_deleted_by_sender = True
        elif is_recipient:
            message.is_deleted_by_recipient = True

        # Save the updated message and display a success message
        message.save()
        messages.success(request, 'Message deleted successfully.')

        # Redirect to the message list (inbox)
        return redirect('message_list', box_type='inbox')
    
    # Render the message deletion confirmation page
    context = {'message': message}
    return render(request, 'user/delete_message.html', context)


@login_required
def profile_view(request, username):
    """Displays the profile page for a specific user."""

    # Retrieve the user and profile information or return 404 if not found
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    
    # Prepare filtering arguments for content based on the user's posts
    filter_kwargs = {'author': user, 'is_published': True}

    # Optionally filter by content type if provided in the request
    content_type = request.GET.get('content_type', '')
    if content_type:
        filter_kwargs['content_type'] = content_type

    # Fetch the content based on filter criteria, ordered by creation date
    contents = Content.objects.filter(**filter_kwargs).order_by(
        '-created_date'
    )

     # Paginate the content (10 items per page)
    paginator = Paginator(contents, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get the following and follower information for the user:
    # Check if the current user is following the profile user
    is_following_user = is_following(request.user, user)
    # Get the list of users the profile user is following
    following_users = get_following(user)
    # Get the list of users following the profile user
    followers = get_followers(user)

    # Pass all necessary data to the template context
    context = {
        'user': user,  # Profile user
        'profile': profile,  # User's profile data
        'page_obj': page_obj,  # Paginated content for display
        'is_following_user': is_following_user,  # Check if user follows
        'following_users': following_users,  # List of users profile follows
        'followers': followers,  # List of users following the profile user
        'content_type': content_type,  # Filtered content type if provided
    }

    # Render the profile page with the context data
    return render(request, 'user/profile_view.html', context)


@login_required
def follow_view(request, username, action):
    """Handles follow/unfollow actions for a specific user."""

    # Process follow/unfollow actions via POST request
    if request.method == 'POST':
        # Get user to follow/unfollow or return 404 if not found
        user_to_follow_or_unfollow = get_object_or_404(User, username=username)

        # Handle the 'follow' action
        if action == 'follow':
            if not is_following(request.user, user_to_follow_or_unfollow):
                # Follow the user if not already following
                follow_user(request.user, user_to_follow_or_unfollow)
                messages.success(
                    request,
                    f'You are now following '
                    f'{user_to_follow_or_unfollow.username}.'
                )
            else:
                # Inform the user if already following
                messages.info(
                    request,
                    f'You are already following '
                    f'{user_to_follow_or_unfollow.username}.'
                )

        # Handle the 'unfollow' action
        elif action == 'unfollow':
            if is_following(request.user, user_to_follow_or_unfollow):
                # Unfollow the user if currently following
                unfollow_user(request.user, user_to_follow_or_unfollow)
                messages.success(
                    request,
                    f'You have unfollowed '
                    f'{user_to_follow_or_unfollow.username}.'
                )
            else:
                # Inform the user if not following
                messages.info(
                    request,
                    f'You are not following '
                    f'{user_to_follow_or_unfollow.username}.'
                )
        else:
            # Handle invalid actions and redirect to home
            messages.error(request, 'Invalid action.')
            return redirect('home')

    # Redirect the user back to the previous page or home if no referer
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def follow_list(request, username, follow_type):
    """Displays a list of followers or following for a specific user."""

    # Retrieve the user by username or return a 404 error if not found
    user = get_object_or_404(User, username=username)

    # Select the list based on the 'follow_type' (followers or following)
    if follow_type == 'followers':
        items = get_followers(user)  # Get the list of followers
    elif follow_type == 'following':
        items = get_following(user)  # Get list of users user follows
    else:
        # Error if 'follow_type' invalid, then redirect to profile
        messages.error(request, 'Invalid follow type.')
        return redirect('profile_view', username=user.username)

     # Add follow status for each user in the list
    items_with_status = [
        {
            # The followed or following user
            'user': item,
            # Check if the current user is following this user
            'is_following': is_following(request.user, item),
            # List of users that the item is following
            'following_users': get_following(item),
            # List of followers of the item
            'followers': get_followers(item)
        }
        for item in items
    ]

    # Paginate the list of followers or following (10 items per page)
    paginator = Paginator(items_with_status, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pass the user data, pagination, and follow type to the template context
    context = {
        'user': user,  # Profile user, followers/following shown
        "page_obj": page_obj,  # Paginated list of followers or following
        'follow_type': follow_type,  # Indicates if showing followers/following
    }

    # Render the follow list page
    return render(request, 'user/follow_list.html', context)


@login_required
def notification_list(request):
    """Displays a list of notifications for the logged-in user."""

    # Retrieve notifications for the logged-in user, ordered by creation date
    notifications = Notification.objects.filter(user=request.user).order_by(
        '-created_date'
    )

    # Exclude comment/like notifications where user is sender
    notifications = notifications.exclude(
        notification_type__in=['comment', 'like'],
        from_user=request.user
    )
    
    # Count the unread notifications
    unread_notifications_count = notifications.filter(is_read=False).count()

    # Paginate notifications (10 items per page)
    paginator = Paginator(notifications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pass the paginated notifications and unread count to the template context
    context = {
        "page_obj": page_obj,
        'unread_notifications_count': unread_notifications_count,
    }

    # Render the notification list page with the context data
    return render(request, 'user/notification_list.html', context)


@login_required
def notification_redirect(request, notification_id):
    """Redirects user based on the notification type."""

    # Retrieve the notification or return a 404 error if not found
    notification = get_object_or_404(Notification, id=notification_id)

    # Ensure the notification belongs to the current user
    if notification.user != request.user:
        raise PermissionDenied(
            "You are not authorized to view this notification."
        )

    # Mark the notification as read if it hasn't been already
    if not notification.is_read:
        notification.is_read = True
        notification.save()

    # Redirect based on the notification type
    if notification.notification_type == 'comment':
        # Redirect to content detail page if notification is for comment
        return redirect(
            'content_detail', content_id=notification.comment.content.id
        )
    
    elif notification.notification_type == 'like':
        # Redirect to the content detail page if the notification is for a like
        if notification.content:
            return redirect(
                'content_detail', content_id=notification.content.id
            )
        # If like is for a comment, redirect to the comment's content
        elif notification.comment and notification.comment.content:
            return redirect(
                'content_detail', content_id=notification.comment.content.id
            )
    
    elif notification.notification_type == 'follow' and notification.from_user:
        # Redirect to profile view page if notification is for a follow action
        return redirect(
            'profile_view', username=notification.from_user.username
        )

    # If no valid notification type, redirect to the notification list page
    return redirect('notification_list')
