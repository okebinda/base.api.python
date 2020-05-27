from copy import copy

import pytest

from app import create_app
from config import Config
from modules.roles.schema_admin import RoleSchema
from modules.roles.model import Role
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
@pytest.mark.admin_api
def test_role_schema_dump(app):
    role = Role.query.get(1)
    result = RoleSchema().dump(role)
    assert len(result) == 14
    assert result['id'] == 1
    assert result['name'] == 'USER'
    assert result['is_admin_role'] is False
    assert result['priority'] == 100
    assert result['login_lockout_policy'] is False
    assert result['login_max_attempts'] == 10
    assert result['login_timeframe'] == 600
    assert result['login_ban_time'] == 1800
    assert result['login_ban_by_ip'] is True
    assert result['password_policy'] is False
    assert result['password_reuse_history'] == 10
    assert result['password_reset_days'] == 365
    assert result['created_at'] == '2018-01-01T00:00:00+0000'
    assert result['updated_at'] == '2018-01-02T00:00:00+0000'
