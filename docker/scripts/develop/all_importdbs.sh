#!/bin/bash
source sh_vars.conf

for ateneu in "${!ateneus[@]}"
do
  :
  # Per accedir al contenidor (la key de l'array): "$ateneu"
  docker exec "$postgres_container" dropdb "${ateneus[$ateneu]}" -U postgres
  printf "Eliminada base de dades: %s\n" "${ateneus[$ateneu]}"
  docker exec "$postgres_container" createdb "${ateneus[$ateneu]}" -U postgres
  printf "Re-creada base de dades: %s\n" "${ateneus[$ateneu]}"
  cat "$dumps_path"/"${ateneus[$ateneu]}".sql | docker exec -i "$postgres_container" psql -d "${ateneus[$ateneu]}" -U postgres
  printf "Importada la base de dades: %s\n" "${ateneus[$ateneu]}"
done
