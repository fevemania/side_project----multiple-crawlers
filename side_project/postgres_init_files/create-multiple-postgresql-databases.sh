#!/bin/bash

set -e
set -u

function create_user_and_database() {
    local database=$(echo $1 | tr ',' ' ' | awk  '{print $1}')
    local owner=$(echo $1 | tr ',' ' ' | awk  '{print $2}')
    echo "  Creating user '$owner' and database '$database'"
    echo "SELECT 'CREATE DATABASE $database' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$database')\gexec" | psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d postgres
    psql -v ON_ERROR_STOP=1 -U "$owner" -d $database <<-EOSQL
    DO \$\$
        BEGIN
          CREATE USER $owner;
          EXCEPTION WHEN OTHERS THEN
          RAISE NOTICE 'not creating user $owner -- it already exists';
        END \$\$;
    GRANT ALL PRIVILEGES ON DATABASE $database TO $owner;
    CREATE EXTENSION IF NOT EXISTS pgroonga;
EOSQL
}

if [ -n "$POSTGRES_MULTIPLE_DATABASES" ]; then
	echo "Multiple database creation requested: $POSTGRES_MULTIPLE_DATABASES"
	for db in $(echo $POSTGRES_MULTIPLE_DATABASES | tr '|' ' '); do
		create_user_and_database $db
	done
	echo "Multiple databases created"
fi
