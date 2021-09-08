from django.core import management


def mailqueue_send_command():
    return management.call_command("send_queued_messages", )
