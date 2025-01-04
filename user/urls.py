from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .forms import EmailAuthenticationForm
from . import views

# URL patterns for the user application
urlpatterns = [
    
    # Authentication URLs
    path('login/',
         LoginView.as_view(authentication_form=EmailAuthenticationForm,
                           template_name='user/login.html'),
         name='login'),  # Path for user login using email instead of username

    path('logout/', LogoutView.as_view(next_page='home'),
         name='logout'),  # Path for user logout

    path('register/', views.register,
         name='register'),  # Path for user registration


    # User profile URLs
    path('dashboard/', views.dashboard,
         name='dashboard'),  # Path for user dashboard

    path('profile/<str:username>/', views.profile_view,
         name='profile_view'),  # Path for user profile view

    path('update_profile/', views.update_profile,
         name='update_profile'),  # Path for updating user profile

    path('delete_account/', views.delete_account,
         name='delete_account'),  # Path for deleting user account


    # Messaging URLs
    path('send_message/', views.send_message,
         name='send_message'),  # Path for sending a message

    path('<str:box_type>/', views.message_list,
         name='message_list'),  # Path for listing messages by box type

    path('message/<int:pk>/', views.message_detail,
         name='message_detail'),  # Path for message detail view

    path('delete_message/<int:message_id>/', views.delete_message,
         name='delete_message'),  # Path for deleting a message


    # Follow/Unfollow URLs
    path('follow/<str:username>/<str:action>/', views.follow_view,
         name='follow_view'),  # Path for following/unfollowing a user

    path('<username>/follow/<follow_type>/', views.follow_list,
         name='follow_list'),  # Path for following list by user


    # Notification URLs
    path('user/notification_list/', views.notification_list,
         name='notification_list'),  # Path for listing notifications

    path('user/notification/<int:notification_id>/',
         views.notification_redirect,  # Path for redirecting to a notification
         name='notification_redirect'),


    # Email verification URLs
    path('user/email_verification/', views.email_verification,
         name='email_verification'),  # Path for email verification

    path('user/request_verification/', views.request_verification,
         name='request_verification'),  # Path for email verification request
]
