#!/bin/bash
source sh_vars.conf

for ateneu in "${!ateneus[@]}"
do
  :
  printf "Running stage_sessions_report --migrate to: %s\n" "$ateneu"
  docker exec "$ateneu" python manage.py stage_sessions_report --check
done