#!/bin/sh

# activate virtual environment
cd /vagrant/application
. ./env/bin/activate

# server variables
export FLASK_APP=main_admin
export FLASK_ENV=development
export FLASK_DEBUG=1

# application variables
export DATABASE_URL='postgresql://api_admin:passpass@localhost:5432/api_db_dev'
export SECRET_KEY='SrJMTtdN7vu9NBBLgzNYRczC3UaWbUYuSwzD7CDduRfNjSPPKQZYzpjQFP4fKD3C'
export AUTH_SECRET_KEY='XHmhmQzSqudjUBpuYT7CXUCnsJC4j274T84E7Hm7MYHccY8Gyfeg4apzPKxbb76N'
export AUTH_TOKEN_EXPIRATION=14400
export AUTH_HASH_ROUNDS=15
export CRYPT_SYM_SECRET_KEY='VEsuvPZ2W5M8Hb8s7cddMyAMB3g9LPf8VmC4hFmJWckG5htZfgybREBeDa2WaUDs'
export CRYPT_DIGEST_SALT='mTqjD2YZKU4SXwT7uADbA5bndcc2meEz9PWgX56acdZUZpKn9X82SaJ67F8x8XAK'
export CORS_ORIGIN='base.admin.python.vm'
export LOGGING_LEVEL='INFO'
export SPARKPOST_API_KEY=''

cd src/
flask run -p 5001
