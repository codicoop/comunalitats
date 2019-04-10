# Generated by Django 2.1.3 on 2019-04-10 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cc_courses', '0006_course_place'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='place',
            field=models.ForeignKey(blank=True, help_text="Aquesta dada de moment és d'ús intern i no es publica.", null=True, on_delete=django.db.models.deletion.SET_NULL, to='cc_courses.CoursePlace', verbose_name='lloc'),
        ),
    ]
