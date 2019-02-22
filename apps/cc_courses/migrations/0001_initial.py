# Generated by Django 2.1.3 on 2019-02-20 12:31

import cc_courses.models
from django.db import migrations, models
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Títol')),
                ('objectives', models.TextField(null=True, verbose_name='Descripció')),
                ('date_start', models.DateField(verbose_name='Dia inici')),
                ('date_end', models.DateField(blank=True, null=True, verbose_name='Dia finalització')),
                ('starting_time', models.TimeField(verbose_name="Hora d'inici")),
                ('ending_time', models.TimeField(verbose_name='Hora de finalització')),
                ('spots', models.IntegerField(default=0, verbose_name='Places totals')),
                ('organizer', models.TextField(choices=[('AT', 'Ateneu'), ('CM', 'Cercle Migracions'), ('CI', 'Cercle Incubació'), ('CC', 'Cercle Consum')], verbose_name='Qui ho organitza')),
                ('axis', models.TextField(choices=[('A', 'Eix A'), ('B', 'Eix B'), ('C', 'Eix C'), ('D', 'Eix D')], help_text='Eix de la convocatòria on es justificarà.', verbose_name='Eix')),
                ('published', models.BooleanField(default=True, verbose_name='Publicada')),
            ],
            options={
                'verbose_name': 'Activitat',
                'ordering': ['date_start'],
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Títol')),
                ('slug', models.CharField(max_length=100, unique=True)),
                ('date_start', models.DateField(verbose_name='Dia inici')),
                ('date_end', models.DateField(verbose_name='Dia finalització')),
                ('hours', models.CharField(help_text='Indica només els horaris, sense els dies.', max_length=200, verbose_name='Horaris')),
                ('description', models.TextField(null=True, verbose_name='Descripció')),
                ('published', models.BooleanField(verbose_name='Publicat')),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('banner', models.ImageField(max_length=250, null=True, upload_to=cc_courses.models.upload_path)),
            ],
            options={
                'verbose_name': 'Formació',
                'verbose_name_plural': 'Formacions',
                'ordering': ['date_start'],
            },
        ),
        migrations.CreateModel(
            name='CoursePlace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Nom')),
                ('address', models.CharField(max_length=200, verbose_name='Adreça')),
            ],
            options={
                'verbose_name': 'Lloc',
            },
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Nom')),
                ('legal_id', models.CharField(max_length=9, verbose_name='C.I.F.')),
            ],
            options={
                'verbose_name': 'Entitat',
            },
        ),
        migrations.CreateModel(
            name='HistoricalActivity',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Títol')),
                ('objectives', models.TextField(null=True, verbose_name='Descripció')),
                ('date_start', models.DateField(verbose_name='Dia inici')),
                ('date_end', models.DateField(blank=True, null=True, verbose_name='Dia finalització')),
                ('starting_time', models.TimeField(verbose_name="Hora d'inici")),
                ('ending_time', models.TimeField(verbose_name='Hora de finalització')),
                ('spots', models.IntegerField(default=0, verbose_name='Places totals')),
                ('organizer', models.TextField(choices=[('AT', 'Ateneu'), ('CM', 'Cercle Migracions'), ('CI', 'Cercle Incubació'), ('CC', 'Cercle Consum')], verbose_name='Qui ho organitza')),
                ('axis', models.TextField(choices=[('A', 'Eix A'), ('B', 'Eix B'), ('C', 'Eix C'), ('D', 'Eix D')], help_text='Eix de la convocatòria on es justificarà.', verbose_name='Eix')),
                ('published', models.BooleanField(default=True, verbose_name='Publicada')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical Activitat',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalCourse',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Títol')),
                ('slug', models.CharField(db_index=True, max_length=100)),
                ('date_start', models.DateField(verbose_name='Dia inici')),
                ('date_end', models.DateField(verbose_name='Dia finalització')),
                ('hours', models.CharField(help_text='Indica només els horaris, sense els dies.', max_length=200, verbose_name='Horaris')),
                ('description', models.TextField(null=True, verbose_name='Descripció')),
                ('published', models.BooleanField(verbose_name='Publicat')),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('banner', models.TextField(max_length=250, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical Formació',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalCoursePlace',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, verbose_name='Nom')),
                ('address', models.CharField(max_length=200, verbose_name='Adreça')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical Lloc',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalEntity',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, verbose_name='Nom')),
                ('legal_id', models.CharField(max_length=9, verbose_name='C.I.F.')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical Entitat',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
