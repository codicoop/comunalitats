# Generated by Django 2.1.3 on 2019-03-06 16:03

import coopolis.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0002_auto_20190225_1748'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectStage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.CharField(choices=[('REQUESTED', 'Acompanyament sol·licitat'), ('CONSTITUTION', 'Constitució'), ('CONSOLIDATION', 'Consolidació')], default='REQUESTED', max_length=50, verbose_name="Fase de l'acompanyament")),
                ('subsidy_period', models.CharField(blank=True, choices=[('2018', '2017-2018'), ('2019', '2018-2019')], max_length=4, null=True, verbose_name='Convocatòria')),
                ('date_start', models.DateField(blank=True, null=True, verbose_name="Data d'inici")),
                ('date_end', models.DateField(blank=True, null=True, verbose_name='Data de finalització')),
                ('follow_up', models.TextField(blank=True, null=True, verbose_name='Seguiment')),
                ('axis', models.CharField(blank=True, choices=[('B', 'Eix B'), ('C', 'Eix C'), ('D', 'Eix D')], help_text='Eix de la convocatòria on es justificarà.', max_length=1, null=True, verbose_name='Eix')),
                ('organizer', models.CharField(choices=[('AT', 'Ateneu'), ('CM', 'Cercle Migracions'), ('CI', 'Cercle Incubació'), ('CC', 'Cercle Consum')], max_length=2, verbose_name='Qui ho fa')),
                ('scanned_signatures', models.FileField(blank=True, max_length=250, null=True, upload_to=coopolis.models.stage_signatures_upload_path, verbose_name='Document amb signatures')),
                ('involved_partners', models.ManyToManyField(related_name='stage_involved_partners', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Fase',
                'verbose_name_plural': 'Fases',
            },
        ),
        migrations.AlterField(
            model_name='project',
            name='motivation',
            field=models.CharField(blank=True, choices=[('COOPERATIVISM_EDUCATION', 'Formació en cooperativisme'), ('COOPERATIVE_CREATION', "Constitució d'una cooperativa"), ('TRANSFORM_FROM_ASSOCIATION', "Transformació d'associació a coopetiva"), ('TRANSFORM_FROM_SCP', 'Transformació de SCP a coopertiva'), ('ENTERPRISE_RELIEF', 'Relleu empresarial'), ('CONSOLIDATION', 'Consolidació'), ('OTHER', 'Altres')], max_length=50, null=True, verbose_name='Petició inicial'),
        ),
        migrations.AlterField(
            model_name='project',
            name='subsidy_period',
            field=models.CharField(blank=True, choices=[('2018', '2017-2018'), ('2019', '2018-2019')], max_length=4, null=True, verbose_name='Convocatòria'),
        ),
        migrations.AddField(
            model_name='projectstage',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coopolis.Project'),
        ),
    ]
