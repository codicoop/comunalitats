# Generated by Django 2.0 on 2019-09-24 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facilities_reservations', '0004_auto_20190923_1441'),
        ('cc_courses', '0023_activity_room_reservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activities', to='facilities_reservations.Room', verbose_name='sala'),
        ),
    ]
