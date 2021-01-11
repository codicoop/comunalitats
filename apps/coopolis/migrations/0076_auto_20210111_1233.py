# Generated by Django 2.2.7 on 2021-01-11 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0075_auto_20201008_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employmentinsertion',
            name='contract_type',
            field=models.SmallIntegerField(choices=[(1, 'Indefinit'), (5, 'Temporal'), (2, 'Formació i aprenentatge'), (3, 'Pràctiques'), (4, 'Soci/a cooperativa o societat laboral')], null=True, verbose_name='tipus de contracte'),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_status',
            field=models.CharField(blank=True, choices=[('IN_MEDITATION_PROCESS', 'En proces de debat/reflexió'), ('IN_CONSTITUTION_PROCESS', 'En constitució'), ('RUNNING', 'Constituïda'), ('DOWN', 'Caigut')], max_length=50, null=True, verbose_name='estat del projecte'),
        ),
    ]
