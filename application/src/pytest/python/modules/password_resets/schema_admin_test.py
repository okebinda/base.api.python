from copy import copy

import pytest

from app import create_app
from config import Config
from modules.password_resets.schema_admin import PasswordResetSchema
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
@pytest.mark.admin_api
def test_login_schema_dump(app):
    pr = PasswordReset.query.get(1)
    result = PasswordResetSchema().dump(pr)
    assert len(result) == 10
    assert result['id'] == 1
    assert result['user']['id'] == 1
    assert result['user']['username'] == 'user1'
    assert result['user']['uri'] == 'http://localhost/user/1'
    assert result['code'] == 'HD7SF2'
    assert result['is_used'] is True
    assert result['requested_at'] == '2019-01-10T07:13:49+0000'
    assert result['ip_address'] == '1.1.1.1'
    assert result['status'] == 1
    assert result['status_changed_at'] == '2019-01-12T00:00:00+0000'
    assert result['created_at'] == '2019-01-10T00:00:00+0000'
    assert result['updated_at'] == '2019-01-11T00:00:00+0000'
