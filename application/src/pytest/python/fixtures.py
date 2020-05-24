import os
import sys

from py_yaml_fixtures import FixturesLoader
from py_yaml_fixtures.factories.sqlalchemy import SQLAlchemyModelFactory

# include application directory in import path
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR,
                                              '../../../main/python')))

# application imports
# from app import create_app
from app import db
# from config import Config
from modules.locations.model import Country, Region
from modules.app_keys.model import AppKey
from modules.roles.model import Role
from modules.administrators.model import Administrator, \
    AdministratorPasswordHistory


class Fixtures:

    def __init__(self, app):

        # init att and prep fixtures
        self.app = app
        self.model_classes = [Country, Region, AppKey, Role, Administrator,
                              AdministratorPasswordHistory]
        self.PY_YAML_FIXTURES_DIR = os.path.normpath(
            os.path.join(SCRIPT_DIR, '../../../../data/fixtures/test'))


    def setup(self):
        # load new fixtures
        with self.app.app_context():
            db.drop_all()
            db.create_all()

            factory = SQLAlchemyModelFactory(db.session, self.model_classes)
            loader = FixturesLoader(factory,
                                    fixture_dirs=[self.PY_YAML_FIXTURES_DIR])

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
