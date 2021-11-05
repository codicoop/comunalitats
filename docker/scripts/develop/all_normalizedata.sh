#!/bin/bash
source sh_vars.conf

for ateneu in "${!ateneus[@]}"
do
  :
  printf "Running migrate %s\n" "$ateneu"
  docker exec "$ateneu" python manage.py normalizedata
done