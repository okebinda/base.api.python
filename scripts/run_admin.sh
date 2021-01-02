#!/bin/bash

# prep virtual environment
export PIPENV_PIPFILE='/vagrant/application/Pipfile'

# export env variables
cd /vagrant/application
set -o allexport
source config/.env.admin.local
set +o allexport

# run application
cd /vagrant/application/src/main/python
pipenv run flask run --port=5001
