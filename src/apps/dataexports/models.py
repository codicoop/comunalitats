from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now


class SubsidyPeriod(models.Model):
    class Meta:
        verbose_name = "convocatòria"
        verbose_name_plural = "convocatòries"
        ordering = ['-date_start']

    name = models.CharField("nom", max_length=250)
    date_start = models.DateField("dia d'inici")
    date_end = models.DateField("dia de finalització")
    number = models.CharField(
        "número d'expedient", max_length=50, null=True, blank=True
    )

    @property
    def range(self):
        return self.date_start, self.date_end

    @staticmethod
    def get_current():
        today = now()
        return SubsidyPeriod.objects.get(
            date_start__lte=today, date_end__gte=today
        )

    def clean(self):
        super().clean()
        """
        Prevent the selected period from overlapping the one of any other.
        """
        q = SubsidyPeriod.objects.filter(
            models.Q(
                date_start__gte=self.date_start, date_start__lt=self.date_end
            )
            | models.Q(
                date_end__gt=self.date_start, date_end__lte=self.date_end
            )
            | models.Q(
                date_start__lte=self.date_start, date_end__gte=self.date_end
            )
        )

        if self.id:
            q = q.exclude(id=self.id)

        if q.count() > 0:
            err = ("La data d'inici i/o la de finalització seleccionades "
                   "trepitgen les d'alguna altra convocatòria, selecciona'n "
                   "unes altres.")
            raise ValidationError({'date_start': err, 'date_end': err})

    def __str__(self):
        return self.name


class DataExports(models.Model):
    class Meta:
        verbose_name = "exportació"
        verbose_name_plural = "exportacions"
        ordering = ["subsidy_period"]

    created = models.DateTimeField(verbose_name="creació", auto_now_add=True)
    subsidy_period = models.ForeignKey(SubsidyPeriod, verbose_name="convocatòria", null=True, on_delete=models.SET_NULL)
    name = models.CharField("nom", max_length=200)
    notes = models.TextField("apunts", blank=True, null=True)
    function_name = models.CharField("nom de la funció", max_length=150,
                                     help_text="No modifiqueu aquesta dada.")
    ignore_errors = models.BooleanField(
        "Ignorar errors", help_text="Si s'activa, es podràn generar els excels de justificació encara que hi hagi "
                                    "errors a les dades. Els excels que es generin així NO es podran volcar a l'excel "
                                    "real!", default=False)

    def __str__(self):
        return self.name
