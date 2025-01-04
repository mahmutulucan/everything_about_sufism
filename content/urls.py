from django.urls import path

from . import views

# URL patterns for the content application
urlpatterns = [
    
    # Content detail and management
    path('<int:content_id>/', views.content_detail,
         name='content_detail'),  # Path to view content details

    path('add_content/', views.add_content,
         name='add_content'),  # Path to add new content

    path('edit_content/<int:content_id>/', views.edit_content,
         name='edit_content'),  # Path to edit content

    path('delete_content/<int:content_id>/', views.delete_content,
         name='delete_content'),  # Path to delete content


    # Comment management
    path('delete_comment/<int:comment_id>/', views.delete_comment,
         name='delete_comment'),  # Path to delete a specific comment


    # Like actions
    path('like_content/<int:content_id>/', views.like_content,
         name='like_content'),  # Path to like content

    path('like_comment/<int:comment_id>/', views.like_comment,
         name='like_comment'),  # Path to like a specific comment
]
