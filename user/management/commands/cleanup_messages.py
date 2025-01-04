from django.core.management.base import BaseCommand
from django.utils import timezone
from user.models import Message

class Command(BaseCommand):
    """
    Command to delete expired messages marked as deleted 
    by both sender and recipient.
    """

    help = ('Deletes messages marked as deleted by both '
            'sender and recipient if older than 30 days.')

    def handle(self, *args, **kwargs):
        # Calculate the expiration date (30 days ago).
        expire_date = timezone.now() - timezone.timedelta(days=30)

        # Filter messages meeting deletion criteria.
        expired_messages = Message.objects.filter(
            is_deleted_by_sender=True,
            is_deleted_by_recipient=True,
            created_date__lt=expire_date
        )

        # Delete the filtered messages.
        expired_messages.delete()

        # Log success message to the console.
        self.stdout.write(
            self.style.SUCCESS('Expired messages have been deleted.')
        )