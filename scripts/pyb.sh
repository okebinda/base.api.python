#!/bin/bash

############################################
#
# Run Pybuilder
#
#  Runs pybuilder to locally run CI workflow
#  before committing code.
#
#  Usage: pyb.sh
#
############################################


cd /vagrant/application

# export env variables
set -o allexport
source config/.env.test
set +o allexport

# create requirements.txt
pipenv lock -r | sed 's/;.*//' | sed '/^[-#]/d' | sed '/^$/d' > requirements.txt
pipenv lock -r --dev | sed 's/;.*//' | sed '/^[-#]/d' | sed '/^$/d' > requirements-dev.txt

# run pybuilder
pyb

# cleanup
rm requirements.txt requirements-dev.txt
