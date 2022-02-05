#!/usr/bin/env bash

mig=""
mock=false
up=false
down=false

display_help() {
  echo "
    usage: ./setup.sh [-mu|-h][-g MESSAGE]
    options:
      -d downgrade database from the most recent migration
      -h display help message
      -m insert mock values into the database
      -u upgrade database with the latest migrations
    optional arguments:
      -g generate a new database migration with the specified message
  "
}

while getopts ":dg:mhu" OPTION
do
  case $OPTION in
    d) down=false;;
    g) mig=${OPTARG};;
    m) mock=true;;
    h) display_help; exit 0;;
    u) up=true;;
    \?) echo "ERROR: One or more options are not recognized by this script"; display_help; exit 1;;
  esac
done

if [ -n "$mig" ]; then
  docker-compose run --rm migration flask db migrate -m "$mig"
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
