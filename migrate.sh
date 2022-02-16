#!/usr/bin/env bash

mig=""
merge=false
mock=false
up=false
down=false
empty=false

display_help() {
  echo "
    Usage: ./setup.sh [options][-g MESSAGE]
    Options:
      -d downgrade database from the most recent migration
      -e create an empty migration file
      -h display help message
      -m insert mock values into the database
      -r merge multiple head revisions
      -u upgrade database with the latest migrations
    Optional Arguments:
      -g generate a new database migration with the specified message
  "
}

while getopts ":dg:mhrue" OPTION
do
  case $OPTION in
    d) down=false;;
    g) mig=${OPTARG};;
    m) mock=true;;
    h) display_help; exit 0;;
    r) merge=true;;
    u) up=true;;
    e) empty=true;;
    \?) echo "ERROR: One or more options are not recognized by this script"; display_help; exit 1;;
  esac
done

if [ -n "$mig" ]; then
  docker-compose run --rm migration flask db migrate -m "$mig"
fi

if [ $merge = true ]; then
  docker-compose run --rm migration flask db merge heads
fi

if [ $up = true ] || [ $mock = true ]; then
  docker-compose run --service-ports --rm migration flask db upgrade
fi

if [ $down = true ]; then
  docker-compose run --service-ports --rm migration flask db downgrade
fi

if [ $mock = true ]; then
  docker-compose run --service-ports --rm migration python3 prephouse/mock.py
fi

if [ $empty = true ]; then
  docker-compose run --service-ports --rm migration flask db revision
fi
