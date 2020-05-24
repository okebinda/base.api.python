#!/bin/bash

############################################
#
# Integration Tests
#
#  Runs all integration tests for project.
#
#  Usage: run.sh [OPTIONS]
#
#  Options:
#   -c : Display coverage report
#   -h : Create coverage HTML to inspect gaps
#
############################################

# environment variables
export PIPENV_PIPFILE='/vagrant/application/Pipfile'
export COVERAGE_FILE='/vagrant/tests/integration/.coverage'

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

# flags
FLAG_COVERAGE_REPORT='false'
FLAG_COVERAGE_HTML='false'

# options
while getopts 'ch' flag; do
  case "${flag}" in
    c) FLAG_COVERAGE_REPORT='true' ;;
    h) FLAG_COVERAGE_HTML='true' ;;
    *) error "Unexpected option ${flag}" ;;
  esac
done
shift $((OPTIND-1))

# run integration tests
cd /vagrant/application/src/main/python
pipenv run coverage run -m --source=. pytest -W ignore -m integration ../../pytest/python/

# show coverage
if [ "$FLAG_COVERAGE_REPORT" = true ]
then
  pipenv run coverage report
fi

# generate HTML coverage files
if [ "$FLAG_COVERAGE_HTML" = true ]
then
  pipenv run coverage html -d /vagrant/tests/integration/htmlcov
fi

