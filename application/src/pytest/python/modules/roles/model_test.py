import pytest

from app import create_app
from config import Config
from modules.roles.model import Role
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
def test_role_get_1(app):
    role = Role.query.get(1)
    assert role.id == 1
    assert role.name == 'USER'
    assert role.is_admin_role == False
    assert role.priority == 100
    assert role.login_lockout_policy == False
    assert role.login_max_attempts == 10
    assert role.login_timeframe == 600
    assert role.login_ban_time == 1800
    assert role.login_ban_by_ip == True
    assert role.password_policy == False
    assert role.password_reuse_history == 10
    assert role.password_reset_days == 365
    assert role.created_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-01-01T00:00:00+0000"
    assert role.updated_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-01-02T00:00:00+0000"
