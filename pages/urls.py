from django.urls import path

from . import views

# URL patterns for the pages application
urlpatterns = [
    path('', views.home, name='home'),  # Path to the home page

    path('about/', views.about, name='about'),  # Path to the about page

    path('<str:topic>/', views.content_topic_list,
         name='content_topic_list'),  # Path to list content by topic

    path('pages/search/', views.search,
         name='search'),  # Path to the search page

    path('pages/contact/', views.contact_view,
         name='contact'),  # Path to the contact form page
]
