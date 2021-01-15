#!/bin/bash
echo "Running migrate ateneu_catcentral"
docker exec ateneu_catcentral python manage.py migrate
echo "Running migrate ateneu_vallesoccidental"
docker exec ateneu_vallesoccidental python manage.py migrate
echo "Running migrate ateneu_bnord"
docker exec ateneu_bnord python manage.py migrate
echo "Running migrate ateneu_ponentcoopera"
docker exec ateneu_ponentcoopera python manage.py migrate
echo "Running migrate ateneu_coopolis"
docker exec ateneu_coopolis python manage.py migrate
echo "Running migrate ateneu_coopmaresme"
docker exec ateneu_coopmaresme python manage.py migrate
echo "Running migrate ateneu_coopcamp"
docker exec ateneu_coopcamp python manage.py migrate
echo "Running migrate ateneu_coopsetania"
docker exec ateneu_coopsetania python manage.py migrate
echo "Running migrate ateneu_terresgironines"
docker exec ateneu_terresgironines python manage.py migrate
echo "Running migrate ateneu_hospitalet"
docker exec ateneu_hospitalet python manage.py migrate
echo "Running migrate ateneu_terresebre"
docker exec ateneu_terresebre python manage.py migrate
echo "Tots els migrates tirats, excepte ateneu_demo."