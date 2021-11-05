from django.contrib.auth.models import UserManager
from django.db import models
from tagulous.models import TaggedManager


class UserQuerySet(models.QuerySet):
    def get_num_members_for_project(self, project_id):
        return self.filter(
            stage_involved_partners__project_id=project_id
        ).values(
            'stage_involved_partners__project_id'
        ).annotate(
            count=models.Count('pk', distinct=True)
        ).order_by().values('count')


class CCUserManager(TaggedManager, UserManager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def create_superuser(self, email, password, **extra_fields):
        return super().create_superuser(email, email, password, **extra_fields)

    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the email address by lowercasing it.
        """
        return email.lower()

    def get_by_natural_key(self, username):
        username_field = f"{self.model.USERNAME_FIELD}__iexact"
        return self.get(**{username_field: username})
