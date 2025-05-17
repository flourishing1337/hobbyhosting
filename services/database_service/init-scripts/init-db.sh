#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
  -- Production databases
  CREATE DATABASE auth_prod;
  CREATE DATABASE mail_prod;
  CREATE DATABASE ecommerce_prod;
  CREATE DATABASE admin_sync_db;

  -- Development databases
  CREATE DATABASE auth_dev;
  CREATE DATABASE mail_dev;
  CREATE DATABASE ecom_dev;
  CREATE DATABASE admin_sync_dev;
