from copy import copy

import pytest

from app import create_app
from config import Config
from modules.logins.schema_admin import LoginSchema
from modules.logins.model import Login
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
def test_login_schema_dump(app):
    login = Login.query.get(1)
    result = LoginSchema().dump(login)
    assert len(result) == 9
    assert result['id'] == 1
    assert result['user_id'] == 1
    assert result['username'] == 'admin1'
    assert result['ip_address'] == '1.1.1.1'
    assert result['api'] == 1
    assert result['success'] == True
    assert result['attempt_date'] == '2018-12-01T08:32:55+0000'
    assert result['created_at'] == '2018-12-01T08:32:56+0000'
    assert result['updated_at'] == '2018-12-01T08:32:57+0000'
