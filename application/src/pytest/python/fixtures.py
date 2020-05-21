import os
import sys

from py_yaml_fixtures import FixturesLoader
from py_yaml_fixtures.factories.sqlalchemy import SQLAlchemyModelFactory

# # set environmental variables for testing
# os.environ["DATABASE_URL"] = 'postgresql://api_admin:passpass@localhost:5432/api_db_test'
# os.environ["SECRET_KEY"] = 'SrJMTtdN7vu9NBBLgzNYRczC3UaWbUYuSwzD7CDduRfNjSPPKQZYzpjQFP4fKD3C'
# os.environ["AUTH_SECRET_KEY"] = 'XHmhmQzSqudjUBpuYT7CXUCnsJC4j274T84E7Hm7MYHccY8Gyfeg4apzPKxbb76N'
# os.environ["AUTH_TOKEN_EXPIRATION"] = '14400'
# os.environ["AUTH_HASH_ROUNDS"] = '15'
# os.environ["CRYPT_SYM_SECRET_KEY"] = 'VEsuvPZ2W5M8Hb8s7cddMyAMB3g9LPf8VmC4hFmJWckG5htZfgybREBeDa2WaUDs'
# os.environ["CRYPT_DIGEST_SALT"] = 'mTqjD2YZKU4SXwT7uADbA5bndcc2meEz9PWgX56acdZUZpKn9X82SaJ67F8x8XAK'

# include application directory in import path
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, '../../../main/python')))

# application imports
# from app import create_app
from app import db
# from config import Config
from modules.locations.model import Country, Region


class Fixtures:

    def __init__(self, app):

        # init att and prep fixtures
        # app = create_app(Config)
        self.app = app
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://api_admin:passpass@localhost:5432/api_db_test'
        self.app.config['CRYPT_SYM_SECRET_KEY'] = 'VEsuvPZ2W5M8Hb8s7cddMyAMB3g9LPf8VmC4hFmJWckG5htZfgybREBeDa2WaUDs'
        self.app.config['CRYPT_DIGEST_SALT'] = 'mTqjD2YZKU4SXwT7uADbA5bndcc2meEz9PWgX56acdZUZpKn9X82SaJ67F8x8XAK'
        self.model_classes = [Country, Region]
        self.PY_YAML_FIXTURES_DIR = os.path.normpath(
            os.path.join(SCRIPT_DIR, '../../../../data/fixtures/test'))


    def setup(self):
        # load new fixtures
        with self.app.app_context():
            db.drop_all()
            db.create_all()

            factory = SQLAlchemyModelFactory(db.session, self.model_classes)
            loader = FixturesLoader(factory, fixture_dirs=[self.PY_YAML_FIXTURES_DIR])

            loader.create_all(lambda identifier, model, created: print(
                '{action} {identifier}: {model}'.format(
                    action='Creating' if created else 'Updating',
                    identifier=identifier.key,
                    model=repr(model)
                )))


    def teardown(self):
        # wipe database
        with self.app.app_context():
            db.drop_all()
