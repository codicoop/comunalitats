# Generated by Django 3.2.14 on 2022-11-22 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cc_courses', '0003_activityfile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['title'], 'verbose_name': 'acció', 'verbose_name_plural': 'accions'},
        ),
        migrations.RemoveField(
            model_name='course',
            name='date_end',
        ),
        migrations.RemoveField(
            model_name='course',
            name='date_start',
        ),
        migrations.RemoveField(
            model_name='course',
            name='hours',
        ),
        migrations.RemoveField(
            model_name='course',
            name='place',
        ),
        migrations.RemoveField(
            model_name='course',
            name='publish',
        ),
    ]
