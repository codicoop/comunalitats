# Generated by Django 2.2.7 on 2021-01-11 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cc_courses', '0045_auto_20200807_1616'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organizer',
            options={'ordering': ['name'], 'verbose_name': 'organitzadora', 'verbose_name_plural': 'organitzadores'},
        ),
    ]
