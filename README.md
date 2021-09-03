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

# Commands

Added two commands for the monitoring dashboard:

`python manage.py mailqueue --pending`
`python manage.py mailqueue --sent-24`

