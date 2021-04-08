#!/bin/bash
postgres_container="develop_ateneus_db"
dumps_path="../dumps"
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
  # Per accedir al contenidor (la key de l'array): "$ateneu"
  docker exec "$postgres_container" dropdb "${ateneus[$ateneu]}" -U postgres
  printf "Eliminada base de dades: %s\n" "${ateneus[$ateneu]}"
  docker exec "$postgres_container" createdb "${ateneus[$ateneu]}" -U postgres
  printf "Re-creada base de dades: %s\n" "${ateneus[$ateneu]}"
  cat "$dumps_path"/"${ateneus[$ateneu]}".sql | docker exec "$postgres_container" psql -d "${ateneus[$ateneu]}" -U postgres
  printf "Importada la base de dades: %s\n" "${ateneus[$ateneu]}"
done
