# Generated by Django 2.2.7 on 2020-06-16 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataexports', '0013_auto_20200122_1000'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subsidyperiod',
            options={'ordering': ['-date_start'], 'verbose_name': 'convocatòria', 'verbose_name_plural': 'convocatòries'},
        ),
    ]
