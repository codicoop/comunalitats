#!/bin/bash
declare -A ateneus=(
  ["ateneu_catcentral"]="ateneus_catcentral"
  ["ateneu_vallesoccidental"]="ateneus_vallesoccidental"
  ["ateneu_bnord"]="ateneus_bnord"
  ["ateneu_ponentcoopera"]="ateneus_ponentcoopera"
  ["ateneu_coopolis"]="coopolis"
  ["ateneu_coopmaresme"]="ateneus_coopmaresme"
  ["ateneu_coopcamp"]="ateneus_coopcamp"
  ["ateneu_coopsetania"]="ateneus_coopsetania"
  ["ateneu_terresgironines"]="ateneus_terresgironines"
  ["ateneu_hospitalet"]="ateneus_hospitalet"
  ["ateneu_terresebre"]="ateneus_terresebre"
  ["ateneu_altpirineu"]="ateneus_altpirineu"
)

for ateneu in "${!ateneus[@]}"
do
  :
  printf "Running stage_sessions_report --migrate to: %s\n" "$ateneu"
  docker exec "$ateneu" python manage.py stage_sessions_report --migrate > /srv/reports/stages_migration_"$ateneu".html
done