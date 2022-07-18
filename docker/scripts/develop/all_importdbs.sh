#!/bin/bash
source sh_vars.conf

for ateneu in "${!comunalitats[@]}"
do
  :
  # Per accedir al contenidor (la key de l'array): "$ateneu"
  docker exec "$postgres_container" dropdb "${comunalitats[$ateneu]}" -U postgres
  printf "Eliminada base de dades: %s\n" "${comunalitats[$ateneu]}"
  docker exec "$postgres_container" createdb "${comunalitats[$ateneu]}" -U postgres
  printf "Re-creada base de dades: %s\n" "${comunalitats[$ateneu]}"
  cat "$dumps_path"/"${comunalitats[$ateneu]}".sql | docker exec -i "$postgres_container" psql -d "${comunalitats[$ateneu]}" -U postgres
  printf "Importada la base de dades: %s\n" "${comunalitats[$ateneu]}"
done
