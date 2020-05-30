from copy import copy

import pytest

from app import create_app
from config import Config
from modules.user_account.schema_public import UserAccountSchema
from modules.users.model import User
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
    user2 = User.query.get(2)
    output = {
        'id': user2.id,
        'username': user2.username,
        'email': user2.email,
        'password_changed_at': user2.password_changed_at,
        'is_verified': user2.is_verified,
        'first_name': user2.profile.first_name,
        'last_name': user2.profile.last_name,
        'joined_at': user2.profile.joined_at,
    }
    result = UserAccountSchema().dump(output)
    assert len(result) == 8
    assert result['id'] == 2
    assert result['username'] == 'user2'
    assert result['email'] == 'user2@test.com'
    assert result['first_name'] == 'Lynne'
    assert result['last_name'] == 'Harford'
    assert result['password_changed_at'] == '2018-12-08T00:00:00+0000'
    assert result['joined_at'] == '2018-12-07T00:00:00+0000'
    assert result['is_verified'] is True
