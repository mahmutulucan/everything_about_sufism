"""
URL configuration for everything_about_sufism project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')

Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')

Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import RedirectView

# URL patterns for the entire project
urlpatterns = [
    
    # Admin site
    path('admin/', admin.site.urls),


    # Main application paths
    path('', include('pages.urls')),  # Static and informational pages

    path('content/', include('content.urls')),  # Content management

    path('user/', include('user.urls')),  # User-related functionalities


    # CKEditor paths
    path('ckeditor5/', include('django_ckeditor_5.urls')),  # Path to CKEditor


    # Static file shortcut
    path('favicon.ico',
         RedirectView.as_view(url='/static/favicon.ico')),  # Favicon


    # Password reset URLs
    path('registration/password_reset/',
        auth_views.PasswordResetView.as_view(),
        name='password_reset'),  # Path for password reset

    path('registration/password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),  # Path for password reset done

    path('registration/reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),  # Path for password reset confirmation

    path('registration/reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),  # Path for password reset completion
]
   
# Serve media files
if not settings.USE_CLOUDINARY:
    # Serve media files from MEDIA_ROOT if Cloudinary is not used.
    urlpatterns += static(settings.MEDIA_URL, 
                          document_root=settings.MEDIA_ROOT)

# Serve static files
if settings.DEBUG:
    if settings.STATICFILES_DIRS:
        # During development, serve static files from STATICFILES_DIRS
        urlpatterns += static(settings.STATIC_URL, 
                              document_root=settings.STATICFILES_DIRS[0])
else:
    # In production, static files will be handled by WhiteNoise automatically
    pass
