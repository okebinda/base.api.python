import pytest

from app import create_app
from config import Config
from modules.password_resets.model import PasswordReset
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
def test_password_reset_get_1(app):
    password_reset = PasswordReset.query.get(1)
    assert password_reset.id == 1
    assert password_reset.user_id == 1
    assert password_reset.user.id == 1
    assert password_reset.code == 'HD7SF2'
    assert password_reset.is_used is True
    assert password_reset.requested_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2019-01-10T07:13:49+0000"
    assert password_reset.ip_address == '1.1.1.1'
    assert password_reset.status == 1
    assert password_reset.status_changed_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2019-01-12T00:00:00+0000"
    assert password_reset.created_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2019-01-10T00:00:00+0000"
    assert password_reset.updated_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2019-01-11T00:00:00+0000"
