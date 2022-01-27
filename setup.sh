#!/usr/bin/env bash

docker-compose down --remove-orphans

docker network create prephouse || true

docker-compose build

docker-compose up --detach && {
  echo "Setting up your local database..."
  sleep 5
  docker-compose run --service-ports --rm migration flask db upgrade
}
docker-compose stop
