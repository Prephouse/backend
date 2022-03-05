#!/usr/bin/env bash

###################################
# NOTE: Set the docker-compose.production.yml file as
# the docker-compose.yml when deploying a new
# version of the BE to AWS Beanstalk
###################################

# Move all environment variables to .env file
cat .env.production >> .env

# Set/update beanstalk environment variables
# shellcheck disable=SC2046
eb setenv $(cat .env | sed '/^#/ d' | sed '/^$/ d')

# Deploys the most recent git commit in current branch
# Use  `eb deploy --staged` to deploy staged changes
eb deploy
