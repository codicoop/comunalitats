# Generated by Django 2.2.7 on 2021-03-26 12:45

import coopolis.storage_backends
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0082_auto_20210326_1319'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(storage=coopolis.storage_backends.PublicMediaStorage(), upload_to='', verbose_name='fitxer')),
                ('name', models.CharField(max_length=120, verbose_name='nom del fitxer')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='coopolis.Project')),
            ],
            options={
                'verbose_name': 'fitxer',
                'verbose_name_plural': 'fitxers',
                'ordering': ['name'],
            },
        ),
    ]
