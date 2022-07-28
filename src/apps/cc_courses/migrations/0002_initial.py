# Generated by Django 3.2.14 on 2022-07-28 11:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cc_courses', '0001_initial'),
        ('coopolis', '0001_initial'),
        ('facilities_reservations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='courseplace',
            name='town',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='coopolis.town', verbose_name='població'),
        ),
        migrations.AddField(
            model_name='course',
            name='place',
            field=models.ForeignKey(blank=True, help_text="Aquesta dada de moment és d'ús intern i no es publica.", null=True, on_delete=django.db.models.deletion.SET_NULL, to='cc_courses.courseplace', verbose_name='lloc'),
        ),
        migrations.AddField(
            model_name='activityresourcefile',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='cc_courses.activity'),
        ),
        migrations.AddField(
            model_name='activityenrolled',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='cc_courses.activity', verbose_name='sessió'),
        ),
        migrations.AddField(
            model_name='activityenrolled',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to=settings.AUTH_USER_MODEL, verbose_name='persona'),
        ),
        migrations.AddField(
            model_name='activity',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='cc_courses.course', verbose_name='acció'),
        ),
        migrations.AddField(
            model_name='activity',
            name='enrolled',
            field=models.ManyToManyField(blank=True, related_name='enrolled_activities', through='cc_courses.ActivityEnrolled', to=settings.AUTH_USER_MODEL, verbose_name='inscrites'),
        ),
        migrations.AddField(
            model_name='activity',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cc_courses.entity', verbose_name='entitat'),
        ),
        migrations.AddField(
            model_name='activity',
            name='minors_teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='docent'),
        ),
        migrations.AddField(
            model_name='activity',
            name='organizer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cc_courses.organizer', verbose_name='organitzadora'),
        ),
        migrations.AddField(
            model_name='activity',
            name='place',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cc_courses.courseplace', verbose_name='lloc'),
        ),
        migrations.AddField(
            model_name='activity',
            name='responsible',
            field=models.ForeignKey(blank=True, help_text="Persona de l'equip al càrrec de la sessió. Per aparèixer al desplegable, cal que la persona tingui activada l'opció 'Membre del personal'.", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activities_responsible', to=settings.AUTH_USER_MODEL, verbose_name='persona responsable'),
        ),
        migrations.AddField(
            model_name='activity',
            name='room',
            field=models.ForeignKey(blank=True, help_text='Si selecciones una sala, quan guardis quedarà reservada per la sessió. <br>Consulta el <a href="/reservations/calendar/" target="_blank">CALENDARI DE RESERVES</a> per veure la disponibilitat.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activities', to='facilities_reservations.room', verbose_name='sala'),
        ),
        migrations.AddField(
            model_name='activity',
            name='room_reservation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_activities', to='facilities_reservations.reservation'),
        ),
        migrations.AlterUniqueTogether(
            name='activityenrolled',
            unique_together={('user', 'activity')},
        ),
    ]
