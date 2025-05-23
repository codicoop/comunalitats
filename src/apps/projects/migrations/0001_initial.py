# Generated by Django 3.2.14 on 2022-11-28 15:56

import apps.coopolis.storage_backends
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tagulous.models.fields
import tagulous.models.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cc_courses', '0004_auto_20221122_1853'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dataexports', '0001_initial'),
        ('towns', '0002_load_town_fixtures'),
    ]

    operations = [
        migrations.CreateModel(
            name='Derivation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='nom')),
            ],
            options={
                'verbose_name': 'derivació',
                'verbose_name_plural': 'derivacions',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='nom')),
                ('sector', models.CharField(choices=[('M', 'Alimentació'), ('S', 'Assessorament'), ('A', 'Altres'), ('C', 'Comunicació i tecnologia'), ('CU', 'Cultura'), ('U', 'Cures'), ('E', 'Educació'), ('F', 'Finances'), ('H', 'Habitatge'), ('L', 'Logística'), ('O', 'Oci'), ('R', 'Roba')], max_length=2)),
                ('web', models.CharField(blank=True, max_length=200, verbose_name='Web')),
                ('project_status', models.CharField(blank=True, choices=[('IN_MEDITATION_PROCESS', 'En proces de debat/reflexió'), ('IN_CONSTITUTION_PROCESS', 'En constitució'), ('RUNNING', 'Constituïda'), ('DOWN', 'Caigut')], max_length=50, null=True, verbose_name='estat del projecte')),
                ('motivation', models.CharField(blank=True, choices=[('COOPERATIVISM_EDUCATION', 'Formació en cooperativisme'), ('COOPERATIVE_CREATION', "Constitució d'una cooperativa"), ('TRANSFORM_FROM_ASSOCIATION', "Transformació d'associació a cooperativa"), ('TRANSFORM_FROM_SCP', 'Transformació de SCP a cooperativa'), ('ENTERPRISE_RELIEF', 'Relleu empresarial'), ('CONSOLIDATION', 'Consolidació'), ('OTHER', 'Altres')], max_length=50, null=True, verbose_name='petició inicial')),
                ('mail', models.EmailField(max_length=254, verbose_name='correu electrònic')),
                ('phone', models.CharField(max_length=25, verbose_name='telèfon')),
                ('neighborhood', models.CharField(blank=True, default='', max_length=50, verbose_name='Barri')),
                ('number_people', models.IntegerField(blank=True, null=True, verbose_name='número de persones')),
                ('registration_date', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='data de registre')),
                ('cif', models.CharField(blank=True, max_length=11, null=True, verbose_name='N.I.F.')),
                ('object_finality', models.TextField(blank=True, null=True, verbose_name='objecte i finalitat')),
                ('project_origins', models.TextField(blank=True, null=True, verbose_name='orígens del projecte')),
                ('solves_necessities', models.TextField(blank=True, null=True, verbose_name='quines necessitats resol el vostre projecte?')),
                ('social_base', models.TextField(blank=True, null=True, verbose_name='compta el vostre projecte amb una base social?')),
                ('constitution_date', models.DateField(blank=True, null=True, verbose_name='data de constitució')),
                ('estatuts', models.FileField(blank=True, max_length=250, null=True, storage=apps.coopolis.storage_backends.PrivateMediaStorage(), upload_to='', verbose_name='estatuts')),
                ('viability', models.FileField(blank=True, max_length=250, null=True, storage=apps.coopolis.storage_backends.PrivateMediaStorage(), upload_to='', verbose_name='pla de viabilitat')),
                ('sostenibility', models.FileField(blank=True, max_length=250, null=True, storage=apps.coopolis.storage_backends.PrivateMediaStorage(), upload_to='', verbose_name='pla de sostenibilitat')),
                ('derivation_date', models.DateField(blank=True, null=True, verbose_name='data de derivació')),
                ('description', models.TextField(blank=True, null=True, verbose_name='descripció')),
                ('other', models.CharField(blank=True, help_text="Apareix a la taula de Seguiment d'Acompanyaments", max_length=240, null=True, verbose_name='altres')),
                ('employment_estimation', models.PositiveIntegerField(default=0, verbose_name='insercions laborals previstes')),
                ('follow_up_situation', models.CharField(blank=True, choices=[('PENDENT', 'Pendent d’enviar proposta de trobada'), ('ENVIAT', 'Enviat email amb proposta de data per trobar-nos'), ('CONCERTADA', 'Data de trobada concertada'), ('ACOLLIT', 'Acollida realitzada'), ('PAUSA', 'Acompanyament en pausa'), ('CANCEL', 'Acompanyament cancel·lat')], max_length=50, null=True, verbose_name='seguiment')),
                ('follow_up_situation_update', models.DateTimeField(blank=True, null=True, verbose_name='actualització seguiment')),
                ('derivation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.derivation', verbose_name='derivat')),
                ('partners', models.ManyToManyField(blank=True, related_name='projects', to=settings.AUTH_USER_MODEL, verbose_name='sòcies')),
                ('subsidy_period', models.ForeignKey(blank=True, help_text="OPCIONAL. En cas que el projecte s'hagi constituït en una convocatòria posterior a l'ultima intervenció de la comunalitat, podeu indicar-ho aquí, per tal que aparegui a l'informe de Projectes Constituïts. Aquest camp NO farà aparèixer el projecte a l'excel de justificació (per aparèixer a l'excel cal crear una Justificació d'Acompanyament)", null=True, on_delete=django.db.models.deletion.SET_NULL, to='dataexports.subsidyperiod', verbose_name='convocatòria de la constitució')),
            ],
            options={
                'verbose_name': 'projecte',
                'verbose_name_plural': 'projectes',
            },
        ),
        migrations.CreateModel(
            name='ProjectStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage_type', models.CharField(choices=[('11', 'Creació'), ('12', 'Consolidació'), ('9', 'Incubació')], default=1, max_length=2, verbose_name="tipus d'acompanyament")),
                ('date_start', models.DateField(auto_now_add=True, verbose_name='data creació acompanyament')),
                ('service', models.SmallIntegerField(blank=True, choices=[(None, 'Cap'), (10, "A) Serveis d'anàlisis i prospectiva"), (20, "B) Servei de formació i difusió per a l'activisme"), (30, "C) Servei de formació per a la creació i l'establiment de projectes d'ajuda mútua"), (40, "D) Servei per a la creació i consolidació de projectes d'ajuda mútua, d'intercooperació i de cooperació entre els bens comuns urbans i la ciutadania"), (50, "E) Punt de trobada i d'informació de comunalitat urbana")], null=True, verbose_name='Servei')),
                ('sub_service', models.SmallIntegerField(blank=True, choices=[(None, 'Cap'), (101, "A.1) Articulació i posada en funcionament de l'Assemblea de la Comunalitat"), (102, 'A.2) Identificació i incorporació dels béns comuns urbans, de les organitzacions, els col.lectius i els representants'), (103, "A.3) Creació o manteniment i difusió d'un recurs/ eina per visualitzar béns comuns i projectes d'ajuda mútua assolits. "), (104, "A.4) Elaboració d'un catàleg d'exemples de bones pràctiques d'ajuda mútua i ESS. Identificar i elaborar fitxes de bones pràctiques i iniciatives"), (105, 'A.5) Organització de jornades i accions directes a la comunalitat per visualitzar experiències; fires,actes, presència als mitjans de comunicació. '), (106, "A.6) Organització logística i metodològica de jornades pròpies per presentar bones pràctiques, parlar de temes sectorials o d'interés per el territori"), (107, "A.7) Participació o colaboració a actes, jornades, fires, publicacions amb l'objectiu de presentar el programa, visibilitzar experiències,organitzar tallers, publicar notes de premsa o articles opinió"), (108, "A.8) Altres accions dins el servei d'anàlisi i prospectiva "), (201, "B.1) Campanya de comunicació i difusió a col.lectius d'especial atenció"), (202, 'B.2) Elaboració de material especific i difusió dels materials'), (203, "B.3) Activitats anuals de dinamització  i activació de l'autoorganització col.lectiva per  a la generació de projectes"), (204, 'B.4)Tallers adreçats preferentment als joves o a la ciutadania de la comunalitat.'), (205, "B.5) Altres accions dins el servei de formació i difusió per a l'activisme al barri/espai urbà"), (301, "C.1) Activitats formatives i informatives per a la creció d'aliances "), (302, 'C.2) Organització de formació bàsica o dinamització destinades a persones o entitats interessades en la fórmula de colaboració, ajuda mutua o intercooperació'), (303, "C.3) Organització de sessions col.lectives i individuals per al disseny d'estratègies vinculades a l'autoorganització i intercooperació"), (304, "C.4) Activitats destinades a fomentar la col.laboració entre empreses de l'economia social i cooperativa del territori"), (305, 'C.5) Organització i acompanyament a les empreses/entitats participants en la primera fase de coordinació del projecte. '), (306, 'C.6) Elaboració i difusió de materials destinat a empreses, associassions i entitats sobre ajuda mútua i ESS'), (307, 'C.7) Tallers de sensibilització/dinamització destinats al teixit associatiu i a les empreses per donar a conèixer projectes '), (308, "C.8) Tallers de sensibilització/dinamització adreçats a professionals que s'agrupin de manera conjunta"), (309, "C.9) Altres accions dins el servei de formació per a la creació i establiment de projectes d'ajuda"), (401, "D.1) Creació d'espais d'intercooperació dins els territoris de referència per la generació de nous models econòmics"), (402, "D.2) Incorporació d'empreses, cooperatives i entitats ESS en els béns comuns urbans"), (403, 'D.3) Activitats de treball en xarxa amb altres comunalitats urbanes del programa '), (404, "D.4) Altres accions dins el servei per a la creació i consolidació de projectes d'ajuda mútua"), (501, "E.1) Atenció als usuaris a l'espai físic de referència"), (502, "E.2) Difusió del punt d'informació")], null=True, verbose_name='Sub-servei')),
                ('scanned_certificate', models.FileField(blank=True, max_length=250, null=True, storage=apps.coopolis.storage_backends.PrivateMediaStorage(), upload_to='', verbose_name='Certificat')),
                ('involved_partners', models.ManyToManyField(blank=True, help_text="Persones que apareixeran a la justificació com a que han participat a l'acompanyament.", related_name='stage_involved_partners', to=settings.AUTH_USER_MODEL, verbose_name='(obsolet) Persones involucrades')),
                ('organizer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cc_courses.organizer', verbose_name='organitzadora')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stages', to='projects.project', verbose_name='projecte acompanyat')),
                ('responsible', models.ForeignKey(blank=True, help_text="Persona de l'equip al càrrec de l'acompanyament. Per aparèixer al desplegable, cal que la persona tingui activada la opció 'Membre del personal'.", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stage_responsible', to=settings.AUTH_USER_MODEL, verbose_name='persona responsable')),
            ],
            options={
                'verbose_name': "justificació d'acompanyament",
                'verbose_name_plural': "justificacions d'acompanyaments",
                'ordering': ['-date_start'],
            },
        ),
        migrations.CreateModel(
            name='StageSubtype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='nom')),
            ],
            options={
                'verbose_name': 'subtipus',
                'verbose_name_plural': 'subtipus',
            },
        ),
        migrations.CreateModel(
            name='Tagulous_Project_tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                ('count', models.IntegerField(default=0, help_text='Internal counter of how many times this tag is in use')),
                ('protected', models.BooleanField(default=False, help_text='Will not be deleted when the count reaches 0')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
                'unique_together': {('slug',)},
            },
            bases=(tagulous.models.models.BaseTagModel, models.Model),
        ),
        migrations.CreateModel(
            name='ProjectStageSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today, null=True, verbose_name='data')),
                ('hours', models.FloatField(blank=True, help_text='Camp necessari per la justificació.', null=True, verbose_name="número d'hores")),
                ('follow_up', models.TextField(blank=True, null=True, verbose_name='seguiment')),
                ('justification_file', models.FileField(blank=True, null=True, storage=apps.coopolis.storage_backends.PrivateMediaStorage(), upload_to='', verbose_name='fitxer de justificació')),
                ('entity', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cc_courses.entity', verbose_name='Entitat')),
                ('involved_partners', models.ManyToManyField(blank=True, help_text="Persones que apareixeran a la justificació com a que han participat a la sessió d'acompanyament.", related_name='stage_sessions_participated', to=settings.AUTH_USER_MODEL, verbose_name='persones involucrades')),
                ('project_stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stage_sessions', to='projects.projectstage', verbose_name="justificació d'acompanyament")),
                ('session_responsible', models.ForeignKey(blank=True, help_text="Persona de l'equip que ha facilitat la sessió. Per aparèixer al desplegable, cal que la persona tingui activada la opció 'Membre del personal'.", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stage_sessions', to=settings.AUTH_USER_MODEL, verbose_name='persona facilitadora')),
            ],
            options={
                'verbose_name': "Sessió d'acompanyament",
                'verbose_name_plural': "Sessions d'acompanyament",
            },
        ),
        migrations.AddField(
            model_name='projectstage',
            name='stage_subtype',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.stagesubtype', verbose_name='subtipus'),
        ),
        migrations.AddField(
            model_name='projectstage',
            name='subsidy_period',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dataexports.subsidyperiod', verbose_name='convocatòria'),
        ),
        migrations.CreateModel(
            name='ProjectFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(max_length=250, storage=apps.coopolis.storage_backends.PublicMediaStorage(), upload_to='', verbose_name='fitxer')),
                ('name', models.CharField(help_text="Els fitxers antics tenen com a etiqueta el propi nom de l'arxiu, però aquí hi pot anar qualsevol text descriptiu.", max_length=250, verbose_name='Etiqueta')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='projects.project')),
            ],
            options={
                'verbose_name': 'fitxer',
                'verbose_name_plural': 'fitxers',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='project',
            name='tags',
            field=tagulous.models.fields.TagField(_set_tag_meta=True, blank=True, force_lowercase=True, help_text='Prioritza les etiquetes que apareixen auto-completades. Si escrius una etiqueta amb un espai creurà que son dues etiquetes, per evitar-ho escriu-la entre cometes dobles, "etiqueta amb espais".', to='projects.Tagulous_Project_tags', verbose_name='etiquetes'),
        ),
        migrations.AddField(
            model_name='project',
            name='town',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='towns.town', verbose_name='població'),
        ),
        migrations.CreateModel(
            name='EmploymentInsertion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insertion_date', models.DateField(verbose_name='alta seguretat social')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='baixa seg. social')),
                ('contract_type', models.SmallIntegerField(choices=[(1, 'Indefinit'), (5, 'Temporal'), (2, 'Soci/a cooperativa o societat laboral'), (3, 'Autònom')], null=True, verbose_name='tipus de contracte')),
                ('entity_name', models.CharField(max_length=150, verbose_name="Nom de l'entitat on s'insereix")),
                ('entity_nif', models.CharField(max_length=11, verbose_name="NIF de l'entitat on s'insereix")),
                ('entity_neighborhood', models.CharField(max_length=50, verbose_name="Barri de l'entitat on s'insereix")),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employment_insertions', to='cc_courses.activity', verbose_name="activitat relacionada amb l'inserció")),
                ('entity_town', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='towns.town', verbose_name="població de l'entitat on s'insereix")),
                ('subsidy_period', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dataexports.subsidyperiod', verbose_name='convocatòria')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='persona')),
            ],
            options={
                'verbose_name': 'inserció laboral',
                'verbose_name_plural': 'insercions laborals',
                'ordering': ['-insertion_date'],
            },
        ),
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
            bases=('projects.project',),
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
            bases=('projects.project',),
        ),
    ]
