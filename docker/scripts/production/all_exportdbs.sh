#!/bin/bash
source sh_vars.conf

for ateneu in "${!ateneus[@]}"
do
  :
  docker exec -i "$postgres_container" pg_dump "${ateneus[$ateneu]}" -U postgres > "$dumps_path"/"${ateneus[$ateneu]}".sql
  printf "Exportada base de dades de: %s\n" "$ateneu"
done