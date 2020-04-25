#!/bin/bash

# activate virtual environment
cd /vagrant/application
. ./env/bin/activate

# load data fixtures by hijacking flask_testing module
cd /vagrant
python ./scripts/load_fixtures.py
