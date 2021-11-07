#!/usr/bin/env bash

down=false
mock=false
up=false

iter_cnt=0
res=-1

display_help() {
  echo "
    USAGE: ./setup.sh [-d] [-h] [-m] [-u]
    -------------------------------------------------------------------------------------------------------------------------
    |  FLAG  |  DESCRIPTION                                          |  ARGUMENT                  |  DEFAULT                |
    |--------|-------------------------------------------------------|----------------------------|-------------------------|
    |  -d    |  remove existing docker containers first, if any      |  N/A                       |  false                  |
    |  -h    |  display help message                                 |  N/A                       |  false                  |
    |  -m    |  insert test data into prephouse database             |  N/A                       |  false                  |
    |  -u    |  start container immediately after setup completion   |  N/A                       |  false                  |
    -------------------------------------------------------------------------------------------------------------------------
  "
}

while getopts ":dhms" FLAG
do
  case $FLAG in
    d) down=true;;
    m) mock=true;;
    s) up=true;;
    h) display_help; exit 0;;
    \?) echo "ERROR: One or more flags are not recognized by this script"; display_help; exit 1;;
  esac
done

if [ $down = true ]; then
  docker-compose down --remove-orphans
fi

docker-compose build
docker-compose up --detach && {
  sleep 10
  until [ $iter_cnt -gt 0 ] && [ $res = 0 ]
  do
    ((iter_cnt++))
    if [ $mock = true ]; then
      docker exec -it backend-prephouse-1 python3 create_schema.py --mock
    else
      docker exec -it backend-prephouse-1 python3 create_schema.py
    fi
    res=$?
    sleep 3
  done
}
docker-compose stop  # stop regardless of the [-u] flag

if [ $up = true ]; then
  docker-compose up --no-recreate
fi
