from django.db.models.signals import post_delete
from django.dispatch import receiver

from cc_courses.models import Activity


@receiver(post_delete, sender=Activity)
def delete_room_reservation(sender, instance, *args, **kwargs):
    if instance.room_reservation:
        instance.room_reservation.delete()
