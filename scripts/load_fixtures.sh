#!/bin/sh

HIGHLIGHT_COLOR="\e[1;36m" # cyan
DEFAULT_COLOR="\e[0m"

# activate virtual environment
cd /vagrant/application
. ./env/bin/activate

# load data fixtures by hijacking flask_testing module
cd /vagrant

echo "\n${HIGHLIGHT_COLOR}Loading development data fixtures...${DEFAULT_COLOR}"

if ! python ./scripts/load_fixtures.py > /dev/null 2>&1 ; then
    echo "Could not load data fixtures."
    exit
fi

echo "Complete."
