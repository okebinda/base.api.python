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

cd /vagrant/application

# create requirements.txt
pipenv lock -r | sed 's/;.*//' | sed '/^[-#]/d' | sed '/^$/d' > requirements.txt
pipenv lock -r --dev | sed 's/;.*//' | sed '/^[-#]/d' | sed '/^$/d' > requirements-dev.txt

# run pybuilder
pyb

# cleanup
rm requirements.txt requirements-dev.txt
