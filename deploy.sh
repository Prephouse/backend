#!/usr/bin/env bash

mv docker-compose.yml docker-compose.tmp.yml
mv docker-compose.production.yml docker-compose.yml

eb deploy

mv docker-compose.yml docker-compose.production.yml
mv docker-compose.tmp.yml docker-compose.yml
