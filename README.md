# Coòpolis: Back office

Aplicació online per gestionar les formacions que fa Coòpolis durant l'any, així com l'acompanyament de projectes.

## Prepare the develop environment

*⚠ For the file and image uploads to work, set a `DJANGO_SETTINGS_MODULE` environment variable pointing to a config
module that sets `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` values.*

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
