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
PIPENV_DOTENV_LOCATION=/vagrant/application/config/.env.test pipenv run coverage run -m --source=. pytest -m integration ../../pytest/python/

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

