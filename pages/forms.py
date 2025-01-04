from django import forms


class ContentSearchForm(forms.Form):
    """Form for searching content based on various criteria."""

    search_query = forms.CharField(
        label='Search Query', max_length=255, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search...'}),
    )
    search_fields = forms.MultipleChoiceField(
        choices=[
            ('title', 'Content Title'),
            ('introduction', 'Content Introduction'),
            ('text', 'Content Text'),
            ('comment', 'Comment Text'),
            ('username', 'Author Username'),
        ],
        label='Search in fields',
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    content_topic = forms.ChoiceField(
        choices=[
            ('', 'All Topics'),
            ('history', 'History'),
            ('literature', 'Literature'),
            ('concepts', 'Concepts'),
            ('sufis', 'Sufis'),
            ('sects', 'Sects'),
            ('popular_topics', 'Popular Topics'),
        ],
        label='Search in topics',
        required=False,
    )
    content_type = forms.ChoiceField(
        choices=[
            ('', 'All Content Types'),
            ('academic_article', 'Academic Article'),
            ('insightful_essay', 'Insightful Essay'),
            ('sufi_experience', 'Sufi Experience'),
            ('question_answer', 'Question-Answer'),
            ('book_review', 'Book/Article Review'),
        ],
        label='Search in content types',
        required=False,
    )


class ContactForm(forms.Form):
    """Form for users to contact support or administration."""

    name = forms.CharField(label='Your Name', max_length=100,)
    email = forms.EmailField(label='Your Email',)
    subject = forms.CharField(label='Subject', max_length=200,)
    message = forms.CharField(label='Message', widget=forms.Textarea,)
