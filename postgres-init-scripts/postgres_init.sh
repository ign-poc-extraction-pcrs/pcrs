#!/bin/bash
set -e

# Create the database
echo "Creating database pcrs..."
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
  CREATE DATABASE pcrs;
EOSQL

# Install PostGIS
echo "Installing PostGIS extensions..."
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "pcrs" <<-EOSQL
  CREATE EXTENSION postgis;
  CREATE EXTENSION postgis_topology;
EOSQL

# Create the table
echo "Creating table mytable..."
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "pcrs" -f /docker-entrypoint-initdb.d/create_table.sql
