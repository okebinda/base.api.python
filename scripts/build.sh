#!/bin/bash

#################################################
#
# Build
#
#  Builds the project, including installing
#  dependencies.
#
#  Usage: build.sh [OPTIONS]
#
#  Options:
#   -d : Build the local development environment
#   -r : Rebuild the local development environment
#   -s : Sync the dependencies with pipfile.lock
#
#################################################


# flags
FLAG_LOCAL_DEVELOPMENT_BUILD='false'
FLAG_LOCAL_DEVELOPMENT_REBUILD='false'
FLAG_LOCAL_DEVELOPMENT_SYNC='false'

# options
while getopts 'drs' flag; do
  case "${flag}" in
    d) FLAG_LOCAL_DEVELOPMENT_BUILD='true' ;;
    r) FLAG_LOCAL_DEVELOPMENT_REBUILD='true' ;;
    s) FLAG_LOCAL_DEVELOPMENT_SYNC='true' ;;
    *) error "Unexpected option ${flag}" ;;
  esac
done
shift $((OPTIND-1))


# config env
export PIPENV_VERBOSITY=-1
HIGHLIGHT_COLOR="\e[1;36m" # cyan
DEFAULT_COLOR="\e[0m"


# LOCAL DEVELOPMENT BUILD
if [ "$FLAG_LOCAL_DEVELOPMENT_BUILD" = true ]
then

  echo -e "\n${HIGHLIGHT_COLOR}Creating virtual environment and installing dependencies...${DEFAULT_COLOR}"

  cd /vagrant/application

  # install global packages
  pip install uwsgi
  pip install pybuilder

  # create and activate virtual environment
  pipenv sync --dev

  echo -e "\n${HIGHLIGHT_COLOR}Adding database extensions...${DEFAULT_COLOR}"

  # add crypto extension to dev and test databases
  sudo -u postgres psql api_db_dev -c "CREATE EXTENSION pgcrypto"
  sudo -u postgres psql api_db_test -c "CREATE EXTENSION pgcrypto"

  # load data fixtures by hijacking flask_testing module
  cd /vagrant
  ./scripts/load_data.sh

  echo -e "\n${HIGHLIGHT_COLOR}Build complete.${DEFAULT_COLOR}\n"

fi


# LOCAL DEVELOPMENT REBUILD
if [ "$FLAG_LOCAL_DEVELOPMENT_REBUILD" = true ]
then

  echo -e "\n${HIGHLIGHT_COLOR}Installing dependencies...${DEFAULT_COLOR}"

  # install dependencies
  cd /vagrant/application
  pipenv install --dev

  # load data fixtures
  cd /vagrant
  ./scripts/load_data.sh

  echo -e "\n${HIGHLIGHT_COLOR}Rebuild complete.${DEFAULT_COLOR}\n"

fi

# LOCAL DEVELOPMENT SYNC
if [ "$FLAG_LOCAL_DEVELOPMENT_SYNC" = true ]
then

  echo -e "\n${HIGHLIGHT_COLOR}Installing dependencies...${DEFAULT_COLOR}"

  # install dependencies
  cd /vagrant/application
  pipenv sync --dev

  # load data fixtures
  cd /vagrant
  ./scripts/load_data.sh

  echo -e "\n${HIGHLIGHT_COLOR}Rebuild complete.${DEFAULT_COLOR}\n"

fi


# PYBUILDER
if [[ "$FLAG_LOCAL_DEVELOPMENT_BUILD" = false && "$FLAG_LOCAL_DEVELOPMENT_REBUILD" = false && "$FLAG_LOCAL_DEVELOPMENT_SYNC" = false ]]
then

  echo -e "\n${HIGHLIGHT_COLOR}Running pybuilder...${DEFAULT_COLOR}"

  # run pybuilder
  cd /vagrant
  ./scripts/pyb.sh

  echo -e "\n${HIGHLIGHT_COLOR}Build complete.${DEFAULT_COLOR}\n"

fi
