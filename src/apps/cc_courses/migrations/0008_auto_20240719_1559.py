# Generated by Django 3.2.14 on 2024-07-19 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('towns', '0002_load_town_fixtures'),
        ('cc_courses', '0007_auto_20240709_1020'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['title'], 'verbose_name': 'projecte', 'verbose_name_plural': 'projectes'},
        ),
        migrations.RemoveField(
            model_name='activity',
            name='included_project',
        ),
        migrations.AlterField(
            model_name='activity',
            name='course',
            field=models.ForeignKey(help_text="Escriu el nom del projecte i selecciona'l del desplegable. Si no existeix, clica a la lupa i després a 'Crear projecte'.", on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='cc_courses.course', verbose_name="Projecte al qual s'engloba"),
        ),
        migrations.AlterField(
            model_name='activity',
            name='date_start',
            field=models.DateField(verbose_name="dia inici d'actuació"),
        ),
        migrations.AlterField(
            model_name='activity',
            name='description',
            field=models.CharField(blank=True, default='', help_text="Descripció breu per l'excel de justificació.", max_length=150, verbose_name='descripció actuació'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='name',
            field=models.CharField(max_length=200, verbose_name="nom de l'actuació"),
        ),
        migrations.AlterField(
            model_name='activity',
            name='service',
            field=models.SmallIntegerField(blank=True, choices=[(None, 'Cap'), (10, "A) Serveis d'anàlisis i prospectiva"), (20, "B) Servei de formació i difusió per a l'activisme"), (30, "C) Servei de formació per a la creació i l'establiment de projectes d'ajuda mútua"), (40, "D) Servei per a la creació i consolidació de projectes d'ajuda mútua, d'intercooperació i de cooperació entre els bens comuns urbans i la ciutadania"), (50, "E) Punt de trobada i d'informació de comunalitat urbana"), (60, "A) Serveis d'anàlisis i prospectiva"), (70, "B) Servei de formació i difusió per a l'activisme al barri/espai urbà adreçat a entitats i persones"), (80, "C) Servei de foment a projectes d'ajuda mútua, d'intercooperació i de cooperació entre els bens comuns urbans i la ciutadania"), (90, "D) Servei d’acompanyament a la creació i a la consolidació de projectes d'ajuda mútua")], help_text='Els Serveis disponibles s\'actualitzen segons la convocatòria, que es calcula amb el valor del camp "Data d\'inici".', null=True, verbose_name='Serveis'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='sub_service',
            field=models.SmallIntegerField(blank=True, choices=[(None, 'Cap'), (101, "A.1) Articulació i posada en funcionament de l'Assemblea de la Comunalitat"), (102, 'A.2) Identificació i incorporació dels béns comuns urbans, de les organitzacions, els col.lectius i els representants'), (103, "A.3) Creació o manteniment i difusió d'un recurs/ eina per visualitzar béns comuns i projectes d'ajuda mútua assolits. "), (104, "A.4) Elaboració d'un catàleg d'exemples de bones pràctiques d'ajuda mútua i ESS. Identificar i elaborar fitxes de bones pràctiques i iniciatives"), (105, 'A.5) Organització de jornades i accions directes a la comunalitat per visualitzar experiències; fires,actes, presència als mitjans de comunicació. '), (106, "A.6) Organització logística i metodològica de jornades pròpies per presentar bones pràctiques, parlar de temes sectorials o d'interés per el territori"), (107, "A.7) Participació o colaboració a actes, jornades, fires, publicacions amb l'objectiu de presentar el programa, visibilitzar experiències,organitzar tallers, publicar notes de premsa o articles opinió"), (108, "A.8) Altres accions dins el servei d'anàlisi i prospectiva "), (201, "B.1) Campanya de comunicació i difusió a col.lectius d'especial atenció"), (202, 'B.2) Elaboració de material especific i difusió dels materials'), (203, "B.3) Activitats anuals de dinamització  i activació de l'autoorganització col.lectiva per  a la generació de projectes"), (204, 'B.4)Tallers adreçats preferentment als joves o a la ciutadania de la comunalitat.'), (205, "B.5) Altres accions dins el servei de formació i difusió per a l'activisme al barri/espai urbà"), (301, "C.1) Activitats formatives i informatives per a la creció d'aliances "), (302, 'C.2) Organització de formació bàsica o dinamització destinades a persones o entitats interessades en la fórmula de colaboració, ajuda mutua o intercooperació'), (303, "C.3) Organització de sessions col.lectives i individuals per al disseny d'estratègies vinculades a l'autoorganització i intercooperació"), (304, "C.4) Activitats destinades a fomentar la col.laboració entre empreses de l'economia social i cooperativa del territori"), (305, 'C.5) Organització i acompanyament a les empreses/entitats participants en la primera fase de coordinació del projecte. '), (306, 'C.6) Elaboració i difusió de materials destinat a empreses, associassions i entitats sobre ajuda mútua i ESS'), (307, 'C.7) Tallers de sensibilització/dinamització destinats al teixit associatiu i a les empreses per donar a conèixer projectes '), (308, "C.8) Tallers de sensibilització/dinamització adreçats a professionals que s'agrupin de manera conjunta"), (309, "C.9) Altres accions dins el servei de formació per a la creació i establiment de projectes d'ajuda"), (401, "D.1) Creació d'espais d'intercooperació dins els territoris de referència per la generació de nous models econòmics"), (402, "D.2) Incorporació d'empreses, cooperatives i entitats ESS en els béns comuns urbans"), (403, 'D.3) Activitats de treball en xarxa amb altres comunalitats urbanes del programa '), (404, "D.4) Altres accions dins el servei per a la creació i consolidació de projectes d'ajuda mútua"), (501, "E.1) Atenció als usuaris a l'espai físic de referència"), (502, "E.2) Difusió del punt d'informació"), (601, 'A.1) Diagnosi i/o avaluació de necessitats de forma participada a nivell general i/o sectorial'), (602, 'A.2) Identificació i visualització de béns comuns urbans i altres iniciatives de suport mutu, activisme i ESS del territori'), (603, 'A.3) Elaboració de materials i suports de difusió de bones pràctiques de suport mutu, activisme i ESS del territori'), (604, 'A.4) Enxarxament territorial i de barri'), (605, 'A.5) Articulació i posada en funcionament de l’Assemblea, així com d’altres espais de governança democràtica i inclusiva de la Comunalitat'), (701, "B.1) Campanya de comunicació a col·lectius d'especial atenció"), (702, 'B.2) Dinamització per donar a conèixer projectes d’ajuda mútua, l’autogestió, ESS i cooperativisme, al teixit associatiu i a les empreses'), (703, 'B.3) Organització de jornades i assistència a accions directes de la comunalitat per visibilitzar experiències'), (704, "B.4) Generació d’espais de trobada i d'intercanvi d’experiències i col·laboració en iniciatives conjuntes entre actors i sectors diversos."), (705, 'B.5) Realització de formacions i/o divulgació de coneixement compartit entorn el suport mutu, l’activisme, els béns comuns i l’ESS'), (801, 'C.1) Orientació a persones, empreses i entitats per la creació d’activitats econòmiques i iniciatives empresarials de l’ESS'), (802, "C.2) Generació d’aliances entre professionals per promoure l'ocupabilitat digne a través de la intercooperació"), (803, 'C.3) Creació o consolidació dinàmiques de col·laboració i aliances entre diferents agents econòmics de forma democràtica i inclusiva'), (804, "C.4) Organització de sessions per al disseny d'estratègies vinculades a l'autoorganització col·lectiva, xarxes de suport mutu, intercooperació"), (805, 'C.5) Activitats per a la creació d’aliances i l’accés a l’ús comunal d’infraestructures i recursos'), (901, 'D.1) Acompanyament a projectes veïnals, socials i/o comunitaris per a la resolució de necessitats col·lectives'), (902, "D.2) Generació de nous projectes d'intercooperació o ajuda mútua dirigides i realitzades amb col·lectius específics")], null=True, verbose_name='Actuacions'),
        ),
        migrations.AlterField(
            model_name='courseplace',
            name='town',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='towns.town', verbose_name='municipi'),
        ),
        migrations.AlterField(
            model_name='entity',
            name='neighborhood',
            field=models.CharField(blank=True, default='', help_text="Aquest camp NO és el que apareix a l'excel de justificació.", max_length=50, verbose_name="Barri de l'entitat"),
        ),
    ]
