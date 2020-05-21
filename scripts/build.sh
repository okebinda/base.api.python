#!/bin/sh

export PIPENV_VERBOSITY=-1

HIGHLIGHT_COLOR="\e[1;36m" # cyan
DEFAULT_COLOR="\e[0m"

echo "\n${HIGHLIGHT_COLOR}Creating virtual environment and installing dependencies...${DEFAULT_COLOR}"

cd /vagrant/application

# create and activate virtual environment
pipenv install --dev

# install uwsgi
pip install uwsgi

echo "\n${HIGHLIGHT_COLOR}Adding database extensions...${DEFAULT_COLOR}"

# add crypto extension to dev and test databases
sudo -u postgres psql api_db_dev -c "CREATE EXTENSION pgcrypto"
sudo -u postgres psql api_db_test -c "CREATE EXTENSION pgcrypto"

# load data fixtures by hijacking flask_testing module
cd /vagrant
./scripts/load_data.sh

echo "\n${HIGHLIGHT_COLOR}Build complete.${DEFAULT_COLOR}\n"
