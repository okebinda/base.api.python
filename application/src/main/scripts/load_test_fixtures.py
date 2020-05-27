import os
import sys

from py_yaml_fixtures import FixturesLoader
from py_yaml_fixtures.factories.sqlalchemy import SQLAlchemyModelFactory

# include application directory in import path
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, '../python')))

# application imports
from app import create_app
from app import db
from config import Config
from modules.locations.model import Country, Region
from modules.app_keys.model import AppKey
from modules.roles.model import Role
from modules.administrators.model import Administrator, \
    AdministratorPasswordHistory
from modules.terms_of_services.model import TermsOfService
from modules.users.model import User, UserPasswordHistory, UserTermsOfService
from modules.user_profiles.model import UserProfile
from modules.logins.model import Login

# init att and prep fixtures
app = create_app(Config)
model_classes = [Country, Region, AppKey, Role, Administrator,
                 AdministratorPasswordHistory, TermsOfService, User,
                 UserPasswordHistory, UserTermsOfService, UserProfile,
                 Login]
PY_YAML_FIXTURES_DIR = os.path.normpath(
    os.path.join(SCRIPT_DIR, '../../../../data/fixtures/test'))

# wipe database and load new fixtures
with app.app_context():
    db.drop_all()
    db.create_all()

    factory = SQLAlchemyModelFactory(db.session, model_classes)
    loader = FixturesLoader(factory, fixture_dirs=[PY_YAML_FIXTURES_DIR])

    loader.create_all(lambda identifier, model, created: print(
        '{action} {identifier}: {model}'.format(
            action='Creating' if created else 'Updating',
            identifier=identifier.key,
            model=repr(model)
        )))
