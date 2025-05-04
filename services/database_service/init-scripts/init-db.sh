#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
  CREATE DATABASE auth_prod;
  CREATE DATABASE mail_prod;
  CREATE DATABASE ecom_prod;
EOSQL
