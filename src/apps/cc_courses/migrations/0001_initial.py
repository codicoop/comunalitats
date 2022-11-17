# Generated by Django 3.2.14 on 2022-11-17 17:43

import apps.coopolis.storage_backends
from django.db import migrations, models
import django.db.models.deletion
import easy_thumbnails.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0004_load_town_fixtures'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('name', models.CharField(max_length=200, verbose_name='títol')),
                ('objectives', models.TextField(null=True, verbose_name='descripció')),
                ('date_start', models.DateField(verbose_name='dia inici')),
                ('date_end', models.DateField(blank=True, null=True, verbose_name='dia finalització')),
                ('starting_time', models.TimeField(verbose_name="hora d'inici")),
                ('ending_time', models.TimeField(verbose_name='hora de finalització')),
                ('spots', models.IntegerField(default=0, help_text="Si hi ha inscripcions en llista d'espera i augmentes el número de places, passaran a confirmades i se'ls hi notificarà el canvi. Si redueixes el número de places per sota del total d'inscrites les que ja estaven confirmades seguiran confirmades. Aquestes autotatitzacions únicament s'activen si la sessió té una data futura.", verbose_name='places totals')),
                ('service', models.SmallIntegerField(blank=True, choices=[(None, 'Cap'), (10, "A) Serveis d'anàlisis i prospectiva"), (20, "B) Servei de formació i difusió per a l'activisme"), (30, "C) Servei de formació per a la creació i l'establiment de projectes d'ajuda mútua"), (40, "D) Servei per a la creació i consolidació de projectes d'ajuda mútua, d'intercooperació i de cooperació entre els bens comuns urbans i la ciutadania"), (50, "E) Punt de trobada i d'informació de comunalitat urbana")], null=True, verbose_name='Servei')),
                ('sub_service', models.SmallIntegerField(blank=True, choices=[(None, 'Cap'), (101, "A.1) Articulació i posada en funcionament de l'Assemblea de la Comunalitat"), (102, 'A.2) Identificació i incorporació dels béns comuns urbans, de les organitzacions, els col.lectius i els representants'), (103, "A.3) Creació o manteniment i difusió d'un recurs/ eina per visualitzar béns comuns i projectes d'ajuda mútua assolits. "), (104, "A.4) Elaboració d'un catàleg d'exemples de bones pràctiques d'ajuda mútua i ESS. Identificar i elaborar fitxes de bones pràctiques i iniciatives"), (105, 'A.5) Organització de jornades i accions directes a la comunalitat per visualitzar experiències; fires,actes, presència als mitjans de comunicació. '), (106, "A.6) Organització logística i metodològica de jornades pròpies per presentar bones pràctiques, parlar de temes sectorials o d'interés per el territori"), (107, "A.7) Participació o colaboració a actes, jornades, fires, publicacions amb l'objectiu de presentar el programa, visibilitzar experiències,organitzar tallers, publicar notes de premsa o articles opinió"), (108, "A.8) Altres accions dins el servei d'anàlisi i prospectiva "), (201, "B.1) Campanya de comunicació i difusió a col.lectius d'especial atenció"), (202, 'B.2) Elaboració de material especific i difusió dels materials'), (203, "B.3) Activitats anuals de dinamització  i activació de l'autoorganització col.lectiva per  a la generació de projectes"), (204, 'B.4)Tallers adreçats preferentment als joves o a la ciutadania de la comunalitat.'), (205, "B.5) Altres accions dins el servei de formació i difusió per a l'activisme al barri/espai urbà"), (301, "C.1) Activitats formatives i informatives per a la creció d'aliances "), (302, 'C.2) Organització de formació bàsica o dinamització destinades a persones o entitats interessades en la fórmula de colaboració, ajuda mutua o intercooperació'), (303, "C.3) Organització de sessions col.lectives i individuals per al disseny d'estratègies vinculades a l'autoorganització i intercooperació"), (304, "C.4) Activitats destinades a fomentar la col.laboració entre empreses de l'economia social i cooperativa del territori"), (305, 'C.5) Organització i acompanyament a les empreses/entitats participants en la primera fase de coordinació del projecte. '), (306, 'C.6) Elaboració i difusió de materials destinat a empreses, associassions i entitats sobre ajuda mútua i ESS'), (307, 'C.7) Tallers de sensibilització/dinamització destinats al teixit associatiu i a les empreses per donar a conèixer projectes '), (308, "C.8) Tallers de sensibilització/dinamització adreçats a professionals que s'agrupin de manera conjunta"), (309, "C.9) Altres accions dins el servei de formació per a la creació i establiment de projectes d'ajuda"), (401, "D.1) Creació d'espais d'intercooperació dins els territoris de referència per la generació de nous models econòmics"), (402, "D.2) Incorporació d'empreses, cooperatives i entitats ESS en els béns comuns urbans"), (403, 'D.3) Activitats de treball en xarxa amb altres comunalitats urbanes del programa '), (404, "D.4) Altres accions dins el servei per a la creació i consolidació de projectes d'ajuda mútua"), (501, "E.1) Atenció als usuaris a l'espai físic de referència"), (502, "E.2) Difusió del punt d'informació")], null=True, verbose_name='Sub-servei')),
                ('photo1', models.FileField(blank=True, max_length=250, null=True, storage=apps.coopolis.storage_backends.PrivateMediaStorage(), upload_to='', verbose_name='fotografia')),
                ('photo3', models.FileField(blank=True, max_length=250, null=True, storage=apps.coopolis.storage_backends.PrivateMediaStorage(), upload_to='', verbose_name='fotografia 2')),
                ('photo2', models.FileField(blank=True, max_length=250, null=True, storage=apps.coopolis.storage_backends.PrivateMediaStorage(), upload_to='', verbose_name='document acreditatiu')),
                ('file1', models.FileField(blank=True, max_length=250, null=True, storage=apps.coopolis.storage_backends.PrivateMediaStorage(), upload_to='', verbose_name='material de difusió')),
                ('publish', models.BooleanField(default=True, verbose_name='publicada')),
                ('for_minors', models.BooleanField(default=False, help_text="Determina el tipus de justificació i en aquest cas, s'han d'omplir els camps relatius a menors.", verbose_name='acció dirigida a menors')),
                ('minors_school_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='nom del centre educatiu')),
                ('minors_school_cif', models.CharField(blank=True, max_length=12, null=True, verbose_name='CIF del centre educatiu')),
                ('minors_grade', models.CharField(blank=True, choices=[('PRIM', 'Primària'), ('ESO', 'Secundària obligatòria'), ('BATX', 'Batxillerat'), ('FPGM', 'Formació professional grau mig'), ('FPGS', 'Formació professional grau superior')], max_length=4, null=True, verbose_name="grau d'estudis")),
                ('minors_participants_number', models.IntegerField(blank=True, null=True, verbose_name="número d'alumnes participants")),
                ('videocall_url', models.URLField(blank=True, max_length=250, null=True, verbose_name='enllaç a la videotrucada')),
                ('instructions', models.TextField(blank=True, help_text='Aquest text s\'inclourà al correu de recordatori. És molt important que el formateig del text sigui el menor possible, i en particular, que si copieu i enganxeu el text d\'algun altre lloc cap aquí, ho feu amb l\'opció "enganxar sense format", ja que sinó arrossegarà molta informació de formateig que probablement farà que el correu es vegi malament.', null=True, verbose_name='instruccions per participar')),
                ('poll_sent', models.DateTimeField(blank=True, null=True, verbose_name="data d'enviament de l'enquesta")),
            ],
            options={
                'verbose_name': 'sessió',
                'verbose_name_plural': 'sessions',
                'ordering': ['-date_start'],
            },
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='nom')),
            ],
            options={
                'verbose_name': 'organitzadora',
                'verbose_name_plural': 'organitzadores',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='nom')),
                ('legal_id', models.CharField(blank=True, max_length=9, null=True, verbose_name='N.I.F.')),
                ('is_active', models.BooleanField(default=True, help_text='Si la desactives no apareixerà al desplegable.', verbose_name='Activa')),
                ('neighborhood', models.CharField(blank=True, default='', max_length=50, verbose_name='Barri')),
                ('town', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.town', verbose_name='municipi')),
            ],
            options={
                'verbose_name': 'entitat',
                'verbose_name_plural': 'entitats',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CoursePlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='nom')),
                ('address', models.CharField(max_length=200, verbose_name='adreça')),
                ('town', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.town', verbose_name='població')),
            ],
            options={
                'verbose_name': 'lloc',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='títol')),
                ('slug', models.CharField(max_length=250, unique=True)),
                ('date_start', models.DateField(verbose_name='dia inici')),
                ('date_end', models.DateField(blank=True, null=True, verbose_name='dia finalització')),
                ('hours', models.CharField(help_text='Indica només els horaris, sense els dies.', max_length=200, verbose_name='horaris')),
                ('description', models.TextField(null=True, verbose_name='descripció')),
                ('publish', models.BooleanField(verbose_name='publicat')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='data de creació')),
                ('banner', easy_thumbnails.fields.ThumbnailerImageField(blank=True, max_length=250, null=True, storage=apps.coopolis.storage_backends.PublicMediaStorage(), upload_to='')),
                ('place', models.ForeignKey(blank=True, help_text="Aquesta dada de moment és d'ús intern i no es publica.", null=True, on_delete=django.db.models.deletion.SET_NULL, to='cc_courses.courseplace', verbose_name='lloc')),
            ],
            options={
                'verbose_name': 'acció',
                'verbose_name_plural': 'accions',
                'ordering': ['-date_start'],
            },
        ),
        migrations.CreateModel(
            name='ActivityResourceFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(storage=apps.coopolis.storage_backends.PublicMediaStorage(), upload_to='', verbose_name='fitxer')),
                ('name', models.CharField(max_length=120, verbose_name='nom del recurs')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='cc_courses.activity')),
            ],
            options={
                'verbose_name': 'recurs',
                'verbose_name_plural': 'recursos i material formatiu',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ActivityEnrolled',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_enrolled', models.DateTimeField(auto_now_add=True, null=True, verbose_name="data d'inscripció")),
                ('user_comments', models.TextField(blank=True, null=True, verbose_name='comentaris')),
                ('waiting_list', models.BooleanField(default=False, verbose_name="en llista d'espera")),
                ('reminder_sent', models.DateTimeField(blank=True, null=True, verbose_name='Recordatori enviat')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='cc_courses.activity', verbose_name='sessió')),
            ],
            options={
                'verbose_name': 'inscripció',
                'verbose_name_plural': 'inscripcions',
                'db_table': 'cc_courses_activity_enrolled',
            },
        ),
    ]
