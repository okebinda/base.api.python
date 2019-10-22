#!/bin/sh

# application variables
export DATABASE_URL='postgresql://api_admin:passpass@localhost:5432/api_db_dev'

cd /vagrant/application

# activate virtual environment
. ./env/bin/activate

# migrate/upgrade database
cd src/
flask db migrate
flask db upgrade
