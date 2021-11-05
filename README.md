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

Another option to do this is with PyCharm settings, at Tools -> Terminal -> Environment Variables.
(needs restarting to take effect)

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

### Editing stylesheets

They're located at apps/coopolis/static/styles

Use sass to compile them.
So first of all [install sass](https://sass-lang.com/install) in your computer.

Edit the files inside styles/scss, don't touch styles/stylesheet.css.

To compile, go to styles/scss folder and do:

    sass main.scss ../stylesheet.css
    
There's an option to keep the service running so it detects changes and auto-compiles them, but I had
problems running this and editing the files with PyCharm, I guess because PyCharm keeps the changes
saved all the time and that messes up with the changes detection.

### Adding or modifying permissions assigned to user groups

The idea is to keep all the instances with the same permissions structure.
To do so we need data migrations that create or modify the groups whenever something change, i.e. adding a new model.

Note: when a m2m field without a through is migrated to one with a through table, even if the new through model's table
is the same than before, users will need specific permissions to continue being able to see and use this m2m relation.

In order to keep things simple, the data migration always replace everything, therefore, contains all the permissions
assigned to groups.

Locate the last groups update migration (user_groups in the filename, usually).

Create a new empty migration and replicate the code there, making the changes you want.
Make sure you add the function in the "operations" list.

Run migrate and commit the new migration.

# Installed packages

[ To do: add them all and clean unused ones ]

## dynamic-fields

https://gitlab.com/dannosaur/django-dynamic-form-fields

Enables dropdowns that filter its content according to another dropdown.
We use them when selecting Axis and Sub-axis.

## Django-Q

Package for handling scheduled tasks.
We're using it in a very simple way to execute the *mailqueue* command
`send_queued_messages`.

This tutorial is helpful to understand the setup:
https://mattsegal.dev/simple-scheduled-tasks.html

Then, the process is launched by having one docker container instance for each
ateneu, each suffixed as "automation".

# Commands

Added two commands for the monitoring dashboard:

`python manage.py mailqueue --pending`
`python manage.py mailqueue --sent-24`

## Dockerització per desenvolupament i pel servidor de develop

La carpeta /docker conté la dockerització que necessites aixecar per
treballar amb el projecte, i és la mateixa que aixequem al servidor de develop
quan volem que l'usuari entri a fer proves abans d'una release a producció.

La dockerització de develop monta la carpeta /src dins de la imatge de manera
que quan facis canvis al codi automàticament es reflecteixin a la imatge i això
farà que el gunicorn reiniciï l'aplicació al moment.

El docker-compose per aixecar el servidor de develop és al fitxer `compose-dev.yml`.
Aquest compose crea un contenidor de la imatge a un stage concret, és a dir:
tant producció com develop fan servir la mateixa imatge, però el compose indica
a quin stage de la imatge s'ha d'aturar.
Això ho pots veure al `compose-dev.yml` on fa el build, a:
`target: development`

Per aixecar-lo cal fer:
`docker-compose -f compose-dev.yml up`

# Dockerització per producció

A `/docker` hi ha el Dockerfile per generar la imatge de producció.
També hi ha un docker-compose per comprovar-la al fitxer `compose-prod.yml`.

Com s'explica més amunt, hi ha un sol Dockerfile i diversos composes.
En el cas del compose per producció hi ha la línia:
`target: production`
On especifica que el contenidor s'ha d'aturar en aquest stage de la imatge.

## Generar la imatge manualment

Fer això servirà per verificar que la build funcionarà abans de fer que
Dockerhub la generi automàticament i potencialment falli.

Des de la carpeta arrel del projecte:
`docker build -f docker/Dockerfile .`

Amb això estem dient-li que generi la imatge en el context de la carpeta actual
(per això el punt la final) però fent servir el Dockerfile que li especifiquem.

## Generar la imatge a Dockerhub

El repositori a dockerhub està configurat de manera que sempre que hi hagi un
push a la branch `main` generi una nova imatge.

Accedeix al compte de dockerhub per veure quines imatges hi ha generades, si
l'última ja s'ha generat o ha fallat, etc.

Si la vols pujar manualment:
1. Crear la imatge, des de la carpeta /docker:
`docker build --compress --target production --tag codicoop/ateneus:latest --file Dockerfile ../`

2. Fer `docker login` si no has fet abans.
3. Pujar la imatge:
`docker push codicoop/ateneus:latest`

## Testejar la imatge de producció en local o a develop
Assumint que tens l'última versió a dockerhub, fes:
`docker-compose -f compose-develop-hub.yml up`