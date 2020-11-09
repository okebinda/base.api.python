from copy import copy
import re
import base64

import pytest
from werkzeug.exceptions import NotFound, Unauthorized
from sqlalchemy.orm.exc import NoResultFound

from fixtures import Fixtures
from app import create_app
from config import Config
from modules.roles.routes_admin import get_roles, post_roles, get_role, \
    put_role, delete_role
from modules.administrators.model import Administrator
from modules.roles.model import Role
from modules.app_keys.model import AppKey


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


# UNIT TESTS


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_roles(app, mocker):
    expected_status = 200
    expected_length = 2
    expected_properties = ['created_at', 'id', 'is_admin_role',
                           'login_ban_by_ip', 'login_ban_time',
                           'login_lockout_policy', 'login_max_attempts',
                           'login_timeframe', 'name', 'password_policy',
                           'password_reset_days', 'password_reuse_history',
                           'priority', 'updated_at']
    expected_limit = 10
    expected_page = 1
    expected_total = 2

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [Role()] * expected_length
    query_mock.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    result = get_roles()

    assert result[1] == expected_status
    assert len(result[0].json['roles']) == expected_length
    assert result[0].json['roles'][0] == {
        x: None for x in expected_properties}
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_roles_limit_10_page_2_of_3(app, mocker):
    expected_status = 200
    expected_length = 10
    expected_properties = ['created_at', 'id', 'is_admin_role',
                           'login_ban_by_ip', 'login_ban_time',
                           'login_lockout_policy', 'login_max_attempts',
                           'login_timeframe', 'name', 'password_policy',
                           'password_reset_days', 'password_reuse_history',
                           'priority', 'updated_at']
    expected_limit = 10
    expected_page = 2
    expected_total = 25
    expected_previous_uri = 'http://localhost/roles/1/10'
    expected_next_uri = 'http://localhost/roles/3/10'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [Role()] * expected_length
    query_mock.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    result = get_roles(expected_page, expected_limit)

    assert result[1] == expected_status
    assert len(result[0].json['roles']) == expected_length
    assert result[0].json['roles'][0] == {
        x: None for x in expected_properties}
    assert result[0].json['previous_uri'] == expected_previous_uri
    assert result[0].json['next_uri'] == expected_next_uri
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_roles_user(app, mocker):
    expected_status = 200
    expected_length = 2
    expected_properties = ['created_at', 'id', 'is_admin_role',
                           'login_ban_by_ip', 'login_ban_time',
                           'login_lockout_policy', 'login_max_attempts',
                           'login_timeframe', 'name', 'password_policy',
                           'password_reset_days', 'password_reuse_history',
                           'priority', 'updated_at']
    expected_limit = 10
    expected_page = 1
    expected_total = 2

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .order_by.return_value \
        .filter.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [Role()] * expected_length
    query_mock.return_value \
        .order_by.return_value \
        .filter.return_value \
        .count.return_value = expected_total

    result = get_roles(expected_page, expected_limit, 'user')

    assert result[1] == expected_status
    assert len(result[0].json['roles']) == expected_length
    assert result[0].json['roles'][0] == {
        x: None for x in expected_properties}
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_roles_empty(app, mocker):
    expected_status = 204
    expected_content = ''

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = []
    query_mock.return_value \
        .order_by.return_value \
        .count.return_value = 15

    result = get_roles(5, 10)

    assert result[1] == expected_status
    assert result[0] == expected_content


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_roles_route(app, mocker, client):
    expected_status = 200
    expected_length = 10
    expected_limit = 10
    expected_page = 1
    expected_total = 15
    expected_next_uri = 'http://localhost/roles/2/10'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login db query
    role2 = Role()
    role2.id = 2
    role2.name = 'SUPER_ADMIN'
    role2.password_reset_days = 365

    admin1 = Administrator()
    admin1.id = 1
    admin1.password = 'admin1pass'
    admin1.roles = [role2]

    query_mock.return_value \
        .filter.return_value \
        .first.return_value = admin1

    auth_db_mock = mocker.patch('modules.administrators.authentication.db')
    auth_db_mock.add.return_value = None
    auth_db_mock.commit.return_value = None

    query_mock.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [Role()] * expected_length
    query_mock.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    # mock user login
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get("/roles?app_key=123",
                          headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert len(response.json['roles']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_roles_limit_5_page_2_of_3_route(app, mocker, client):
    expected_status = 200
    expected_length = 5
    expected_limit = 5
    expected_page = 2
    expected_total = 12
    expected_next_uri = 'http://localhost/roles/3/5'
    expected_previous_uri = 'http://localhost/roles/1/5'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login db query
    role2 = Role()
    role2.id = 2
    role2.name = 'SUPER_ADMIN'
    role2.password_reset_days = 365

    admin1 = Administrator()
    admin1.id = 1
    admin1.password = 'admin1pass'
    admin1.roles = [role2]

    query_mock.return_value \
        .filter.return_value \
        .first.return_value = admin1

    auth_db_mock = mocker.patch('modules.administrators.authentication.db')
    auth_db_mock.add.return_value = None
    auth_db_mock.commit.return_value = None

    query_mock.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [Role()] * expected_length
    query_mock.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    # mock user login
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get(
        "/roles/{}/{}?app_key=123".format(expected_page, expected_limit),
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert len(response.json['roles']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri
    assert response.json['previous_uri'] == expected_previous_uri


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_roles_user_route(app, mocker, client):
    expected_status = 200
    expected_length = 10
    expected_limit = 10
    expected_page = 1
    expected_total = 15
    expected_next_uri = 'http://localhost/roles/user/2/10'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login db query
    role2 = Role()
    role2.id = 2
    role2.name = 'SUPER_ADMIN'
    role2.password_reset_days = 365

    admin1 = Administrator()
    admin1.id = 1
    admin1.password = 'admin1pass'
    admin1.roles = [role2]

    query_mock.return_value \
        .filter.return_value \
        .first.return_value = admin1

    auth_db_mock = mocker.patch('modules.administrators.authentication.db')
    auth_db_mock.add.return_value = None
    auth_db_mock.commit.return_value = None

    query_mock.return_value \
        .order_by.return_value \
        .filter.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [Role()] * expected_length
    query_mock.return_value \
        .order_by.return_value \
        .filter.return_value \
        .count.return_value = expected_total

    # mock user login
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get("/roles/user?app_key=123",
                          headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert len(response.json['roles']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_roles_empty_route(app, mocker, client):
    expected_status = 204
    expected_json = None

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login db query
    role2 = Role()
    role2.id = 2
    role2.name = 'SUPER_ADMIN'
    role2.password_reset_days = 365

    admin1 = Administrator()
    admin1.id = 1
    admin1.password = 'admin1pass'
    admin1.roles = [role2]

    query_mock.return_value \
        .filter.return_value \
        .first.return_value = admin1

    auth_db_mock = mocker.patch('modules.administrators.authentication.db')
    auth_db_mock.add.return_value = None
    auth_db_mock.commit.return_value = None

    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = []
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = 15

    # mock user login
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get("/roles/3?app_key=123",
                          headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_roles_route_no_app_key(app, client):
    expected_status = 401

    response = client.get("/roles")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_roles_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.get("/roles?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_roles_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.get("/roles?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_role_by_id_ok(app, mocker):
    expected_status = 200
    expected_properties = ['created_at', 'id', 'is_admin_role',
                           'login_ban_by_ip', 'login_ban_time',
                           'login_lockout_policy', 'login_max_attempts',
                           'login_timeframe', 'name', 'password_policy',
                           'password_reset_days', 'password_reuse_history',
                           'priority', 'updated_at']

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = Role()

    result = get_role(1)

    assert result[1] == expected_status
    assert result[0].json['role'] == {x: None for x in expected_properties}


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_role_by_name_ok(app, mocker):
    expected_status = 200
    expected_properties = ['created_at', 'id', 'is_admin_role',
                           'login_ban_by_ip', 'login_ban_time',
                           'login_lockout_policy', 'login_max_attempts',
                           'login_timeframe', 'name', 'password_policy',
                           'password_reset_days', 'password_reuse_history',
                           'priority', 'updated_at']

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = Role()

    result = get_role('USER')

    assert result[1] == expected_status
    assert result[0].json['role'] == {x: None for x in expected_properties}


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_role_by_id_not_found(app, mocker):
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = None

    try:
        get_role(250)
        assert False
    except NotFound:
        assert True


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_role_by_name_not_found(app, mocker):
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = None

    try:
        get_role(None, 'bad_name')
        assert False
    except NotFound:
        assert True


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_role_by_id_route_ok(app, mocker, client):
    expected_status = 200

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login db query
    role2 = Role()
    role2.id = 2
    role2.name = 'SUPER_ADMIN'
    role2.password_reset_days = 365

    admin1 = Administrator()
    admin1.id = 1
    admin1.password = 'admin1pass'
    admin1.roles = [role2]

    query_mock.return_value \
        .filter.return_value \
        .first.return_value = admin1

    auth_db_mock = mocker.patch('modules.administrators.authentication.db')
    auth_db_mock.add.return_value = None
    auth_db_mock.commit.return_value = None

    # mock resource query
    query_mock.return_value \
        .get.return_value = Role()

    # mock user login
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get("/role/1?app_key=123",
                          headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert 'role' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_role_by_id_route_no_app_key(app, client):
    expected_status = 401

    response = client.get("/role/1")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_role_by_id_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.get("/role/1?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_role_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.get("/role/1?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_roles_ok(app, mocker):
    expected_status = 201
    expected_m_length = 14
    expected_m_id = None
    expected_m_name = "SOME_ROLE"
    expected_m_is_admin_role = False
    expected_m_priority = 125
    expected_m_login_lockout_policy = True
    expected_m_login_max_attempts = 5
    expected_m_login_timeframe = 450
    expected_m_login_ban_time = 1200
    expected_m_login_ban_by_ip = False
    expected_m_password_policy = True
    expected_m_password_reuse_history = 12
    expected_m_password_reset_days = 180
    expected_m_created_at = None
    expected_m_updated_at = None

    request_mock = mocker.patch('modules.roles.routes_admin.request')
    request_mock.json = {
        'name': expected_m_name,
        'is_admin_role': expected_m_is_admin_role,
        "priority": expected_m_priority,
        "login_lockout_policy": expected_m_login_lockout_policy,
        "login_max_attempts": expected_m_login_max_attempts,
        "login_timeframe": expected_m_login_timeframe,
        "login_ban_time": expected_m_login_ban_time,
        "login_ban_by_ip": expected_m_login_ban_by_ip,
        "password_policy": expected_m_password_policy,
        "password_reuse_history": expected_m_password_reuse_history,
        "password_reset_days": expected_m_password_reset_days
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    db_mock = mocker.patch('modules.roles.routes_admin.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    result = post_roles()

    assert result[1] == expected_status
    assert 'role' in result[0].json
    assert len(result[0].json['role']) == expected_m_length
    assert result[0].json['role']['id'] == expected_m_id
    assert result[0].json['role']['name'] == expected_m_name
    assert result[0].json['role']['is_admin_role'] == expected_m_is_admin_role
    assert result[0].json['role']['priority'] == expected_m_priority
    assert result[0].json['role']['login_lockout_policy'] == \
        expected_m_login_lockout_policy
    assert result[0].json['role']['login_max_attempts'] == \
        expected_m_login_max_attempts
    assert result[0].json['role']['login_timeframe'] == \
        expected_m_login_timeframe
    assert result[0].json['role']['login_ban_time'] == \
        expected_m_login_ban_time
    assert result[0].json['role']['login_ban_by_ip'] == \
        expected_m_login_ban_by_ip
    assert result[0].json['role']['password_policy'] == \
        expected_m_password_policy
    assert result[0].json['role']['password_reuse_history'] == \
        expected_m_password_reuse_history
    assert result[0].json['role']['password_reset_days'] == \
        expected_m_password_reset_days
    assert result[0].json['role']['created_at'] == expected_m_created_at
    assert result[0].json['role']['updated_at'] == expected_m_updated_at


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_role_unique_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {'name': ['Value must be unique.']}}

    request_mock = mocker.patch('modules.roles.routes_admin.request')
    request_mock.json = {
        'name': "USER",
        'is_admin_role': False,
        "priority": 100,
        "login_lockout_policy": True,
        "login_max_attempts": 5,
        "login_timeframe": 600,
        "login_ban_time": 1800,
        "login_ban_by_ip": False,
        "password_policy": True,
        "password_reuse_history": 24,
        "password_reset_days": 365
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = Role()

    result = post_roles()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_roles_required_fail(app, mocker):
    expected_status = 400
    expected_json = {
        "error": {
            "foo": ["Unknown field."],
            "is_admin_role": ["Missing data for required field."],
            "login_ban_by_ip": ["Missing data for required field."],
            "login_ban_time": ["Missing data for required field."],
            "login_lockout_policy": ["Missing data for required field."],
            "login_max_attempts": ["Missing data for required field."],
            "login_timeframe": ["Missing data for required field."],
            "name": ["Missing data for required field."],
            "password_policy": ["Missing data for required field."],
            "password_reset_days": ["Missing data for required field."],
            "password_reuse_history": ["Missing data for required field."],
            "priority": ["Missing data for required field."]
        }
    }

    request_mock = mocker.patch('modules.roles.routes_admin.request')
    request_mock.json = {'foo': "bar"}

    result = post_roles()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_roles_min_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'name': ['Value must be between 2 and 32 characters long.'],
        }
    }

    request_mock = mocker.patch('modules.roles.routes_admin.request')
    request_mock.json = {
        'name': "U",
        'is_admin_role': False,
        "priority": 100,
        "login_lockout_policy": True,
        "login_max_attempts": 5,
        "login_timeframe": 600,
        "login_ban_time": 1800,
        "login_ban_by_ip": False,
        "password_policy": True,
        "password_reuse_history": 24,
        "password_reset_days": 365
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = post_roles()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_roles_max_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'name': ['Value must be between 2 and 32 characters long.'],
        }
    }

    request_mock = mocker.patch('modules.roles.routes_admin.request')
    request_mock.json = {
        'name': "3J36V3565FtBxrjNRLf5DDYPmKkY4zpJa",
        'is_admin_role': False,
        "priority": 100,
        "login_lockout_policy": True,
        "login_max_attempts": 5,
        "login_timeframe": 600,
        "login_ban_time": 1800,
        "login_ban_by_ip": False,
        "password_policy": True,
        "password_reuse_history": 24,
        "password_reset_days": 365
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = post_roles()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_roles_type_fail(app, mocker):
    expected_status = 400
    expected_json = {
        "error": {
            "is_admin_role": ["Not a valid boolean."],
            "login_ban_by_ip": ["Not a valid boolean."],
            "login_ban_time": ["Not a valid integer."],
            "login_lockout_policy": ["Not a valid boolean."],
            "login_max_attempts": ["Not a valid integer."],
            "login_timeframe": ["Not a valid integer."],
            "name": ["Not a valid string."],
            "password_policy": ["Not a valid boolean."],
            "password_reset_days": ["Not a valid integer."],
            "password_reuse_history": ["Not a valid integer."],
            "priority": ["Not a valid integer."]
        }
    }

    request_mock = mocker.patch('modules.roles.routes_admin.request')
    request_mock.json = {
        "name": 123,
        "is_admin_role": "bad",
        "priority": "bad",
        "login_lockout_policy": "bad",
        "login_max_attempts": "bad",
        "login_timeframe": "bad",
        "login_ban_time": "bad",
        "login_ban_by_ip": "bad",
        "password_policy": "bad",
        "password_reuse_history": "bad",
        "password_reset_days": "bad"
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = post_roles()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_roles_route_ok(app, mocker, client):
    expected_status = 201
    expected_m_length = 14
    expected_m_id = None
    expected_m_name = "SOME_ROLE"
    expected_m_is_admin_role = False
    expected_m_priority = 125
    expected_m_login_lockout_policy = True
    expected_m_login_max_attempts = 5
    expected_m_login_timeframe = 450
    expected_m_login_ban_time = 1200
    expected_m_login_ban_by_ip = False
    expected_m_password_policy = True
    expected_m_password_reuse_history = 12
    expected_m_password_reset_days = 180
    expected_m_created_at = None
    expected_m_updated_at = None

    data = {
        'name': expected_m_name,
        'is_admin_role': expected_m_is_admin_role,
        "priority": expected_m_priority,
        "login_lockout_policy": expected_m_login_lockout_policy,
        "login_max_attempts": expected_m_login_max_attempts,
        "login_timeframe": expected_m_login_timeframe,
        "login_ban_time": expected_m_login_ban_time,
        "login_ban_by_ip": expected_m_login_ban_by_ip,
        "password_policy": expected_m_password_policy,
        "password_reuse_history": expected_m_password_reuse_history,
        "password_reset_days": expected_m_password_reset_days
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login db query
    role2 = Role()
    role2.id = 2
    role2.name = 'SUPER_ADMIN'
    role2.password_reset_days = 365

    admin1 = Administrator()
    admin1.id = 1
    admin1.password = 'admin1pass'
    admin1.roles = [role2]

    query_mock.return_value \
        .filter.return_value \
        .first.side_effect = [admin1, None]

    auth_db_mock = mocker.patch('modules.administrators.authentication.db')
    auth_db_mock.add.return_value = None
    auth_db_mock.commit.return_value = None

    db_mock = mocker.patch('modules.roles.routes_admin.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    # mock user login
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.post("/roles?app_key=123", json=data,
                           headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert 'role' in response.json
    assert len(response.json['role']) == expected_m_length
    assert response.json['role']['id'] == expected_m_id
    assert response.json['role']['name'] == expected_m_name
    assert response.json['role']['is_admin_role'] == expected_m_is_admin_role
    assert response.json['role']['priority'] == expected_m_priority
    assert response.json['role']['login_lockout_policy'] == \
        expected_m_login_lockout_policy
    assert response.json['role']['login_max_attempts'] == \
        expected_m_login_max_attempts
    assert response.json['role']['login_timeframe'] == \
        expected_m_login_timeframe
    assert response.json['role']['login_ban_time'] == \
        expected_m_login_ban_time
    assert response.json['role']['login_ban_by_ip'] == \
        expected_m_login_ban_by_ip
    assert response.json['role']['password_policy'] == \
        expected_m_password_policy
    assert response.json['role']['password_reuse_history'] == \
        expected_m_password_reuse_history
    assert response.json['role']['password_reset_days'] == \
        expected_m_password_reset_days
    assert response.json['role']['created_at'] == expected_m_created_at
    assert response.json['role']['updated_at'] == expected_m_updated_at


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_role_route_no_app_key(app, client):
    expected_status = 401

    response = client.post("/roles")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_role_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.post("/roles?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_role_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.post("/roles?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_role_ok(app, mocker):
    expected_status = 200
    expected_m_length = 14
    expected_m_id = 1
    expected_m_name = "USER_A"
    expected_m_is_admin_role = True
    expected_m_priority = 101
    expected_m_login_lockout_policy = True
    expected_m_login_max_attempts = 11
    expected_m_login_timeframe = 601
    expected_m_login_ban_time = 1801
    expected_m_login_ban_by_ip = False
    expected_m_password_policy = True
    expected_m_password_reuse_history = 11
    expected_m_password_reset_days = 366
    expected_m_created_at = None
    expected_m_updated_at = None

    request_mock = mocker.patch('modules.roles.routes_admin.request')
    request_mock.json = {
        'name': expected_m_name,
        'is_admin_role': expected_m_is_admin_role,
        "priority": expected_m_priority,
        "login_lockout_policy": expected_m_login_lockout_policy,
        "login_max_attempts": expected_m_login_max_attempts,
        "login_timeframe": expected_m_login_timeframe,
        "login_ban_time": expected_m_login_ban_time,
        "login_ban_by_ip": expected_m_login_ban_by_ip,
        "password_policy": expected_m_password_policy,
        "password_reuse_history": expected_m_password_reuse_history,
        "password_reset_days": expected_m_password_reset_days
    }

    role_1 = Role()
    role_1.id = expected_m_id

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = role_1
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    db_mock = mocker.patch('modules.roles.routes_admin.db')
    db_mock.commit.return_value = None

    result = put_role(expected_m_id)

    assert result[1] == expected_status
    assert 'role' in result[0].json
    assert len(result[0].json['role']) == expected_m_length
    assert result[0].json['role']['id'] == expected_m_id
    assert result[0].json['role']['name'] == expected_m_name
    assert result[0].json['role']['is_admin_role'] == expected_m_is_admin_role
    assert result[0].json['role']['priority'] == expected_m_priority
    assert result[0].json['role']['login_lockout_policy'] == \
        expected_m_login_lockout_policy
    assert result[0].json['role']['login_max_attempts'] == \
        expected_m_login_max_attempts
    assert result[0].json['role']['login_timeframe'] == \
        expected_m_login_timeframe
    assert result[0].json['role']['login_ban_time'] == \
        expected_m_login_ban_time
    assert result[0].json['role']['login_ban_by_ip'] == \
        expected_m_login_ban_by_ip
    assert result[0].json['role']['password_policy'] == \
        expected_m_password_policy
    assert result[0].json['role']['password_reuse_history'] == \
        expected_m_password_reuse_history
    assert result[0].json['role']['password_reset_days'] == \
        expected_m_password_reset_days
    assert result[0].json['role']['created_at'] == expected_m_created_at
    assert result[0].json['role']['updated_at'] == expected_m_updated_at


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_role_unique_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {'name': ['Value must be unique.']}}

    request_mock = mocker.patch('modules.roles.routes_admin.request')
    request_mock.json = {
        'name': "USER",
        'is_admin_role': False,
        "priority": 100,
        "login_lockout_policy": True,
        "login_max_attempts": 5,
        "login_timeframe": 600,
        "login_ban_time": 1800,
        "login_ban_by_ip": False,
        "password_policy": True,
        "password_reuse_history": 24,
        "password_reset_days": 365
    }

    role_1 = Role()
    role_1.id = 1

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = role_1
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = Role()

    result = put_role(1)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_role_required_fail(app, mocker):
    expected_status = 400
    expected_json = {
        "error": {
            "foo": ["Unknown field."],
            "is_admin_role": ["Missing data for required field."],
            "login_ban_by_ip": ["Missing data for required field."],
            "login_ban_time": ["Missing data for required field."],
            "login_lockout_policy": ["Missing data for required field."],
            "login_max_attempts": ["Missing data for required field."],
            "login_timeframe": ["Missing data for required field."],
            "name": ["Missing data for required field."],
            "password_policy": ["Missing data for required field."],
            "password_reset_days": ["Missing data for required field."],
            "password_reuse_history": ["Missing data for required field."],
            "priority": ["Missing data for required field."]
        }
    }

    request_mock = mocker.patch('modules.roles.routes_admin.request')
    request_mock.json = {'foo': "bar"}

    role_1 = Role()
    role_1.id = 1

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = role_1
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_role(1)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_role_min_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'name': ['Value must be between 2 and 32 characters long.'],
        }
    }

    request_mock = mocker.patch('modules.roles.routes_admin.request')
    request_mock.json = {
        'name': "U",
        'is_admin_role': False,
        "priority": 100,
        "login_lockout_policy": True,
        "login_max_attempts": 5,
        "login_timeframe": 600,
        "login_ban_time": 1800,
        "login_ban_by_ip": False,
        "password_policy": True,
        "password_reuse_history": 24,
        "password_reset_days": 365
    }

    role_1 = Role()
    role_1.id = 1

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = role_1
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_role(1)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_role_max_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'name': ['Value must be between 2 and 32 characters long.'],
        }
    }

    request_mock = mocker.patch('modules.roles.routes_admin.request')
    request_mock.json = {
        'name': "3J36V3565FtBxrjNRLf5DDYPmKkY4zpJa",
        'is_admin_role': False,
        "priority": 100,
        "login_lockout_policy": True,
        "login_max_attempts": 5,
        "login_timeframe": 600,
        "login_ban_time": 1800,
        "login_ban_by_ip": False,
        "password_policy": True,
        "password_reuse_history": 24,
        "password_reset_days": 365
    }

    role_1 = Role()
    role_1.id = 1

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = role_1
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_role(1)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_role_type_fail(app, mocker):
    expected_status = 400
    expected_json = {
        "error": {
            "is_admin_role": ["Not a valid boolean."],
            "login_ban_by_ip": ["Not a valid boolean."],
            "login_ban_time": ["Not a valid integer."],
            "login_lockout_policy": ["Not a valid boolean."],
            "login_max_attempts": ["Not a valid integer."],
            "login_timeframe": ["Not a valid integer."],
            "name": ["Not a valid string."],
            "password_policy": ["Not a valid boolean."],
            "password_reset_days": ["Not a valid integer."],
            "password_reuse_history": ["Not a valid integer."],
            "priority": ["Not a valid integer."]
        }
    }

    request_mock = mocker.patch('modules.roles.routes_admin.request')
    request_mock.json = {
        "name": 123,
        "is_admin_role": "bad",
        "priority": "bad",
        "login_lockout_policy": "bad",
        "login_max_attempts": "bad",
        "login_timeframe": "bad",
        "login_ban_time": "bad",
        "login_ban_by_ip": "bad",
        "password_policy": "bad",
        "password_reuse_history": "bad",
        "password_reset_days": "bad"
    }

    role_1 = Role()
    role_1.id = 1

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = role_1
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_role(1)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_role_route_ok(app, mocker, client):
    expected_status = 200
    expected_m_length = 14
    expected_m_id = 1
    expected_m_name = "USER_A"
    expected_m_is_admin_role = True
    expected_m_priority = 101
    expected_m_login_lockout_policy = True
    expected_m_login_max_attempts = 11
    expected_m_login_timeframe = 601
    expected_m_login_ban_time = 1801
    expected_m_login_ban_by_ip = False
    expected_m_password_policy = True
    expected_m_password_reuse_history = 11
    expected_m_password_reset_days = 366
    expected_m_created_at = None
    expected_m_updated_at = None

    data = {
        'name': expected_m_name,
        'is_admin_role': expected_m_is_admin_role,
        "priority": expected_m_priority,
        "login_lockout_policy": expected_m_login_lockout_policy,
        "login_max_attempts": expected_m_login_max_attempts,
        "login_timeframe": expected_m_login_timeframe,
        "login_ban_time": expected_m_login_ban_time,
        "login_ban_by_ip": expected_m_login_ban_by_ip,
        "password_policy": expected_m_password_policy,
        "password_reuse_history": expected_m_password_reuse_history,
        "password_reset_days": expected_m_password_reset_days
    }

    role_1 = Role()
    role_1.id = expected_m_id

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login db query
    role2 = Role()
    role2.id = 2
    role2.name = 'SUPER_ADMIN'
    role2.password_reset_days = 365

    admin1 = Administrator()
    admin1.id = 1
    admin1.password = 'admin1pass'
    admin1.roles = [role2]

    query_mock.return_value \
        .filter.return_value \
        .first.side_effect = [admin1, None]

    auth_db_mock = mocker.patch('modules.administrators.authentication.db')
    auth_db_mock.add.return_value = None
    auth_db_mock.commit.return_value = None

    query_mock.return_value \
        .get.return_value = role_1

    db_mock = mocker.patch('modules.roles.routes_admin.db')
    db_mock.commit.return_value = None

    # mock user login
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.put(
        "/role/{}?app_key=123".format(expected_m_id),
        json=data,
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert 'role' in response.json
    assert len(response.json['role']) == expected_m_length
    assert response.json['role']['id'] == expected_m_id
    assert response.json['role']['name'] == expected_m_name
    assert response.json['role']['is_admin_role'] == expected_m_is_admin_role
    assert response.json['role']['priority'] == expected_m_priority
    assert response.json['role']['login_lockout_policy'] == \
        expected_m_login_lockout_policy
    assert response.json['role']['login_max_attempts'] == \
        expected_m_login_max_attempts
    assert response.json['role']['login_timeframe'] == \
        expected_m_login_timeframe
    assert response.json['role']['login_ban_time'] == \
        expected_m_login_ban_time
    assert response.json['role']['login_ban_by_ip'] == \
        expected_m_login_ban_by_ip
    assert response.json['role']['password_policy'] == \
        expected_m_password_policy
    assert response.json['role']['password_reuse_history'] == \
        expected_m_password_reuse_history
    assert response.json['role']['password_reset_days'] == \
        expected_m_password_reset_days
    assert response.json['role']['created_at'] == expected_m_created_at
    assert response.json['role']['updated_at'] == expected_m_updated_at


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_role_route_no_app_key(app, client):
    expected_status = 401

    response = client.put("/role/1")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_role_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.put("/role/1?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_role_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.put("/role/1?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_delete_role_ok(app, mocker):
    expected_status = 204
    expected_content = ''

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = Role()

    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    db_mock = mocker.patch('modules.roles.routes_admin.db')
    db_mock.commit.return_value = None

    result = delete_role(1)

    assert result[1] == expected_status
    assert result[0] == expected_content


@pytest.mark.unit
@pytest.mark.admin_api
def test_delete_role_fail(app, mocker):
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = None

    try:
        delete_role(250)
        assert False
    except NotFound:
        assert True


@pytest.mark.unit
@pytest.mark.admin_api
def test_delete_role_route_ok(app, mocker, client):
    expected_status = 204
    expected_json = None

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login db query
    role2 = Role()
    role2.id = 2
    role2.name = 'SUPER_ADMIN'
    role2.password_reset_days = 365

    admin1 = Administrator()
    admin1.id = 1
    admin1.password = 'admin1pass'
    admin1.roles = [role2]

    query_mock.return_value \
        .filter.return_value \
        .first.side_effect = [admin1, None, None]

    auth_db_mock = mocker.patch('modules.administrators.authentication.db')
    auth_db_mock.add.return_value = None
    auth_db_mock.commit.return_value = None

    # mock resource query
    query_mock.return_value \
        .get.return_value = Role()

    # mock db commit
    db_mock = mocker.patch('modules.roles.routes_admin.db')
    db_mock.commit.return_value = None

    # mock user login
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.delete(
        "/role/3?app_key=123",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_delete_role_route_no_app_key(app, client):
    expected_status = 401

    response = client.delete("/role/3")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_delete_role_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.delete("/role/3?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_delete_role_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.delete("/role/3?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


# INTEGRATION TESTS


@pytest.mark.integration
@pytest.mark.admin_api
def test_get_roles_route_with_data(client):
    expected_status = 200
    expected_json = {
        "limit": 10,
        "page": 1,
        "roles": [
            {
                "created_at": "2018-01-01T00:00:00+0000",
                "id": 1,
                "is_admin_role": False,
                "login_ban_by_ip": True,
                "login_ban_time": 1800,
                "login_lockout_policy": False,
                "login_max_attempts": 10,
                "login_timeframe": 600,
                "name": "USER",
                "password_policy": False,
                "password_reset_days": 365,
                "password_reuse_history": 10,
                "priority": 100,
                "updated_at": "2018-01-02T00:00:00+0000"
            },
            {
                "created_at": "2018-01-05T00:00:00+0000",
                "id": 2,
                "is_admin_role": True,
                "login_ban_by_ip": True,
                "login_ban_time": 1800,
                "login_lockout_policy": True,
                "login_max_attempts": 5,
                "login_timeframe": 300,
                "name": "SUPER_ADMIN",
                "password_policy": True,
                "password_reset_days": 90,
                "password_reuse_history": 24,
                "priority": 10,
                "updated_at": "2018-01-06T00:00:00+0000"
            },
            {
                "created_at": "2018-01-10T00:00:00+0000",
                "id": 3,
                "is_admin_role": False,
                "login_ban_by_ip": True,
                "login_ban_time": 1800,
                "login_lockout_policy": True,
                "login_max_attempts": 5,
                "login_timeframe": 300,
                "name": "SERVICE",
                "password_policy": True,
                "password_reset_days": 365,
                "password_reuse_history": 24,
                "priority": 50,
                "updated_at": "2018-01-11T00:00:00+0000"
            },
            {
                "created_at": "2018-01-15T00:00:00+0000",
                "id": 4,
                "is_admin_role": True,
                "login_ban_by_ip": True,
                "login_ban_time": 3600,
                "login_lockout_policy": True,
                "login_max_attempts": 5,
                "login_timeframe": 600,
                "name": "EDITOR",
                "password_policy": True,
                "password_reset_days": 365,
                "password_reuse_history": 24,
                "priority": 75,
                "updated_at": "2018-01-16T00:00:00+0000"
            }
        ],
        "total": 4
    }

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get(
        "/roles?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.integration
@pytest.mark.admin_api
def test_get_role_1_route_with_data(client):
    expected_status = 200
    expected_json = {
        "role": {
            "created_at": "2018-01-01T00:00:00+0000",
            "id": 1,
            "is_admin_role": False,
            "login_ban_by_ip": True,
            "login_ban_time": 1800,
            "login_lockout_policy": False,
            "login_max_attempts": 10,
            "login_timeframe": 600,
            "name": "USER",
            "password_policy": False,
            "password_reset_days": 365,
            "password_reuse_history": 10,
            "priority": 100,
            "updated_at": "2018-01-02T00:00:00+0000"
        }
    }

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get(
        "/role/1?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.integration
@pytest.mark.admin_api
def test_post_app_keys_route_with_data(client, mocker):
    expected_status = 201
    expected_m_length = 14
    expected_m_id = 5
    expected_m_name = "SOME_ROLE"
    expected_m_is_admin_role = False
    expected_m_priority = 125
    expected_m_login_lockout_policy = True
    expected_m_login_max_attempts = 5
    expected_m_login_timeframe = 450
    expected_m_login_ban_time = 1200
    expected_m_login_ban_by_ip = False
    expected_m_password_policy = True
    expected_m_password_reuse_history = 12
    expected_m_password_reset_days = 180
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}$")

    request_mock = mocker.patch('modules.roles.routes_admin.request')
    request_mock.json = {
        'name': expected_m_name,
        'is_admin_role': expected_m_is_admin_role,
        "priority": expected_m_priority,
        "login_lockout_policy": expected_m_login_lockout_policy,
        "login_max_attempts": expected_m_login_max_attempts,
        "login_timeframe": expected_m_login_timeframe,
        "login_ban_time": expected_m_login_ban_time,
        "login_ban_by_ip": expected_m_login_ban_by_ip,
        "password_policy": expected_m_password_policy,
        "password_reuse_history": expected_m_password_reuse_history,
        "password_reset_days": expected_m_password_reset_days
    }

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.post(
        "/roles?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert 'role' in response.json
    assert len(response.json['role']) == expected_m_length
    assert response.json['role']['id'] == expected_m_id
    assert response.json['role']['name'] == expected_m_name
    assert response.json['role']['is_admin_role'] == expected_m_is_admin_role
    assert response.json['role']['priority'] == expected_m_priority
    assert response.json['role']['login_lockout_policy'] == \
        expected_m_login_lockout_policy
    assert response.json['role']['login_max_attempts'] == \
        expected_m_login_max_attempts
    assert response.json['role']['login_timeframe'] == \
        expected_m_login_timeframe
    assert response.json['role']['login_ban_time'] == \
        expected_m_login_ban_time
    assert response.json['role']['login_ban_by_ip'] == \
        expected_m_login_ban_by_ip
    assert response.json['role']['password_policy'] == \
        expected_m_password_policy
    assert response.json['role']['password_reuse_history'] == \
        expected_m_password_reuse_history
    assert response.json['role']['password_reset_days'] == \
        expected_m_password_reset_days
    assert bool(re_datetime.match(response.json['role']['created_at']))
    assert bool(re_datetime.match(response.json['role']['updated_at']))


@pytest.mark.integration
@pytest.mark.admin_api
def test_put_role_route_with_data(client, mocker):
    expected_status = 200
    expected_m_length = 14
    expected_m_id = 1
    expected_m_name = "USER_A"
    expected_m_is_admin_role = True
    expected_m_priority = 101
    expected_m_login_lockout_policy = True
    expected_m_login_max_attempts = 11
    expected_m_login_timeframe = 601
    expected_m_login_ban_time = 1801
    expected_m_login_ban_by_ip = False
    expected_m_password_policy = True
    expected_m_password_reuse_history = 11
    expected_m_password_reset_days = 366
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}$")

    request_mock = mocker.patch('modules.roles.routes_admin.request')
    request_mock.json = {
        'name': expected_m_name,
        'is_admin_role': expected_m_is_admin_role,
        "priority": expected_m_priority,
        "login_lockout_policy": expected_m_login_lockout_policy,
        "login_max_attempts": expected_m_login_max_attempts,
        "login_timeframe": expected_m_login_timeframe,
        "login_ban_time": expected_m_login_ban_time,
        "login_ban_by_ip": expected_m_login_ban_by_ip,
        "password_policy": expected_m_password_policy,
        "password_reuse_history": expected_m_password_reuse_history,
        "password_reset_days": expected_m_password_reset_days
    }

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.put(
        "/role/{}?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW".format(
            expected_m_id), headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert 'role' in response.json
    assert len(response.json['role']) == expected_m_length
    assert response.json['role']['id'] == expected_m_id
    assert response.json['role']['name'] == expected_m_name
    assert response.json['role']['is_admin_role'] == expected_m_is_admin_role
    assert response.json['role']['priority'] == expected_m_priority
    assert response.json['role']['login_lockout_policy'] == \
        expected_m_login_lockout_policy
    assert response.json['role']['login_max_attempts'] == \
        expected_m_login_max_attempts
    assert response.json['role']['login_timeframe'] == \
        expected_m_login_timeframe
    assert response.json['role']['login_ban_time'] == \
        expected_m_login_ban_time
    assert response.json['role']['login_ban_by_ip'] == \
        expected_m_login_ban_by_ip
    assert response.json['role']['password_policy'] == \
        expected_m_password_policy
    assert response.json['role']['password_reuse_history'] == \
        expected_m_password_reuse_history
    assert response.json['role']['password_reset_days'] == \
        expected_m_password_reset_days
    assert bool(re_datetime.match(response.json['role']['created_at']))
    assert bool(re_datetime.match(response.json['role']['updated_at']))


@pytest.mark.integration
@pytest.mark.admin_api
def test_delete_role_1_route_with_data(client):
    expected_status = 204
    expected_json = None

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.delete(
        "/role/4?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json
