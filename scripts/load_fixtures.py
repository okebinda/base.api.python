import os
import sys
import unittest

from flask_testing import TestCase
from fixture import SQLAlchemyFixture
from fixture.style import NamedDataStyle

# set environmental variables for testing
os.environ["DATABASE_URL"] = 'postgresql://api_admin:passpass@localhost:5432/api_db_dev'
os.environ["SECRET_KEY"] = 'SrJMTtdN7vu9NBBLgzNYRczC3UaWbUYuSwzD7CDduRfNjSPPKQZYzpjQFP4fKD3C'
os.environ["AUTH_SECRET_KEY"] = 'XHmhmQzSqudjUBpuYT7CXUCnsJC4j274T84E7Hm7MYHccY8Gyfeg4apzPKxbb76N'
os.environ["AUTH_TOKEN_EXPIRATION"] = '14400'
os.environ["AUTH_HASH_ROUNDS"] = '15'
os.environ["CRYPT_SYM_SECRET_KEY"] = 'VEsuvPZ2W5M8Hb8s7cddMyAMB3g9LPf8VmC4hFmJWckG5htZfgybREBeDa2WaUDs'
os.environ["CRYPT_DIGEST_SALT"] = 'mTqjD2YZKU4SXwT7uADbA5bndcc2meEz9PWgX56acdZUZpKn9X82SaJ67F8x8XAK'

# include application directory in import path
PACKAGE_PARENT = '../application/src'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

# include data directory in import path
DATA_PARENT = '../data'
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, DATA_PARENT)))

from test_fixtures import *

# application imports
from app import db
from app.api_admin import create_app
from app.Config import Config
from app import models

class MockTest(TestCase):

    def create_app(self):
        app = create_app(Config)
        return app
        
    def setUp(self):
        db.drop_all()
        db.create_all()
        dbfixture = SQLAlchemyFixture(
            engine=db.engine, env=models,
            style=NamedDataStyle())
        data = dbfixture.data(CountryData, RegionData, AppKeyData, AdministratorData, TermsOfServiceData,
            UserTermsOfServiceData, UserProfileData, LoginData, PasswordResetData,
            NotificationData)
        data.setup()
        dbfixture.dispose()

    def tearDown(self):
        pass
    
    def test_mock(self):
        pass

# run tests
if __name__ == '__main__':
    unittest.main()
