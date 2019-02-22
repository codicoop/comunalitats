# Generated by Django 2.1.3 on 2019-02-20 12:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cc_courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalentity',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalcourseplace',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalcourse',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalactivity',
            name='course',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='cc_courses.Course', verbose_name='Formació / Programa'),
        ),
        migrations.AddField(
            model_name='historicalactivity',
            name='entity',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='cc_courses.Entity'),
        ),
        migrations.AddField(
            model_name='historicalactivity',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalactivity',
            name='place',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='cc_courses.CoursePlace', verbose_name='Lloc'),
        ),
        migrations.AddField(
            model_name='activity',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cc_courses.Course', verbose_name='Formació / Programa'),
        ),
        migrations.AddField(
            model_name='activity',
            name='enrolled',
            field=models.ManyToManyField(blank=True, related_name='enrolled_activities', to=settings.AUTH_USER_MODEL, verbose_name='Inscrites'),
        ),
        migrations.AddField(
            model_name='activity',
            name='entity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cc_courses.Entity'),
        ),
        migrations.AddField(
            model_name='activity',
            name='place',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cc_courses.CoursePlace', verbose_name='Lloc'),
        ),
    ]
