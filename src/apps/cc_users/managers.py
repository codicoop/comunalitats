from django.contrib.auth.models import UserManager
from tagulous.models import TaggedManager


class CCUserManager(TaggedManager, UserManager):
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
