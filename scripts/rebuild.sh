#!/bin/sh

export PIPENV_VERBOSITY=-1

HIGHLIGHT_COLOR="\e[1;36m" # cyan
DEFAULT_COLOR="\e[0m"

# activate virtual environment
cd /vagrant/application
. ./env/bin/activate

echo "\n${HIGHLIGHT_COLOR}Installing dependencies...${DEFAULT_COLOR}"

# install dependencies
pipenv install --dev

# load data fixtures
cd /vagrant
./scripts/load_fixtures.sh
