from copy import copy

import pytest

from app import create_app
from config import Config
from modules.user_account.schema_admin import UserAccountAdminSchema
from modules.administrators.model import Administrator
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
def test_user_account_admin_schema_dump(app):
    admin1 = Administrator.query.get(1)
    result = UserAccountAdminSchema().dump(admin1)
    assert len(result) == 8
    assert result['id'] == 1
    assert result['username'] == 'admin1'
    assert result['email'] == 'admin1@test.com'
    assert result['first_name'] == 'Tommy'
    assert result['last_name'] == 'Lund'
    assert result['uri'] == 'http://localhost/administrator/1'
    assert result['password_changed_at'] == '2018-11-04T00:00:00+0000'
    assert result['joined_at'] == '2018-11-01T00:00:00+0000'
