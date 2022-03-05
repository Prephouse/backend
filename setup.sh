#!/usr/bin/env bash

no_cache=false

while getopts ":n" OPTION
do
  case $OPTION in
    n) no_cache=true;;
    \?) echo "ERROR: One or more options are not recognized by this script"; display_help; exit 1;;
  esac
done

docker compose down --remove-orphans

docker network create prephouse || true

if [ $no_cache = true ]; then
  docker compose build --no-cache
else
  docker compose build
fi

docker compose up --detach && {
  echo "Setting up your local database..."
  sleep 5
  docker compose run --service-ports --rm migration flask db upgrade
}
docker compose stop
