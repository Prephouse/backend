#!/usr/bin/env bash

down=false
mock=false
up=false

iter_cnt=0
res=-1

display_help() {
  echo "
    usage: ./setup.sh [-dmu|-h]
    options:
      -d remove existing docker containers first, if any
      -h display help message
      -m insert test data into prephouse database
      -u start container immediately after setup completion
  "
}

while getopts ":dhmu" FLAG
do
  case $FLAG in
    d) down=true;;
    m) mock=true;;
    u) up=true;;
    h) display_help; exit 0;;
    \?) echo "ERROR: One or more options are not recognized by this script"; display_help; exit 1;;
  esac
done

if [ $down = true ]; then
  docker-compose down --remove-orphans
fi

docker network create prephouse || true

docker-compose build --no-cache
docker-compose up --detach && {
  sleep 7
  until [ $iter_cnt -gt 0 ] && [ $res = 0 ]
  do
    ((iter_cnt++))
    if [ $mock = true ]; then
      echo "Creating a local database with some mock data..."
      docker exec -it prephouse-backend python3 prephouse/create_database.py --mock
    else
      docker exec -it prephouse-backend python3 prephouse/create_database.py
    fi
    res=$?
    sleep 3
  done
}
docker-compose stop

if [ $up = true ]; then
  docker-compose up --no-recreate
fi
