# Comunalitats: Back office

Aplicació web per gestionar l'activitat de les comunalitats, facilitant la 
inscripció de les participants i la justificació de la convocatòria.

## Prepare the develop environment

*⚠ For the file and image uploads to work, set a `DJANGO_SETTINGS_MODULE` environment variable pointing to a config
module that sets `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` values.*

*⚠ If you get the "failed to load a library: cairo" when generating attendees lists, it's because of Weasyprint,
which uses Cairo.
You need to install Weasyprint in your system following the [official website's instruccions](https://weasyprint.readthedocs.io/en/stable/install.html#macos).

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

L'objectiu és tenir dues imatges per cada release:

- codi.coop/comunalitats:latest
- codi.coop/comunalitats:release-22.03.002 (versió corresponent a la tag)

Quan es fa una release s'ha de crear una card al Trello fent servir la plantilla
que hi ha amb la llista de passos que cal seguir, i en aquesta plantilla ja
s'hi inclouen els passos per generar això.

### Per generar la imatge :latest

El repositori a dockerhub està configurat de manera que sempre que hi hagi un
push a la branch `main` generi una nova imatge.

Accedeix al compte de dockerhub per veure quines imatges hi ha generades, si
l'última ja s'ha generat o ha fallat, etc.

Si la vols pujar manualment:
1. Crear la imatge, des de la carpeta /docker:
`docker build --compress --target production --tag codicoop/comunalitats:latest --file Dockerfile ../`

2. Fer `docker login` si no has fet abans.
3. Pujar la imatge:
`docker push codicoop/comunalitats:latest`

### Per generar la imatge :release-*tag*

Tenint la versió final a la branch main, obrir el repositori a Github i anar a Tags - Releases - New release.

A Choose a tag, desplegar i escriure el nom que tindrà el nou tag seguint la 
nomenclatura:
**v22.02.001** on **22.02** son l'any i el mes de release, i **001** el nº de release dins del mateix mes.

A Target triar Main.

Com a títol el que creguis, p.ex. 'Canvis d'abril de 2022'.

Clicar a Publish Release.

La creació de la imatge es dispararà, ara cal que entris al cap d'uns 10 minuts
a hub.docker.com per comprovar que s'ha generat sense errors.

## Testejar la imatge de producció en local o a develop
Assumint que tens l'última versió a dockerhub, fes:
`docker-compose -f compose-develop-hub.yml up`