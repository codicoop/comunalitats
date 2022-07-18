#!/bin/bash
source sh_vars.conf

for ateneu in "${!comunalitats[@]}"
do
  :
  printf "Running migrate %s\n" "$ateneu"
  docker exec "$ateneu" python manage.py migrate
done