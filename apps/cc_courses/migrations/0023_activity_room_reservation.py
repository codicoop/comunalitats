# Generated by Django 2.0 on 2019-09-23 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facilities_reservations', '0004_auto_20190923_1441'),
        ('cc_courses', '0022_activity_subaxis'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='room_reservation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='facilities_reservations.Reservation'),
        ),
    ]
