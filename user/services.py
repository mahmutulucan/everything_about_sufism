from django.contrib.auth.models import User
from django.db import transaction

from .models import Follow


@transaction.atomic
def follow_user(following_user, followed_user):
    """
    Create a follow relationship between two users.

    Args:
        following_user (User): The user who wants to follow.
        followed_user (User): The user to be followed.

    Notes:
        The function is atomic, ensuring database integrity.
        It prevents a user from following themselves.
    """

    if following_user != followed_user:
        Follow.objects.get_or_create(
            following_user=following_user,
            followed_user=followed_user
        )


@transaction.atomic
def unfollow_user(following_user, followed_user):
    """Remove the follow relationship between two users."""

    Follow.objects.filter(
        following_user=following_user,
        followed_user=followed_user
    ).delete()


def get_following(user):
    """Retrieve the users that a given user is following."""
    
    following_ids = Follow.objects.filter(
        following_user=user
    ).values_list('followed_user_id', flat=True)

    return User.objects.filter(id__in=following_ids)


def get_followers(user):
    """Retrieve the users who are following a given user."""

    follower_ids = Follow.objects.filter(
        followed_user=user
    ).values_list('following_user_id', flat=True)

    return User.objects.filter(id__in=follower_ids)


def is_following(following_user, potential_followed_user):
    """
    Check if a user is following another user.

    Args:
        following_user (User): The user who might be following.
        potential_followed_user (User): The user who might be followed.

    Returns:
        bool: True if following_user is following potential_followed_user,
              False otherwise.
    """

    return Follow.objects.filter(
        following_user=following_user,
        followed_user=potential_followed_user
    ).exists()
