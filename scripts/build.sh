#!/bin/sh

HIGHLIGHT_COLOR="\e[1;36m" # cyan
DEFAULT_COLOR="\e[0m"


echo "\n${HIGHLIGHT_COLOR}Creating virtual environment...${DEFAULT_COLOR}\n"

cd /vagrant/application

# create and activate virtual environment
virtualenv -p python3 env
. ./env/bin/activate

echo "\n${HIGHLIGHT_COLOR}Installing dependencies...${DEFAULT_COLOR}\n"

# install uwsgi
pip install uwsgi

# install pipenv
pip install pipenv

# install dependencies
pipenv install --dev

### TEMP REMOVED - until Postgres extensions are integrated into this script ###
#echo "\n${HIGHLIGHT_COLOR}Loading data fixtures...${DEFAULT_COLOR}\n"
#
#cd /vagrant
#
## load data fixtures by hijacking flask_testing module
#python ./scripts/load_fixtures.py

echo "\n${HIGHLIGHT_COLOR}Build complete.${DEFAULT_COLOR}\n"
