from constance import config

from mailing_manager.mail_queue_handler import MailQueueHandler


class MyMailTemplate(MailQueueHandler):
    debug_bcc = config.EMAIL_TO_DEBUG
    template = 'emails/front_generic.html'
    template_extra_context = {'config': config, }
