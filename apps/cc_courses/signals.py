from constance import config
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.template import Context, Template
from django.urls import reverse
from django.utils.html import strip_tags

from cc_courses.models import Activity, ActivityEnrolled, Course
from coopolis_backoffice.custom_mail_manager import MyMailTemplate

pre_save.connect(Course.pre_save, sender=Course)


@receiver(post_delete, sender=Activity)
def delete_room_reservation(sender, instance, *args, **kwargs):
    if instance.room_reservation:
        instance.room_reservation.delete()


@receiver(post_save, sender=Activity)
def save_activity(sender, instance, *args, **kwargs):
    """
    When an Activity is saved, it can happen that the nº of spots is increased.
    This signal makes sure that any available spot is filled with people in the waiting list.
    """
    _process_available_spots(instance)


@receiver(post_delete, sender=ActivityEnrolled)
def delete_enrollment(sender, instance, *args, **kwargs):
    """
    When an enrollment is deleted, we have to check if it left free spots that people in the waiting list could make use
    of.
    """
    _process_available_spots(instance.activity)


def _process_available_spots(activity):
    """
    That's going to happen both when a user removes an enrollment in the Front and when they manage them in the back.

    Therefore, it's important that it can only be triggered for events that are active and not past due. Otherwise
    users will receive e-mails months after the activity, when the Ateneu is organizing the information.
    """
    if not activity.is_past_due and activity.remaining_spots > 0 and activity.waiting_list_count > 0:
        # s'han de processar les places lliures i omplir-les amb gent en llista d'espera.
        waiting_list = activity.waiting_list
        for enrollment in waiting_list:
            # The .save() checks for free spots and sets waiting_list to false if there's one.
            enrollment.save()
            # Check that it actually is now enrolled
            if enrollment.waiting_list is False:
                _send_confirmation_email(activity, enrollment.user)


def _send_confirmation_email(activity, user):
    mail = MyMailTemplate('EMAIL_ENROLLMENT_CONFIRMATION')
    mail.to = user.email
    mail.subject_strings = {
        'activitat_nom': activity.name
    }
    mail.body_strings = {
        'activitat_nom': activity.name,
        'ateneu_nom': config.PROJECT_FULL_NAME,
        'activitat_data_inici': activity.date_start,
        'activitat_hora_inici': activity.starting_time,
        'activitat_lloc': activity.place,
        'absolute_url_my_activities': f"{settings.ABSOLUTE_URL}{reverse('my_activities')}",
        'url_web_ateneu': config.PROJECT_WEBSITE_URL,
    }
    mail.send()
