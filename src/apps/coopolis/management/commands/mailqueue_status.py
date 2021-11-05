from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from mailqueue.models import MailerMessage


class Command(BaseCommand):
    help = ("Prints information from the mailqueue package about pending "
            "e-mails to be sent and total e-mails recently sent.")

    def add_arguments(self, parser):
        parser.add_argument(
            "--pending",
            action="store_true",
            help="Shows the amount of e-mails currently in queue.",
        )
        parser.add_argument(
            "--sent-24h",
            action="store_true",
            help="Shows the amount of e-mails already sent or currently in "
                 "queue for the last 24hh.",
        )

    def handle(self, *args, **options):
        if options['pending']:
            self.stdout.write(str(self.get_pending_emails()))
            return

        if options['sent_24h']:
            self.stdout.write(str(self.get_total_emails(24)))
            return

        self.stdout.write("Missing parameter, use --help for more information.")

    @staticmethod
    def get_pending_emails() -> int:
        return MailerMessage.objects.filter(sent=False).count()

    @staticmethod
    def get_total_emails(hours: int) -> int:
        """
        Return the amount of e-mails in the queue for the time specified in
        hours, regardless of its status.
        :param hours: int for the amount of hours
        :return: int with the amount of e-mails
        """
        time = timezone.now() - timedelta(hours=hours)
        return MailerMessage.objects.filter(created__gt=time).count()
