#!/bin/sh
set -e

# Vänta tills Postgres accepterar anslutningar
until pg_isready -U "$POSTGRES_USER" > /dev/null 2>&1 ; do
  echo "⏳  Postgres startar..."
  sleep 2
done

# Skapa de databaser vi behöver om de inte redan finns
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-SQL
  CREATE DATABASE ${AUTH_DB}  WITH TEMPLATE template0 ENCODING 'UTF8';
  CREATE DATABASE ${MAIL_DB}  WITH TEMPLATE template0 ENCODING 'UTF8';
  CREATE DATABASE ${ECOM_DB}  WITH TEMPLATE template0 ENCODING 'UTF8';
  CREATE DATABASE ${ADMIN_DB} WITH TEMPLATE template0 ENCODING 'UTF8';
SQL
