# Generated by Django 3.2.14 on 2022-07-18 09:31

import apps.coopolis.storage_backends
from django.db import migrations, models
import easy_thumbnails.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
                ('circle', models.SmallIntegerField(blank=True, choices=[(None, 'Cap'), (0, 'Ateneu'), (1, 'Cercle 1'), (2, 'Cercle 2'), (3, 'Cercle 3'), (4, 'Cercle 4'), (5, 'Cercle 5')], null=True, verbose_name='Ateneu / Cercle')),
                ('service', models.SmallIntegerField(blank=True, choices=[(None, 'Cap'), (10, 'Servei de mapatge i diagnosi'), (20, 'Servei de Divulgació, Sensibilització i Generació de Coneixement.'), (30, "Servei de Formació per a la promoció, creació i consolidació de cooperatives i projectes de l'ESS."), (40, "Servei d'Acompanyament per la creació i consolidació de cooperatives i projectes de l'ESS."), (50, 'Servei de Facilitació de la Intercooperació, treball en xarxa i dinamització territorial.'), (60, "Punt d'informació sobre l'ESS.")], null=True, verbose_name='Servei')),
                ('sub_service', models.SmallIntegerField(blank=True, choices=[(None, 'Cap'), (101, "Taula territorial per l'articulació conjunta de l'economia social amb els diversos actors."), (102, "Elaboració d'un catàleg bones pràctiques."), (103, 'Organització de jornades per visibilitzar experiències, presència als mitjans de comunicació locals, assistència a fires, actes i premis, trobades sectorials, col·laboracions amb altres iniciatives.'), (199, "Altres accions dins del servei de mapeig i diagnosi (si s'escau desenvolupeu a la memòria)"), (201, "Campanya de Comunicació i difusió a col·lectius d'especial atenció. Materials específic de difusió sobre la fórmula cooperativa."), (202, 'Tallers dirigits a joves estudiants de cicles formatius presencials o virtuals .'), (203, 'Accions per a la creació de diferents classes de cooperatives (concursos i tallers sensibilització)'), (204, 'Diagnosi sobre les mancances i oportunitats socioeconòmiques i identificació de les empreses participants.'), (205, "Sessions col·lectives i d'acompanyament expert individual."), (299, "Altres accions dins del servei de divulgació, sensibilitzacio i generació de coneixement (si s'escau desenvolupeu a la memòria)"), (301, 'Activitats formatives i informatives.'), (302, 'Tallers de formació bàsica a persones emprenedores interessades en la fòrmula cooperativa .'), (303, 'Sessions col·lectives'), (304, 'Acompanyament expert'), (305, 'Tallers de sensibilització o dinamització adreçada al teixit associatiu, empreses o professionals.'), (399, "Altres accions dins del servei de formació (si s'escau desenvolupeu a la memòria)"), (401, "Assessorament a mida per a la creació de cooperatives i altres organitzacions d'ESS"), (402, 'Acompanyament a la consolidació i creixement de cooperatives existents'), (403, "Acompanyament a la transformació d'empreses"), (404, 'Campanya de comunicació i difusió'), (405, 'Accions de sensibilització o dinamització'), (499, "Altres accions dins del servei d'acompanyament (si s'escau desenvolupeu a la memòria)"), (501, "Generar espais d'intercooperació i treball en xarxa dins del territori, intercooperació local, creació d'espais i grups d'intercooperació"), (502, "Incorporació d'empreses a l'ateneu cooperatiu i assemblea"), (503, 'Treball en xarxa amb altres ateneus: assistir a reunions i col·laborar en iniciatives conjuntes.'), (599, "Altres accions dins del servei de facilitació (si s'escau desenvolupeu a la memòria)"), (601, 'Espai físic per proporcionar informació sobre ESS a diferents públics'), (602, "Difusió del Punt o punts d'informació")], null=True, verbose_name='Sub-servei')),
                ('axis', models.CharField(blank=True, choices=[('A', 'Eix A'), ('B', 'Eix B'), ('C', 'Eix C'), ('D', 'Eix D'), ('E', 'Eix E'), ('F', 'Eix F')], help_text='Eix de la convocatòria on es justificarà.', max_length=1, null=True, verbose_name='(OBSOLET) Eix')),
                ('subaxis', models.CharField(blank=True, choices=[(None, '---------'), ('A1', 'A.1 Reunions de la taula territorial'), ('A2', 'A.2 Diagnosi entitats socials del territori'), ('A3', 'A.3 Elaboració catàleg bones pràctiques'), ('A4', "A.4 Jornades per presentar experiències de bones pràctiques o jornades sectorials i/o d'interès per al territori"), ('A5', 'A.5 Assistència a fires, actes per visibilitzar el programa'), ('A6', 'A.6 Publicitat en mitjans de comunicació.  Web del programa'), ('A7', 'A.7 Altres'), ('B1', 'B.1 Accions de suport a la inserció laboral i a la creació de cooperatives i societats laborals (concursos de projectes cooperatius o altres accions)'), ('B2', 'B.2 Tallers sensibilització o dinamització'), ('B3', 'B.3 Acompanyament a empreses i entitats'), ('B4', 'B.4 Altres'), ('C1', 'C.1 Tallers de dinamització adreçats al teixit associatiu i a empreses'), ('C2', "C.2 Tallers de dinamització adreçats a professionals que s'agrupen per prestar serveis de manera conjunta"), ('C3', 'C.3 Acompanyament a mida per a la creació o transformació'), ('C4', 'C.4 Altres'), ('D1', 'D.1 Accions de difusió'), ('D2', 'D.2 Activitats de sensibilització o dinamització.'), ('D3', 'D.3 Acompanyament individualitzat'), ('D4', 'D.4 Altres'), ('E1', 'E.1 Tallers a joves'), ('E2', 'E.2 Atenció individual professorat'), ('E3', 'E.3 Complementàries (recursos, eines, productes, publicacions sectorials pròpies )'), ('E4', 'E.4 Altres'), ('F1', "F.1 Pla d'actuació"), ('F2', "F.2 Tallers de creació de cooperatives o societats laborals, o transformació d'associacions, altres entitats"), ('F3', 'F.3 Altres')], help_text="Correspon a 'Tipus d'acció' a la justificació.", max_length=2, null=True, verbose_name='(OBSOLET) Sub-eix')),
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
                ('cofunded_ateneu', models.BooleanField(default=False, verbose_name='Cofinançat amb Ateneus Cooperatius')),
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
            name='ActivityEnrolled',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_enrolled', models.DateTimeField(auto_now_add=True, null=True, verbose_name="data d'inscripció")),
                ('user_comments', models.TextField(blank=True, null=True, verbose_name='comentaris')),
                ('waiting_list', models.BooleanField(default=False, verbose_name="en llista d'espera")),
                ('reminder_sent', models.DateTimeField(blank=True, null=True, verbose_name='Recordatori enviat')),
            ],
            options={
                'verbose_name': 'inscripció',
                'verbose_name_plural': 'inscripcions',
                'db_table': 'cc_courses_activity_enrolled',
            },
        ),
        migrations.CreateModel(
            name='ActivityResourceFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(storage=apps.coopolis.storage_backends.PublicMediaStorage(), upload_to='', verbose_name='fitxer')),
                ('name', models.CharField(max_length=120, verbose_name='nom del recurs')),
            ],
            options={
                'verbose_name': 'recurs',
                'verbose_name_plural': 'recursos i material formatiu',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Cofunding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='nom')),
            ],
            options={
                'verbose_name': 'cofinançadora',
                'verbose_name_plural': 'cofinançadores',
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
            ],
            options={
                'verbose_name': 'acció',
                'verbose_name_plural': 'accions',
                'ordering': ['-date_start'],
            },
        ),
        migrations.CreateModel(
            name='CoursePlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='nom')),
                ('address', models.CharField(max_length=200, verbose_name='adreça')),
            ],
            options={
                'verbose_name': 'lloc',
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
            ],
            options={
                'verbose_name': 'entitat',
                'verbose_name_plural': 'entitats',
                'ordering': ['name'],
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
            name='StrategicLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='nom')),
            ],
            options={
                'verbose_name': 'línia estratègica',
                'verbose_name_plural': 'línies estratègiques',
                'ordering': ['name'],
            },
        ),
    ]
