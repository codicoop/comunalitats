from django.db import models


class Town(models.Model):
    class Meta:
        verbose_name = "població"
        verbose_name_plural = "poblacions"

    name = models.CharField("nom", max_length=250)

    def __str__(self):
        return self.name
