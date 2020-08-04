#!/bin/bash
echo "Running normalizedata ateneu_catcentral"
docker exec ateneu_catcentral python manage.py normalizedata
echo "Running normalizedata ateneu_vallesoccidental"
docker exec ateneu_vallesoccidental python manage.py normalizedata
echo "Running normalizedata ateneu_bnord"
docker exec ateneu_bnord python manage.py normalizedata
echo "Running normalizedata ateneu_ponentcoopera"
docker exec ateneu_ponentcoopera python manage.py normalizedata
echo "Running normalizedata ateneu_coopolis"
docker exec ateneu_coopolis python manage.py normalizedata
echo "Running normalizedata ateneu_coopmaresme"
docker exec ateneu_coopmaresme python manage.py normalizedata
echo "Running normalizedata ateneu_coopcamp"
docker exec ateneu_coopcamp python manage.py normalizedata
echo "Running normalizedata ateneu_coopsetania"
docker exec ateneu_coopsetania python manage.py normalizedata
echo "Running normalizedata ateneu_terresgironines"
docker exec ateneu_terresgironines python manage.py normalizedata
echo "Tots els normalizedatas tirats, excepte ateneu_demo."