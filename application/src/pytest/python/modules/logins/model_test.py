import pytest

from app import create_app
from config import Config
from modules.logins.model import Login
from fixtures import Fixtures


@pytest.fixture
def app(request):
    Config.TESTING = True
    app = create_app(Config)

    if 'unit' in request.keywords:
        # unit tests don't get data fixtures
        yield app
    else:
        # other tests need the test data set
        fixtures = Fixtures(app)
        fixtures.setup()
        yield app
        fixtures.teardown()


# INTEGRATION TESTS


@pytest.mark.integration
def test_login_get_1(app):
    login = Login.query.get(1)
    assert login.id == 1
    assert login.user_id == 1
    assert login.username == 'admin1'
    assert login.ip_address == '1.1.1.1'
    assert login.api == 1
    assert login.success == True
    assert login.attempt_date.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-12-01T08:32:55+0000"
    assert login.created_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-12-01T08:32:56+0000"
    assert login.updated_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-12-01T08:32:57+0000"
