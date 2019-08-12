# Coòpolis: Back office

Aplicació online per gestionar les formacions que fa Coòpolis durant l'any, així com l'acompanyament de projectes.

## Prepare the develop environment

*⚠ For the file and image uploads to work, set a `DJANGO_SETTINGS_MODULE` environment variable pointing to a config
module that sets `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` values.*

*⚠ If you get the "failed to load a library: cairo" when generating attendees lists, it's because of Weasyprint,
which uses Cairo.
You need to install Weasyprint in your system following the [official website's instruccions](https://weasyprint.readthedocs.io/en/stable/install.html#macos).

For the file and image uploads to work, set a `DJANGO_SETTINGS_MODULE` environment variable pointing to a config.

Because is made for multi-tenancy, you'll see that database settings are not in dev.py, but are expected to be placed
in a local settings file.
You can just put them in dev.py if you don't need multitenancy, but if you keep them in the local file
and you run commands directly in PyCharm (or virtual environment) terminal, the execution is probably
going to be missing the settings module environment variable and therefore fail.
A trick I'm doing is to create a command alias (editing ~/.bash_profile) like:
`alias pmc='DJANGO_SETTINGS_MODULE=path_to_.settings.local_settings python3 manage.py'`
And now I can run `pmc check`, `pmc makemigrations`, etc. 

### Update requirements

Make sure you have pipenv installed and to initiate it in the project's folder.
If you are using PyCharm, use [this guide](href="https://www.jetbrains.com/help/pycharm/pipenv.html") to set everything up.

### Start a DB server

`$ sudo docker run -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword postgres`

Then you could connect to the DB server and create DB:
```
$ export PGPASSWORD=mysecretpassword && psql -U postgres -h 127.0.0.1`
create database coopolis;
```

### Create the DB structure
```
python3 manage.py makemigrations
python3 manage.py migrate
```

At this point you could add fake data (⚠ this action erases data in DB):
```
python3 manage.py generatefakedata
```
