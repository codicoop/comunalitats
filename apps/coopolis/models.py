from cc_users.models import BaseUser
from django.db import models


class User(BaseUser):
    class Meta:
        verbose_name_plural = "Usuaris"

    @property
    def full_name(self):
        return self.get_full_name() if self.get_full_name() else self.username


class Project(models.Model):
    class Meta:
        verbose_name_plural = "Projectes"

    SECTORS = (
        ('A', 'Altres'),
        ('C', 'Comunicació i tecnologia'),
        ('F', 'Finances'),
        ('O', 'Oci'),
        ('H', 'Habitatge'),
        ('L', 'Logística'),
        ('E', 'Educació'),
        ('C', 'Cultura'),
        ('S', 'Assessorament')
    )
    name = models.CharField("Nom", max_length=200, blank=False, unique=True)
    sector = models.CharField(max_length=2, choices=SECTORS)
    web = models.CharField("Web", max_length=200, blank=True)
    mail = models.EmailField("Correu electrònic")
    phone = models.CharField("Telèfon", max_length=25)
    members = models.ManyToManyField(User, blank=True, related_name='projects')

    def __str__(self):
        return self.name