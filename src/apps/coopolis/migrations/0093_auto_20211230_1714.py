# Generated by Django 3.2.9 on 2021-12-30 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0092_auto_20211222_1237'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectsConstitutedService',
            fields=[
            ],
            options={
                'verbose_name': 'Projecte constituït',
                'verbose_name_plural': 'Projectes constituïts',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('coopolis.project',),
        ),
        migrations.CreateModel(
            name='ProjectsFollowUpService',
            fields=[
            ],
            options={
                'verbose_name': "Seguiment d'acompanyament",
                'verbose_name_plural': "Seguiment d'acompanyaments",
                'ordering': ['follow_up_situation', 'follow_up_situation_update'],
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('coopolis.project',),
        ),
        migrations.AlterModelOptions(
            name='projectsconstituted',
            options={'verbose_name': '(obsolet) Projecte constituït per eix', 'verbose_name_plural': '(obsolet) Projectes constituïts per eix'},
        ),
        migrations.AlterModelOptions(
            name='projectsfollowup',
            options={'ordering': ['follow_up_situation', 'follow_up_situation_update'], 'verbose_name': "(obsolet) Seguiment d'acompanyament per eix", 'verbose_name_plural': "(obsolet) Seguiment d'acompanyaments per eix"},
        ),
        migrations.RemoveField(
            model_name='projectstage',
            name='covid_crisis',
        ),
    ]
