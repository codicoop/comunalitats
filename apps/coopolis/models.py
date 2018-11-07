from cc_users.models import BaseUser


class User(BaseUser):
    @property
    def full_name(self):
        return self.get_full_name() if self.get_full_name() else self.username
