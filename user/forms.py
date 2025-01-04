from datetime import date

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Message, Profile


class EmailAuthenticationForm(AuthenticationForm):
    """Authentication form that uses email instead of username."""

    # Use email as the username field for authentication
    username = forms.EmailField(label='Email',)

    # Override to display 'email' instead of 'username' in errors
    error_messages = {
        'invalid_login': (
            "Please enter a correct email and password. "
            "Note that both fields may be case-sensitive."
        ),
    }


class RegisterForm(UserCreationForm):
    """Form for user registration."""

    username = forms.CharField(
        label="Username",
        max_length=30,
        help_text=(
            "Required. 30 characters or fewer. "
            "Letters, digits and @/./+/-/_ only."
        ),
    )
    email = forms.EmailField(
        label="Email", 
        required=True,
        help_text=(
            "Enter a valid email address. "
            "This will be used for notifications and password recovery."
        ),
    )
    password1 = forms.CharField(
        label="Password", 
        strip=False, 
        widget=forms.PasswordInput,
        help_text=(
            "Password must be at least 8 characters long, "
            "not contain personal information, not be a common password, "
            "and not consist solely of numbers."
        ),
    )
    password2 = forms.CharField(
        label="Confirm Password", 
        widget=forms.PasswordInput,
        help_text="Enter the same password as above for verification.",
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2',]

    def clean_username(self):
        """Ensure username is unique."""

        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")

        return username

    def clean_email(self):
        """Ensure email is unique."""

        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered.")

        return email

    def clean_password2(self):
        """Ensure both password entries match."""

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password1 != password2:
            raise ValidationError("Passwords do not match.")

        return password2

    def save(self, commit=True):
        """Save user with hashed password."""

        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user


class UserUpdateForm(forms.ModelForm):
    """Form for updating user information."""

    username = forms.CharField(
        label="Username",
        max_length=30,
        help_text=(
            "Required. 30 characters or fewer. "
            "Letters, digits and @/./+/-/_ only."
        ),
    )
    email = forms.EmailField(
        label="Email", 
        required=True,
        help_text=(
            "Enter a valid email address. "
            "This will be used for notifications and password recovery."
        ),
    )
    password1 = forms.CharField(
        label="New Password", 
        strip=False, 
        widget=forms.PasswordInput, 
        required=False,
        help_text=(
            "Leave blank if you do not wish to change your password. "
            "Password must be at least 8 characters long, "
            "not contain personal information, not be a common password, "
            "and not consist solely of numbers."
        ),
    )
    password2 = forms.CharField(
        label="Confirm New Password", 
        widget=forms.PasswordInput, 
        required=False,
        help_text="Enter the same password as above for verification.",
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',]

    def clean_username(self):
        """Ensure username is unique for current user."""

        username = self.cleaned_data.get('username')

        if (
            User.objects.filter(username=username)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise ValidationError("This username is already taken.")

        return username

    def clean_email(self):
        """Ensure email is unique for current user."""

        email = self.cleaned_data.get('email')

        if (
            User.objects.filter(email=email)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise ValidationError("This email address is already registered.")

        return email

    def clean_password1(self):
        """Validate new password."""

        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                validate_password(password1, self.instance)
            except ValidationError as error:
                self.add_error('password1', error)

        return password1

    def clean(self):
        """Ensure both password entries match."""

        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")
        
        return cleaned_data

    def save(self, commit=True):
        """Save user, updating password if provided."""

        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user


class MessageForm(forms.ModelForm):
    """Form for sending messages."""

    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'message',]
        widgets = {
            "message": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"},
                config_name="extends",
            ),
        }


class ProfileForm(forms.ModelForm):
    """Form for updating user profile."""

    class Meta:
        model = Profile
        fields = [
            'birth_date', 'birth_place', 'current_location',
            'education', 'profession', 'about', 'image',
        ]

        widgets = {
            'about': CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"},
                config_name="extends",
            ),
        }

    def clean_birth_date(self):
        """Ensure birth date is not in the future."""

        birth_date = self.cleaned_data.get('birth_date')

        if birth_date and birth_date > date.today():
            raise forms.ValidationError("Birth date cannot be in the future.")

        return birth_date


class EmailVerificationForm(forms.Form):
    """Form for entering verification code."""

    verification_code = forms.CharField(
        max_length=6,
        label='Verification Code',
    )


class EmailVerificationRequestForm(forms.Form):
    """Form for requesting email verification."""

    email = forms.EmailField(label='Email Address')
