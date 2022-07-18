#!/bin/bash
source sh_vars.conf

for ateneu in "${!comunalitats[@]}"
do
  :
  printf "Running maintenance mode on %s\n" "$ateneu"
  docker exec "$ateneu" python manage.py maintenance_mode on
done