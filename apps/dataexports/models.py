from django.db import models
from django.conf import settings


class SubsidyPeriod(models.Model):
    class Meta:
        verbose_name = "convocatòria"
        verbose_name_plural = "convocatòries"

    name = models.CharField("nom", max_length=250)
    date_start = models.DateField("dia d'inici")
    date_end = models.DateField("dia de finalització")
    number = models.CharField("número d'expedient", max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class DataExports(models.Model):
    class Meta:
        verbose_name = "exportació"
        verbose_name_plural = "exportacions"
        ordering = ["-subsidy_period"]

    created = models.DateTimeField(verbose_name="creació", auto_now_add=True)
    subsidy_period = models.ForeignKey(SubsidyPeriod, null=True, on_delete=models.SET_NULL)
    name = models.CharField("nom", max_length=200, unique=True)
    notes = models.TextField("apunts", blank=True, null=True)
    function_name = models.CharField("nom de la funció", max_length=150, unique=True,
                                     help_text="No modifiqueu aquesta dada.")
    ignore_errors = models.BooleanField(
        "Ignorar errors", help_text="Si s'activa, es podràn generar els excels de justificació encara que hi hagi "
                                    "errors a les dades. Els excels que es generin així NO es podran volcar a l'excel "
                                    "real!", default=False)

    def __str__(self):
        return self.name
