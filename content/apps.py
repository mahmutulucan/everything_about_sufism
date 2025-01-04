from django.apps import AppConfig


class ContentConfig(AppConfig):
    """Configuration for the Content application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'content'

    def ready(self):
        """Import content signals when the app is ready."""
        import content.signals
