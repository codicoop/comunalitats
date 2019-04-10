from django.db import models


class Published(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(publish=True)
