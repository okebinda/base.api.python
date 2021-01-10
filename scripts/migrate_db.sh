#!/bin/bash

# prep virtual environment
export PIPENV_PIPFILE='/vagrant/application/Pipfile'

# export env variables
cd /vagrant/application
set -o allexport
source config/.env.public.local
set +o allexport

## UX
#HIGHLIGHT_COLOR="\e[1;36m" # cyan
#DEFAULT_COLOR="\e[0m"
#
#echo -e "\n${HIGHLIGHT_COLOR}Refreshing database...${DEFAULT_COLOR}"
#
#if ! pipenv run python -m src.main.scripts.db_refresh; then
#    echo "Could not load data fixtures."
#    exit
#fi
#
#echo "Complete."


cd /vagrant/application/src/main/

# initiate database
pipenv run flask db init
#pipenv run flask db migrate
#pipenv run flask db upgrade
