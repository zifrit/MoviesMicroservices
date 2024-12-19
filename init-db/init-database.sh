#!/bin/bash

set -e

psql --username postgres --dbname postgres <<-EOSQL
    CREATE DATABASE $AUTH_DB_NAME;
    CREATE DATABASE $MOVIES_DB_NAME;
    CREATE DATABASE $COMMENTS_DB_NAME;
EOSQL