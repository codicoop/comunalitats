#!/bin/bash
source sh_vars.conf

for ateneu in "${!comunalitats[@]}"
do
  :
  printf "Running maintenance mode off %s\n" "$ateneu"
  docker exec "$ateneu" python manage.py maintenance_mode off
done