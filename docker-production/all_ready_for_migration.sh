#!/bin/bash
docker exec ateneu_catcentral python manage.py stage_sessions_report --check
docker exec ateneu_vallesoccidental python manage.py stage_sessions_report --check
docker exec ateneu_bnord python manage.py stage_sessions_report --check
docker exec ateneu_ponentcoopera python manage.py stage_sessions_report --check
docker exec ateneu_coopolis python manage.py stage_sessions_report --check
docker exec ateneu_coopmaresme python manage.py stage_sessions_report --check
docker exec ateneu_coopcamp python manage.py stage_sessions_report --check
docker exec ateneu_coopsetania python manage.py stage_sessions_report --check
docker exec ateneu_terresgironines python manage.py stage_sessions_report --check
docker exec ateneu_hospitalet python manage.py stage_sessions_report --check
docker exec ateneu_terresebre python manage.py stage_sessions_report --check
docker exec ateneu_altpirineu python manage.py stage_sessions_report --check