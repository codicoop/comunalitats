# Users APP

In config:
```
LOGIN_REDIRECT_URL = '/'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
AUTH_USER_MODEL = '<project>.<model>'
DEV_SETTINGS_MODULE = '<project folder>.settings.dev'
USER_FIXTURE_FACTORY_CLASS = ''
```

## How to...

### Make log-in by the email field instead of the username

On your users model you will have to set the authentication field the `email` field and remove it from required fields.

```python
from cc_users.models import BaseUser
from cc_users.managers import CCUserManager
from django.db import models

class User(BaseUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CCUserManager()
    username = models.CharField(unique=False, max_length=1)
```

Then you will have to override the `cc_users.SignUpForm` removing the `username` field from it.

```python
from cc_users.forms import SignUpForm
class MySignUpForm(SignUpForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username')

```

Now you only have to set this form class the one to use for signing up. To do that, add it to the settings as it follows:

```python
SIGNUP_FORM = 'my_project.forms.MySignUpForm'
```
