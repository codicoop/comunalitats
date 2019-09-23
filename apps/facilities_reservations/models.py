from django.db import models

from cc_courses.models import CoursePlace
from coopolis.models import User


class Room(models.Model):
    class Meta:
        verbose_name = "sala"
        verbose_name_plural = "sales"

    place = models.ForeignKey(CoursePlace, on_delete=models.SET_NULL, null=True, verbose_name="lloc",
                              blank=True)
    name = models.CharField("nom", max_length=250)
    color = models.CharField("color al calendari", max_length=7, default='#e94e1b',
                             help_text="Qualsevol color CSS vàlid, incloent-hi 'red', 'green', etc.")
    capacity = models.IntegerField("capacitat", default=None, null=True, blank=True)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    class Meta:
        verbose_name = "reserva"
        verbose_name_plural = "reserves"

    title = models.CharField("títol", max_length=250)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="sala")
    start = models.DateTimeField("data i hora d'inici")
    end = models.DateTimeField("data i hora de finalització")
    responsible = models.ForeignKey(
        User, verbose_name="persona responsable", blank=True, null=True, on_delete=models.SET_NULL,
        related_name='reservations', help_text="Persona de l'equip al càrrec de la reserva. Per aparèixer "
        "al desplegable, cal que la persona tingui activada la opció 'Membre del personal'.")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="creat per…", null=True)
    created = models.DateTimeField(verbose_name="creació", auto_now_add=True)

    def __str__(self):
        return self.title
