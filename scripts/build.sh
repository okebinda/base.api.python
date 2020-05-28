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
#
#################################################


# flags
FLAG_LOCAL_DEVELOPMENT_BUILD='false'
FLAG_LOCAL_DEVELOPMENT_REBUILD='false'

# options
while getopts 'dr' flag; do
  case "${flag}" in
    d) FLAG_LOCAL_DEVELOPMENT_BUILD='true' ;;
    r) FLAG_LOCAL_DEVELOPMENT_REBUILD='true' ;;
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
  pipenv install --dev

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


# PYBUILDER
if [[ "$FLAG_LOCAL_DEVELOPMENT_BUILD" = false && "$FLAG_LOCAL_DEVELOPMENT_REBUILD" = false ]]
then

  echo -e "\n${HIGHLIGHT_COLOR}Running pybuilder...${DEFAULT_COLOR}"

  # application variables
  export DATABASE_URL='postgresql://api_admin:passpass@localhost:5432/api_db_test'
  export SECRET_KEY='SrJMTtdN7vu9NBBLgzNYRczC3UaWbUYuSwzD7CDduRfNjSPPKQZYzpjQFP4fKD3C'
  export AUTH_SECRET_KEY='XHmhmQzSqudjUBpuYT7CXUCnsJC4j274T84E7Hm7MYHccY8Gyfeg4apzPKxbb76N'
  export AUTH_TOKEN_EXPIRATION=14400
  export AUTH_HASH_ROUNDS=4
  export CRYPT_SYM_SECRET_KEY='VEsuvPZ2W5M8Hb8s7cddMyAMB3g9LPf8VmC4hFmJWckG5htZfgybREBeDa2WaUDs'
  export CRYPT_DIGEST_SALT='mTqjD2YZKU4SXwT7uADbA5bndcc2meEz9PWgX56acdZUZpKn9X82SaJ67F8x8XAK'
  export CORS_ORIGIN=''
  export LOGGING_LEVEL='INFO'
  export SPARKPOST_API_KEY=''

  # run pybuilder
  cd /vagrant/application
  pyb

  echo -e "\n${HIGHLIGHT_COLOR}Build complete.${DEFAULT_COLOR}\n"

fi
