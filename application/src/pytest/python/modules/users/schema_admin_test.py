from copy import copy

import pytest

from app import create_app
from config import Config
from modules.users.schema_admin import UserAdminSchema, \
    UserTermsOfServiceAdminSchema
from modules.users.model import User, UserTermsOfService
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
def test_user_schema_dump(app):
    user = User.query.get(2)
    result = UserAdminSchema().dump(user)
    assert len(result) == 13
    assert result['id'] == 2
    assert result['username'] == 'user2'
    assert result['email'] == 'user2@test.com'
    assert len(result['roles']) == 1
    assert result['roles'][0]['id'] == 1
    assert result['roles'][0]['name'] == 'USER'
    assert result['uri'] == 'http://localhost/user/2'
    assert len(result['terms_of_services']) == 2
    assert result['terms_of_services'][0]['accept_date'] == \
        "2019-01-17T08:00:00+0000"
    assert result['terms_of_services'][0]['ip_address'] == '1.1.1.2'
    assert result['terms_of_services'][0]['terms_of_service']['id'] == 2
    assert result['terms_of_services'][0]['terms_of_service']['version'] == \
        '1.1'
    assert len(result['profile']) == 3
    assert result['profile']['first_name'] == "Lynne"
    assert result['profile']['last_name'] == "Harford"
    assert result['profile']['joined_at'] == "2018-12-07T00:00:00+0000"
    assert result['password_changed_at'] == '2018-12-08T00:00:00+0000'
    assert result['is_verified'] is True
    assert result['status'] == User.STATUS_ENABLED
    assert result['status_changed_at'] == '2018-12-07T00:00:00+0000'
    assert result['created_at'] == '2018-12-05T00:00:00+0000'
    assert result['updated_at'] == '2018-12-06T00:00:00+0000'


@pytest.mark.integration
@pytest.mark.admin_api
def test_user_schema_dump(app):
    utos = UserTermsOfService.query.get((1, 1))
    result = UserTermsOfServiceAdminSchema().dump(utos)
    assert len(result) == 6
    assert result['accept_date'] == '2018-12-03T08:00:00+0000'
    assert result['ip_address'] == '1.1.1.1'
    assert result['created_at'] == '2018-12-01T08:00:00+0000'
    assert result['updated_at'] == '2018-12-02T08:00:00+0000'
    assert len(result['user']) == 3
    assert result['user']['id'] == 1
    assert result['user']['username'] == 'user1'
    assert result['user']['uri'] == 'http://localhost/user/1'
    assert len(result['terms_of_service']) == 2
    assert result['terms_of_service']['id'] == 1
    assert result['terms_of_service']['version'] == '1.0'
