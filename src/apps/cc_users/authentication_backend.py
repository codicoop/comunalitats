from django.contrib.auth.backends import ModelBackend

from apps.cc_users.models import User


class IdNumberBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        id_number = kwargs['username']
        password = kwargs['password']
        try:
            user = User.objects.get(id_number__iexact=id_number)
            if user.check_password(password) is True:
                return user
        except User.DoesNotExist:
            pass
