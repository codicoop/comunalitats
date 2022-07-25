#!/bin/bash
#!/bin/bash
source sh_vars.conf
day=$(date +%y%m%d)

for remote_name in "${!wasabi_remotes[@]}"
do
  :
  # Per accedir al nom del remote (la key de l'array): "$remote_name"
  echo Descarregant del remote: "$remote_name" / bucket: "${wasabi_remotes[$remote_name]}" / file name: "${remotes_to_db_names[$remote_name]}".sql
  rclone copyto "$remote_name":/"${wasabi_remotes[$remote_name]}"/server.backup/"${day}"/0000.postgres.sql "$dumps_path"/"${remotes_to_db_names[$remote_name]}".sql

#  docker exec "$postgres_container" dropdb "${comunalitats[bucket]}" -U postgres
#  printf "Eliminada base de dades: %s\n" "${comunalitats[$ateneu]}"
#  docker exec "$postgres_container" createdb "${comunalitats[$ateneu]}" -U postgres
#  printf "Re-creada base de dades: %s\n" "${comunalitats[$ateneu]}"
#  cat "$dumps_path"/"${comunalitats[$ateneu]}".sql | docker exec -i "$postgres_container" psql -d "${comunalitats[$ateneu]}" -U postgres
#  printf "Importada la base de dades: %s\n" "${comunalitats[$ateneu]}"
done

