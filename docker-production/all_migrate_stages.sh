#!/bin/bash
echo "Running migration for ateneu_catcentral"
docker exec ateneu_catcentral python manage.py stage_sessions_report --migrate > /srv/reports/ateneu_catcentral.html
echo "Running migration for ateneu_vallesoccidental"
docker exec ateneu_vallesoccidental python manage.py stage_sessions_report --migrate > /srv/reports/ateneu_vallesoccidental.html
echo "Running migration for ateneu_bnord"
docker exec ateneu_bnord python manage.py stage_sessions_report --migrate > /srv/reports/ateneu_bnord.html
echo "Running migration for ateneu_ponentcoopera"
docker exec ateneu_ponentcoopera python manage.py stage_sessions_report --migrate > /srv/reports/ateneu_ponentcoopera.html
echo "Running migration for ateneu_coopolis"
docker exec ateneu_coopolis python manage.py stage_sessions_report --migrate > /srv/reports/ateneu_coopolis.html
echo "Running migration for ateneu_coopmaresme"
docker exec ateneu_coopmaresme python manage.py stage_sessions_report --migrate > /srv/reports/ateneu_coopmaresme.html
echo "Running migration for ateneu_coopcamp"
docker exec ateneu_coopcamp python manage.py stage_sessions_report --migrate > /srv/reports/ateneu_coopcamp.html
echo "Running migration for ateneu_coopsetania"
docker exec ateneu_coopsetania python manage.py stage_sessions_report --migrate > /srv/reports/ateneu_coopsetania.html
echo "Running migration for ateneu_terresgironines"
docker exec ateneu_terresgironines python manage.py stage_sessions_report --migrate > /srv/reports/ateneu_terresgironines.html
echo "Running migration for ateneu_hospitalet"
docker exec ateneu_hospitalet python manage.py stage_sessions_report --migrate > /srv/reports/ateneu_hospitalet.html
echo "Running migration for ateneu_terresebre"
docker exec ateneu_terresebre python manage.py stage_sessions_report --migrate > /srv/reports/ateneu_terresebre.html
echo "Running migration for ateneu_altpirineu"
docker exec ateneu_altpirineu python manage.py stage_sessions_report --migrate > /srv/reports/ateneu_altpirineu.html
echo "Tots els stage_sessions_report --migrate > /srv/reports/ateneu_catcentral.htmls tirats, excepte ateneu_demo."