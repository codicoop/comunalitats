#!/bin/bash
echo "Running normalizedata develop_coopolis_app"
docker exec develop_coopolis_app python manage.py normalizedata
echo "Running normalizedata develop_coopolis_segon_ateneu"
docker exec develop_coopolis_segon_ateneu python manage.py normalizedata
