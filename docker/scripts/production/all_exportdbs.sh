#!/bin/bash
source sh_vars.conf

for ateneu in "${!comunalitats[@]}"
do
  :
  docker exec -i "$postgres_container" pg_dump "${comunalitats[$ateneu]}" -U postgres > "$dumps_path"/"${comunalitats[$ateneu]}".sql
  printf "Exportada base de dades de: %s\n" "$ateneu"
done