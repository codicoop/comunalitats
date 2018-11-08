from django.db import models
from cc_lib.utils import slugify_model
from django.contrib.auth import get_user_model


class Course(models.Model):
    title = models.CharField("Títol", max_length=200, blank=False, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    place = models.ForeignKey("Places", on_delete=models.SET_NULL, null=True)
    date_start = models.DateTimeField("Dia inici")
    date_end = models.DateTimeField("Dia finalització")
    hours = models.CharField("Horaris", blank=False)
    objectives = models.TextField("Objectius")
    category = models.ForeignKey("Categories", on_delete=models.SET_NULL, null=True)
    published = models.BooleanField("Publicat")
    created = models.DateTimeField(null=True, blank=True)
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='works')

    @classmethod
    def pre_save(cls, sender, instance, **kwargs):
        slugify_model(instance, 'title')

    def __str__(self):
        return self.title


class Activity(models.Model):
    pass


class Categories(models.Model):
    name = models.CharField("Nom", max_length=200, blank=False, unique=True)


class Places(models.Model):
    name = models.CharField("Nom", max_length=200, blank=False, unique=True)
    address = models.CharField("Adreça", max_length=200)

    def __str__(self):
        return self.name
