from django.db import models
from django.conf import settings


class DataExports(models.Model):
    class Meta:
        verbose_name = "exportació"
        verbose_name_plural = "exportacions"
        ordering = ["-subsidy_period"]

    created = models.DateTimeField(verbose_name="creació", auto_now_add=True)
    subsidy_period = models.CharField(
        "convocatòria", max_length=4, default=2019, choices=settings.SUBSIDY_PERIOD_OPTIONS)
    name = models.CharField("nom", max_length=200, unique=True)
    notes = models.TextField("apunts", blank=True, null=True)
    function_name = models.CharField("nom de la funció", max_length=150, unique=True,
                                     help_text="No modifiqueu aquesta dada.")

    def __str__(self):
        return self.name


class DataExportsCorrelation(models.Model):
    class Meta:
        verbose_name = "correlació"
        verbose_name_plural = "correlacions"
        ordering = ["-subsidy_period", "correlated_field", "original_data"]

    created = models.DateTimeField(verbose_name="creació", auto_now_add=True)
    subsidy_period = models.CharField(
        "convocatòria", max_length=4, default=2019, choices=settings.SUBSIDY_PERIOD_OPTIONS)
    CORRELATED_FIELD_OPTIONS = (
        ('axis', 'Eix'),
        ('stage_type', "Tipus d'acompanyament"),
        ('gender', "Gènere"),
        ('minors_grade', "Grau d'estudis")
    )
    correlated_field = models.CharField("camp", max_length=100, choices=CORRELATED_FIELD_OPTIONS)
    original_data = models.CharField("dada original", max_length=200, help_text="Valor del camp al back-office.")
    correlated_data = models.CharField("dada correlacionada", max_length=200,
                                       help_text="Com ha de quedar el valor quan l'exportem per la justificació.")

    def __str__(self):
        return self.subsidy_period + ", " + self.correlated_field
