from django.db import models


class ActivityFileType(models.TextChoices):
    WORK = "WORK", "De treball"
    JUSTIFICATION = "JUSTIFICATION", "Justificatori"
