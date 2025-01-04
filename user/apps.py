from django.apps import AppConfig


class UserConfig(AppConfig):
    """Configuration for the User application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        """Import user signals when the app is ready."""
        import user.signals
