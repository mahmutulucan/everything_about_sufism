from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render

from content.models import Content
from user.models import Follow
from .forms import ContactForm, ContentSearchForm


def home(request):
    """Renders the home page."""
    return render(request, 'pages/home.html')


def about(request):
    """Renders the about page."""
    return render(request, 'pages/about.html')


def content_topic_list(request, topic):
    """Displays content filtered by topic, content type, and
    optionally by followed authors."""

    # Retrieve the content type and following filter from GET parameters.
    content_type = request.GET.get('content_type', '')
    show_following_content = (
        request.GET.get('show_following_content', '') == 'true'
    )

    # Map the topic to a predefined set of categories.
    topic_mapping = {
        'history': 'history',
        'literature': 'literature',
        'concepts': 'concepts',
        'sufis': 'sufis',
        'sects': 'sects',
        'popular_topics': 'popular_topics',
        'all_contents': ''
    } 

    # If an invalid topic is provided, redirect to the default 'history' topic.
    if topic not in topic_mapping:
        messages.error(request, 'Invalid topic.')
        return redirect('content_topic_list', topic='history')

    # Build the base filter criteria for published content.
    filter_criteria = {'is_published': True}
    if topic != 'all_contents':
        filter_criteria['topic'] = topic_mapping.get(topic, '')

    # If user is authenticated and filtering by followed authors.
    if request.user.is_authenticated and show_following_content:
        followed_users = Follow.objects.filter(
            following_user=request.user
        ).values_list('followed_user_id', flat=True)
        if followed_users:
            filter_criteria['author_id__in'] = followed_users
        else:
            filter_criteria['author_id__in'] = []
            contents_topic_list = Content.objects.none()

    # Filter content by criteria and order by creation date.
    contents_topic_list = Content.objects.filter(
        **filter_criteria
    ).order_by('-created_date')

    # Further filter by content type if provided.
    if content_type:
        contents_topic_list = contents_topic_list.filter(
            content_type=content_type
        ).order_by('-created_date')

    # Set up pagination for the filtered content, 10 items per page.
    paginator = Paginator(contents_topic_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Prepare context data for rendering the template.
    context = {
        "topic": topic,
        "page_obj": page_obj,
        'content_type': content_type,
        'show_following_content': show_following_content
    }
    return render(request, 'pages/content_topic_list.html', context)


def search(request):
    """Handles multi-field search with filters and pagination."""

    content_form = ContentSearchForm(request.GET or None)
    content_results = []

    if content_form.is_valid():
        # Extract search query and fields to filter by.
        search_query = content_form.cleaned_data['search_query']
        search_fields = content_form.cleaned_data.get('search_fields', [])
        content_topic = content_form.cleaned_data.get('content_topic', '')
        content_type = content_form.cleaned_data.get('content_type', '')

        # Validate the search input.
        if not search_query:
            messages.error(request, 'Search query cannot be empty.')
        elif not search_fields:
            messages.error(request, 'Please select at least one search field.')
        else:
            # Build the search filters using Q objects.
            filters = Q()
            if 'title' in search_fields:
                filters |= Q(title__icontains=search_query)
            if 'introduction' in search_fields:
                filters |= Q(introduction__icontains=search_query)
            if 'text' in search_fields:
                filters |= Q(text__icontains=search_query)
            if 'comment' in search_fields:
                filters |= Q(comments__text__icontains=search_query)
            if 'username' in search_fields:
                filters |= (
                    Q(author__username__icontains=search_query) | 
                    Q(comments__author__username__icontains=search_query)
                )

            # Apply additional filters based on content topic and type.
            if content_topic:
                filters &= Q(topic=content_topic)
            if content_type:
                filters &= Q(content_type=content_type)

            # Retrieve and order the search results.
            content_results = (
                Content.objects.filter(filters).distinct()
                .order_by('-created_date')
            )

    # Set up pagination for the search results, 10 items per page.
    paginator = Paginator(content_results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Prepare context data for rendering the search results.
    context = {
        'content_search_form': content_form,
        'page_obj': page_obj,
        'search_query': request.GET.get('search_query', ''),
        'search_fields': request.GET.getlist('search_fields'),
        'content_topic': request.GET.get('content_topic', ''),
        'content_type': request.GET.get('content_type', ''),
    }
    return render(request, 'pages/search.html', context)


def contact_view(request):
    """Processes contact form and sends notification email to admins."""

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extract form data for sending the email.
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Determine user status for the email (guest or authenticated).
            user_status = "Guest"
            if request.user.is_authenticated:
                username = request.user.username
                user_email = request.user.email
                user_status = f"Authenticated User ({username}; {user_email})"

            # Retrieve admin contact emails from settings.
            contact_emails = settings.CONTACT_EMAILS

            # Send the contact form email.
            send_mail(
                subject=f"Contact Form: {subject}",
                message=(f"NAME: {name}\nEMAIL: {email}\n"
                         f"STATUS: {user_status}\n\nMESSAGE:\n{message}"),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=contact_emails,
                fail_silently=False
            )

            # Display success message and redirect to home page.
            success_message = "Your message has been sent successfully!"
            messages.success(request, success_message)
            return redirect('home')
        else:
            # Display error message if the form is invalid.
            error_message = (
                "There was an error with your form. "
                "Please correct the errors below."
            )
            messages.error(request, error_message)
    else:
        form = ContactForm()

    # Prepare context data for rendering the contact form.
    context = {'form': form,}
    return render(request, 'pages/contact.html', context)
