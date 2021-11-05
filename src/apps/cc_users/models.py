from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CCUserManager


class BaseUser(AbstractUser):
    class Meta:
        abstract = True

    email = models.EmailField('Correu electrònic', blank=False, null=False, unique=True)
    is_confirmed = models.BooleanField(default=False)
    objects = CCUserManager()
