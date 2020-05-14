#!/bin/bash
echo "Running migrate develop_coopolis_app"
docker exec develop_coopolis_app python manage.py migrate mailqueue
docker exec develop_coopolis_app python manage.py migrate
echo "Running migrate develop_coopolis_segon_ateneu"
docker exec develop_coopolis_segon_ateneu python manage.py migrate mailqueue
docker exec develop_coopolis_segon_ateneu python manage.py migrate
