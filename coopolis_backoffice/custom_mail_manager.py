from django.conf import settings
from constance import config

from mailing_manager.mail_queue_handler import MailQueueHandler


class MyMailTemplate(MailQueueHandler):
    from_address = settings.DEFAULT_FROM_EMAIL
    debug_bcc = config.EMAIL_TO_DEBUG
    template = 'emails/front_generic.html'
    template_extra_context = {'config': config, }
