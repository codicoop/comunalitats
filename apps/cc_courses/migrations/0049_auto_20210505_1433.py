# Generated by Django 2.2.7 on 2021-05-05 14:33

from django.db import migrations
import uuid


def gen_uuid(apps, schema_editor):
    MyModel = apps.get_model('cc_courses', 'Activity')
    for row in MyModel.objects.all():
        row.uuid = uuid.uuid4()
        row.save(update_fields=['uuid'])


class Migration(migrations.Migration):

    dependencies = [
        ('cc_courses', '0048_activity_uuid'),
    ]

    operations = [
        migrations.RunPython(gen_uuid),
    ]
