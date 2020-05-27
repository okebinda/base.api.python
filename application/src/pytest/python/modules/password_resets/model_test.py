from copy import copy

import pytest

from app import create_app
from config import Config
from modules.password_resets.model import PasswordReset
from fixtures import Fixtures


@pytest.fixture
def app(request):
    config = copy(Config)
    config.TESTING = True
    config.APP_TYPE = 'admin' if 'admin_api' in request.keywords else 'public'
    app = create_app(config)

    if 'unit' in request.keywords:
        yield app
    else:
        fixtures = Fixtures(app)
        fixtures.setup()
        yield app
        fixtures.teardown()


# INTEGRATION TESTS


@pytest.mark.integration
def test_login_get_1(app):
    pr = PasswordReset.query.get(1)
    assert pr.id == 1
    assert pr.user_id == 1
    assert pr.user.id == 1
    assert pr.code == 'HD7SF2'
    assert pr.is_used == True
    assert pr.requested_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2019-01-10T07:13:49+0000"
    assert pr.ip_address == '1.1.1.1'
    assert pr.status == 1
    assert pr.status_changed_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2019-01-12T00:00:00+0000"
    assert pr.created_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2019-01-10T00:00:00+0000"
    assert pr.updated_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2019-01-11T00:00:00+0000"
