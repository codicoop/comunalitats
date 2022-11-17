# Generated by Django 3.2.14 on 2022-11-17 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SubsidyPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True, verbose_name='nom')),
                ('date_start', models.DateField(verbose_name="dia d'inici")),
                ('date_end', models.DateField(verbose_name='dia de finalització')),
                ('number', models.CharField(blank=True, max_length=50, null=True, verbose_name="número d'expedient")),
            ],
            options={
                'verbose_name': 'convocatòria',
                'verbose_name_plural': 'convocatòries',
                'ordering': ['-date_start'],
            },
        ),
        migrations.CreateModel(
            name='DataExports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creació')),
                ('name', models.CharField(max_length=200, verbose_name='nom')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='apunts')),
                ('function_name', models.CharField(help_text='No modifiqueu aquesta dada.', max_length=150, verbose_name='nom de la funció')),
                ('ignore_errors', models.BooleanField(default=False, help_text="Si s'activa, es podràn generar els excels de justificació encara que hi hagi errors a les dades. Els excels que es generin així NO es podran volcar a l'excel real!", verbose_name='Ignorar errors')),
                ('subsidy_period', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dataexports.subsidyperiod', verbose_name='convocatòria')),
            ],
            options={
                'verbose_name': 'exportació',
                'verbose_name_plural': 'exportacions',
                'ordering': ['subsidy_period'],
                'unique_together': {('name', 'subsidy_period')},
            },
        ),
    ]
