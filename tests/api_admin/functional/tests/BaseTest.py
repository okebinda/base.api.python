from flask_testing import TestCase
from fixture import SQLAlchemyFixture
from fixture.style import NamedDataStyle

from test_fixtures import *
from . import models

# application imports
from app import db
from app.api_admin import create_app
from app.Config import Config

    
class BaseTest(TestCase):

    def create_app(self):
        app = create_app(Config)
        app.config['TESTING'] = True
        return app
        
    def setUp(self):
        # db.drop_all()
        db.create_all()
        dbfixture = SQLAlchemyFixture(
            engine=db.engine, env=models,
            style=NamedDataStyle())
        data = dbfixture.data(CountryData, RegionData, AppKeyData, AdministratorData,
            TermsOfServiceData, UserProfileData, UserTermsOfServiceData, LoginData,
            PasswordResetData, NotificationData,)
        data.setup()
        dbfixture.dispose()

        # import sys
        # sys.exit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
