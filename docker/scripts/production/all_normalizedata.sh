#!/bin/bash
source sh_vars.conf

for ateneu in "${!comunalitats[@]}"
do
  :
  printf "Running normalizedata %s\n" "$ateneu"
  docker exec "$ateneu" python manage.py normalizedata
done