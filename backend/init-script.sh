#!/bin/bash

# Esperar até que o MySQL esteja pronto
until mysql -hdb -uroot -p"${MYSQL_ROOT_PASSWORD}" -e 'SHOW DATABASES;' &> /dev/null; do
  echo 'Aguardando o MySQL iniciar...'
  sleep 2
done

# Executar o script SQL
mysql -hdb -uroot -p"${MYSQL_ROOT_PASSWORD}" "${MYSQL_DATABASE}" < /docker-entrypoint-initdb.d/bd.sql

