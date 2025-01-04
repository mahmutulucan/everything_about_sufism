import random
import string

from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse

from .models import EmailVerification, Message, Notification


class VerificationRequiredMiddleware:
    """
    Middleware to enforce email verification.

    If the authenticated user's email is not verified, log them out
    and redirect to the verification page, except when accessing
    the verification or logout pages.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Skip the verification check for superusers
            if request.user.is_superuser:
                # Check if EmailVerification exists
                email_verification, created = (
                    EmailVerification.objects.get_or_create(
                        user=request.user,
                        defaults={'is_verified': True}
                    )
                )

                # If exists, update verification code
                if not created:
                    # If a verification code doesn't exist, generate a new one
                    if not email_verification.verification_code:
                        code = self.generate_verification_code()
                        email_verification.verification_code = code
                        email_verification.save()

                return self.get_response(request)
            
            # If not a superuser, check email verification
            email_verification = getattr(
                request.user, 'emailverification', None
            )
            # Check if user has a verified email
            if (
                email_verification is None
                or not email_verification.is_verified
            ):
                if request.path not in [
                    reverse('request_verification'),
                    reverse('logout')
                ]:
                    logout(request)
                    messages.warning(
                        request,
                        'You need to verify your email address. '
                        'Please verify your email address to access this page.'
                    )
                    return redirect(reverse('request_verification'))

        response = self.get_response(request)
        return response
    
    def generate_verification_code(self):
        """Generate a random verification code."""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class UnreadMessagesMiddleware:
    """
    Middleware to add the count of unread messages to the request.

    Adds `request.unread_count` with the count of unread messages for
    authenticated users, otherwise sets it to zero.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Count unread messages for the logged-in user
            unread_count = Message.objects.filter(
                recipient=request.user,
                is_read=False,
                is_deleted_by_recipient=False
            ).count()
            request.unread_count = unread_count
        else:
            request.unread_count = 0

        response = self.get_response(request)
        return response

class UnreadNotificationsMiddleware:
    """
    Middleware to add the count of unread notifications to the request.

    Adds `request.unread_notifications_count` with the count of unread
    notifications for authenticated users, excluding 'comment' or 'like'
    notifications from the user themselves. Sets count to zero if user
    is not authenticated.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Count unread notifications, exclude self-generated comments/likes
            unread_notifications_count = Notification.objects.filter(
                user=request.user,
                is_read=False
            ).exclude(
                notification_type__in=['comment', 'like'],
                from_user=request.user
            ).count()
            request.unread_notifications_count = unread_notifications_count
        else:
            request.unread_notifications_count = 0

        response = self.get_response(request)
        return response
