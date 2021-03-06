from copy import copy
import re
import base64

import pytest
from werkzeug.exceptions import NotFound, Unauthorized
from sqlalchemy.orm.exc import NoResultFound

from fixtures import Fixtures
from app import create_app
from config import Config
from modules.users.routes_admin import get_users, post_user, get_user, \
    put_user, delete_user
from modules.administrators.model import Administrator
from modules.users.model import User
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
def test_get_users(app, mocker):
    expected_status = 200
    expected_length = 2
    expected_json = {
        'created_at': None,
        'email': None,
        'id': None,
        'is_verified': None,
        'password_changed_at': None,
        'profile': None,
        'roles': [],
        'status': None,
        'status_changed_at': None,
        'terms_of_services': [],
        'uri': None,
        'updated_at': None,
        'username': None
    }
    expected_limit = 10
    expected_page = 1
    expected_total = 2

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [User()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    result = get_users()

    assert result[1] == expected_status
    assert len(result[0].json['users']) == expected_length
    assert result[0].json['users'][0] == expected_json
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_users_limit_10_page_2_of_3(app, mocker):
    expected_status = 200
    expected_length = 10
    expected_json = {
        'created_at': None,
        'email': None,
        'id': None,
        'is_verified': None,
        'password_changed_at': None,
        'profile': None,
        'roles': [],
        'status': None,
        'status_changed_at': None,
        'terms_of_services': [],
        'uri': None,
        'updated_at': None,
        'username': None
    }
    expected_limit = 10
    expected_page = 2
    expected_total = 25
    expected_previous_uri = 'http://localhost/users/1/10'
    expected_next_uri = 'http://localhost/users/3/10'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [User()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    result = get_users(expected_page, expected_limit)

    assert result[1] == expected_status
    assert len(result[0].json['users']) == expected_length
    assert result[0].json['users'][0] == expected_json
    assert result[0].json['previous_uri'] == expected_previous_uri
    assert result[0].json['next_uri'] == expected_next_uri
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_users_empty(app, mocker):
    expected_status = 204
    expected_content = ''

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
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

    result = get_users(5, 10)

    assert result[1] == expected_status
    assert result[0] == expected_content


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_users_by_role(app, mocker):
    expected_status = 200
    expected_length = 5
    expected_json = {
        'created_at': None,
        'email': None,
        'id': None,
        'is_verified': None,
        'password_changed_at': None,
        'profile': None,
        'roles': [],
        'status': None,
        'status_changed_at': None,
        'terms_of_services': [],
        'uri': None,
        'updated_at': None,
        'username': None
    }
    expected_limit = 5
    expected_page = 2
    expected_total = 14
    expected_previous_uri = 'http://localhost/users/1/5?role=1'
    expected_next_uri = 'http://localhost/users/3/5?role=1'

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.args = {'role': '1'}

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .filter.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [User()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .filter.return_value \
        .count.return_value = expected_total

    result = get_users(expected_page, expected_limit)

    assert result[1] == expected_status
    assert len(result[0].json['users']) == expected_length
    assert result[0].json['users'][0] == expected_json
    assert result[0].json['previous_uri'] == expected_previous_uri
    assert result[0].json['next_uri'] == expected_next_uri
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_users_route(app, mocker, client):
    expected_status = 200
    expected_length = 10
    expected_limit = 10
    expected_page = 1
    expected_total = 15
    expected_next_uri = 'http://localhost/users/2/10'

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

    db_mock = mocker.patch('modules.administrators.authentication.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [User()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    # mock user login
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get("/users?app_key=123",
                          headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert len(response.json['users']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_users_limit_5_page_2_of_3_route(app, mocker, client):
    expected_status = 200
    expected_length = 5
    expected_limit = 5
    expected_page = 2
    expected_total = 12
    expected_next_uri = 'http://localhost/users/3/5'
    expected_previous_uri = 'http://localhost/users/1/5'

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
        .__iter__.return_value = [User()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    # mock user login
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get(
        "/users/{}/{}?app_key=123".format(expected_page, expected_limit),
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert len(response.json['users']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri
    assert response.json['previous_uri'] == expected_previous_uri


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_users_empty_route(app, mocker, client):
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

    response = client.get("/users/3?app_key=123",
                          headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_users_route_no_app_key(app, client):
    expected_status = 401

    response = client.get("/users")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_users_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.get("/users?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_users_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.get("/users?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_user_ok(app, mocker):
    expected_status = 200
    expected_json = {
        'created_at': None,
        'email': None,
        'id': None,
        'is_verified': None,
        'password_changed_at': None,
        'profile': None,
        'roles': [],
        'status': None,
        'status_changed_at': None,
        'terms_of_services': [],
        'uri': None,
        'updated_at': None,
        'username': None
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = User()

    result = get_user(1)

    assert result[1] == expected_status
    assert result[0].json['user'] == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_user_not_found(app, mocker):
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = None

    try:
        get_user(250)
        assert False
    except NotFound:
        assert True


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_user_route_ok(app, mocker, client):
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
        .get.return_value = User()

    # mock user login
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get("/user/1?app_key=123",
                          headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert 'user' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_user_route_no_app_key(app, client):
    expected_status = 401

    response = client.get("/user/1")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_user_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.get("/user/1?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_user_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.get("/user/1?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_user_ok(app, mocker):
    expected_status = 201
    expected_m_length = 13
    expected_m_email = 'user9@test.com'
    expected_m_id = None
    expected_m_is_verified = False
    expected_m_username = 'user9'
    expected_m_role_id = 1
    expected_m_roles = [{'id': expected_m_role_id, 'name': 'USER'}]
    expected_m_terms_of_services = []
    expected_m_profile = None
    expected_m_uri = None
    expected_m_status = User.STATUS_ENABLED
    expected_m_created_at = None
    expected_m_updated_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {
        'email': expected_m_email,
        'is_verified': expected_m_is_verified,
        'roles': [expected_m_role_id],
        'status': expected_m_status,
        'username': expected_m_username,
        'password': 'user9Pass'
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock exists() validation
    role_1 = Role()
    role_1.id = 1
    role_1.name = 'USER'
    query_mock.return_value \
        .get.return_value = role_1

    db_mock = mocker.patch('modules.users.routes_admin.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    result = post_user()

    assert result[1] == expected_status
    assert 'user' in result[0].json
    assert len(result[0].json['user']) == expected_m_length
    assert result[0].json['user']['id'] == expected_m_id
    assert result[0].json['user']['username'] == expected_m_username
    assert result[0].json['user']['email'] == expected_m_email
    assert result[0].json['user']['is_verified'] == expected_m_is_verified
    assert result[0].json['user']['roles'] == expected_m_roles
    assert result[0].json['user']['terms_of_services'] == \
        expected_m_terms_of_services
    assert result[0].json['user']['profile'] == expected_m_profile
    assert result[0].json['user']['uri'] == expected_m_uri
    assert result[0].json['user']['status'] == expected_m_status
    assert bool(re_datetime.match(
        result[0].json['user']['password_changed_at']))
    assert bool(re_datetime.match(result[0].json['user']['status_changed_at']))
    assert result[0].json['user']['created_at'] == expected_m_created_at
    assert result[0].json['user']['updated_at'] == expected_m_updated_at


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_user_with_profile_ok(app, mocker):
    expected_status = 201
    expected_m_length = 13
    expected_m_email = 'user9@test.com'
    expected_m_id = None
    expected_m_is_verified = False
    expected_m_username = 'user9'
    expected_m_role_id = 1
    expected_m_roles = [{'id': expected_m_role_id, 'name': 'USER'}]
    expected_m_terms_of_services = []
    expected_m_profile = {
        'first_name': "Service",
        'joined_at': "2019-02-04T00:00:00+0000",
        'last_name': "Account",
    }
    expected_m_uri = None
    expected_m_status = User.STATUS_ENABLED
    expected_m_created_at = None
    expected_m_updated_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {
        'email': expected_m_email,
        'is_verified': expected_m_is_verified,
        'profile': expected_m_profile,
        'roles': [expected_m_role_id],
        'status': expected_m_status,
        'username': expected_m_username,
        'password': 'user9Pass'
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock exists() validation
    role_1 = Role()
    role_1.id = 1
    role_1.name = 'USER'
    query_mock.return_value \
        .get.return_value = role_1

    db_mock = mocker.patch('modules.users.routes_admin.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    result = post_user()

    assert result[1] == expected_status
    assert 'user' in result[0].json
    assert len(result[0].json['user']) == expected_m_length
    assert result[0].json['user']['id'] == expected_m_id
    assert result[0].json['user']['username'] == expected_m_username
    assert result[0].json['user']['email'] == expected_m_email
    assert result[0].json['user']['is_verified'] == expected_m_is_verified
    assert result[0].json['user']['roles'] == expected_m_roles
    assert result[0].json['user']['terms_of_services'] == \
        expected_m_terms_of_services
    assert result[0].json['user']['profile'] == expected_m_profile
    assert result[0].json['user']['uri'] == expected_m_uri
    assert result[0].json['user']['status'] == expected_m_status
    assert bool(re_datetime.match(
        result[0].json['user']['password_changed_at']))
    assert bool(re_datetime.match(result[0].json['user']['status_changed_at']))
    assert result[0].json['user']['created_at'] == expected_m_created_at
    assert result[0].json['user']['updated_at'] == expected_m_updated_at


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_user_required_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'email': ['Missing data for required field.'],
            'is_verified': ['Missing data for required field.'],
            'password': ['Missing data for required field.'],
            'roles': ['Missing data for required field.'],
            'status': ['Missing data for required field.'],
            'username': ['Missing data for required field.']
        }
    }

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {'foo': "bar"}

    result = post_user()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_user_unique_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'username': ['Value must be unique.'],
        'email': ['Value must be unique.']}}

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {
        'email': 'user1@test.com',
        'is_verified': False,
        'roles': [1],
        'status': User.STATUS_ENABLED,
        'username': 'user1',
        'password': 'user9Pass'
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = User()

    # mock exists() validation
    role_1 = Role()
    role_1.id = 1
    role_1.name = 'USER'
    query_mock.return_value \
        .get.return_value = role_1

    result = post_user()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_user_role_exists_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'roles': ['Invalid value.']}}

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {
        'email': 'user9@test.com',
        'is_verified': False,
        'roles': [250],
        'status': User.STATUS_ENABLED,
        'username': 'user9',
        'password': 'user9Pass'
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock exists() validation
    query_mock.return_value \
        .get.return_value = None

    result = post_user()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_user_password_complexity_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'password': ['Please choose a more complex password.']}}

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {
        'email': 'user9@test.com',
        'is_verified': False,
        'roles': [1],
        'status': User.STATUS_ENABLED,
        'username': 'user9',
        'password': 'password'
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock exists() validation
    role_1 = Role()
    role_1.id = 1
    role_1.name = 'USER'
    query_mock.return_value \
        .get.return_value = role_1

    result = post_user()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_user_unique_and_is_verified_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'email': ['Value must be unique.'],
        'is_verified': ['Missing data for required field.'],
        'username': ['Value must be unique.'],
    }}

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {
        'email': 'user1@test.com',
        'roles': [1],
        'status': User.STATUS_ENABLED,
        'username': 'user1',
        'password': 'user9Pass'
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = User()

    # mock exists() validation
    role_1 = Role()
    role_1.id = 1
    role_1.name = 'USER'
    query_mock.return_value \
        .get.return_value = role_1

    result = post_user()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_user_username_numeric_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'username': ['Value must not be a number.']}}

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {
        'email': 'user9@test.com',
        'is_verified': False,
        'roles': [250],
        'status': User.STATUS_ENABLED,
        'username': '1234',
        'password': 'user9Pass'
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock exists() validation
    role_1 = Role()
    role_1.id = 1
    role_1.name = 'USER'
    query_mock.return_value \
        .get.return_value = role_1

    result = post_user()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_user_username_character_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'username': ['Value must contain only alphanumeric characters and the underscore.']
    }}

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {
        'email': 'user9@test.com',
        'is_verified': False,
        'roles': [1],
        'status': User.STATUS_ENABLED,
        'username': 'user 9',
        'password': 'user9Pass'
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock exists() validation
    role_1 = Role()
    role_1.id = 1
    role_1.name = 'USER'
    query_mock.return_value \
        .get.return_value = role_1

    result = post_user()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_user_min_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'username': ['Value must be between 2 and 40 characters long.'],
    }}

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {
        'email': 'user9@test.com',
        'is_verified': False,
        'roles': [1],
        'status': User.STATUS_ENABLED,
        'username': 'u',
        'password': 'user9Pass'
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock exists() validation
    role_1 = Role()
    role_1.id = 1
    role_1.name = 'USER'
    query_mock.return_value \
        .get.return_value = role_1

    result = post_user()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_user_max_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'username': ['Value must be between 2 and 40 characters long.'],
    }}

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {
        'email': 'user9@test.com',
        'is_verified': False,
        'roles': [1],
        'status': User.STATUS_ENABLED,
        'username': '39Pz8cc5JeT3VdQHDCNn3L5NJKySHKrXXBwpqL5Ds',
        'password': 'user9Pass'
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock exists() validation
    role_1 = Role()
    role_1.id = 1
    role_1.name = 'USER'
    query_mock.return_value \
        .get.return_value = role_1

    result = post_user()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_user_empty_roles_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'roles': ['Missing data for required field.']
    }}

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {
        'email': 'user9@test.com',
        'is_verified': False,
        'roles': [],
        'status': User.STATUS_ENABLED,
        'username': 'user9',
        'password': 'user9Pass'
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = post_user()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_user_type_fail(app, mocker):
    expected_status = 400
    expected_json = {
        "error": {
            'email': ["Not a valid email address."],
            'is_verified': ["Not a valid boolean."],
            'password': ["Not a valid string."],
            'roles': ['Missing data for required field.'],
            'status': ["Not a valid integer."],
            'username': ["Not a valid string."]
        }
    }

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {
        'email': 123,
        'is_verified': "bad",
        'status': "bad",
        'username': 123,
        'password': 123
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = post_user()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_user_route_ok(app, mocker, client):
    expected_status = 201
    expected_m_length = 13
    expected_m_email = 'user9@test.com'
    expected_m_id = None
    expected_m_is_verified = False
    expected_m_username = 'user9'
    expected_m_role_id = 1
    expected_m_roles = [{'id': expected_m_role_id, 'name': 'USER'}]
    expected_m_terms_of_services = []
    expected_m_profile = None
    expected_m_uri = None
    expected_m_status = User.STATUS_ENABLED
    expected_m_created_at = None
    expected_m_updated_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    data = {
        'email': expected_m_email,
        'is_verified': expected_m_is_verified,
        'roles': [expected_m_role_id],
        'status': expected_m_status,
        'username': expected_m_username,
        'password': 'user9Pass'
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

    # mock user login unique(), unique_email() validation
    query_mock.return_value \
        .filter.return_value \
        .first.side_effect = [admin1, None, None]

    auth_db_mock = mocker.patch('modules.administrators.authentication.db')
    auth_db_mock.add.return_value = None
    auth_db_mock.commit.return_value = None

    # mock exists() validation
    role_1 = Role()
    role_1.id = 1
    role_1.name = 'USER'
    query_mock.return_value \
        .get.return_value = role_1

    db_mock = mocker.patch('modules.users.routes_admin.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    # mock user login
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.post(
        "/users?app_key=123",
        json=data,
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert 'user' in response.json
    assert len(response.json['user']) == expected_m_length
    assert response.json['user']['id'] == expected_m_id
    assert response.json['user']['username'] == expected_m_username
    assert response.json['user']['email'] == expected_m_email
    assert response.json['user']['is_verified'] == expected_m_is_verified
    assert response.json['user']['roles'] == expected_m_roles
    assert response.json['user']['terms_of_services'] == \
        expected_m_terms_of_services
    assert response.json['user']['uri'] == expected_m_uri
    assert response.json['user']['profile'] == expected_m_profile
    assert response.json['user']['status'] == expected_m_status
    assert bool(re_datetime.match(
        response.json['user']['password_changed_at']))
    assert bool(re_datetime.match(response.json['user']['status_changed_at']))
    assert response.json['user']['created_at'] == expected_m_created_at
    assert response.json['user']['updated_at'] == expected_m_updated_at


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_users_route_no_app_key(app, client):
    expected_status = 401

    response = client.post("/users")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_users_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.post("/users?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_users_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.post("/users?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_user_ok(app, mocker):
    expected_status = 200
    expected_m_length = 13
    expected_m_email = 'user2a@test.com'
    expected_m_id = 2
    expected_m_is_verified = False
    expected_m_username = 'user2a'
    expected_m_role_id = 3
    expected_m_roles = [{'id': expected_m_role_id, 'name': 'SERVICE'}]
    expected_m_terms_of_services = []
    expected_m_profile = None
    expected_m_uri = 'http://localhost/user/2'
    expected_m_status = User.STATUS_DISABLED
    expected_m_created_at = None
    expected_m_updated_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {
        'email': expected_m_email,
        'is_verified': expected_m_is_verified,
        'roles': [expected_m_role_id],
        'status': expected_m_status,
        'username': expected_m_username,
        'password': 'user9Pass2'
    }

    user_2 = User()
    user_2.id = expected_m_id

    role_3 = Role()
    role_3.id = 3
    role_3.name = 'SERVICE'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [user_2, role_3]

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    db_mock = mocker.patch('modules.users.routes_admin.db')
    db_mock.commit.return_value = None

    result = put_user(expected_m_id)

    assert result[1] == expected_status
    assert 'user' in result[0].json
    assert len(result[0].json['user']) == expected_m_length
    assert result[0].json['user']['id'] == expected_m_id
    assert result[0].json['user']['username'] == expected_m_username
    assert result[0].json['user']['email'] == expected_m_email
    assert result[0].json['user']['is_verified'] == expected_m_is_verified
    assert result[0].json['user']['roles'] == expected_m_roles
    assert result[0].json['user']['terms_of_services'] == \
        expected_m_terms_of_services
    assert result[0].json['user']['uri'] == expected_m_uri
    assert result[0].json['user']['profile'] == expected_m_profile
    assert result[0].json['user']['status'] == expected_m_status
    assert bool(re_datetime.match(
        result[0].json['user']['password_changed_at']))
    assert bool(re_datetime.match(result[0].json['user']['status_changed_at']))
    assert result[0].json['user']['created_at'] == expected_m_created_at
    assert result[0].json['user']['updated_at'] == expected_m_updated_at


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_user_with_profile_ok(app, mocker):
    expected_status = 200
    expected_m_length = 13
    expected_m_email = 'user2a@test.com'
    expected_m_id = 2
    expected_m_is_verified = False
    expected_m_username = 'user2a'
    expected_m_role_id = 3
    expected_m_roles = [{'id': expected_m_role_id, 'name': 'SERVICE'}]
    expected_m_terms_of_services = []
    expected_m_profile = {
        'first_name': "LynneA",
        'joined_at': "2019-01-15T00:00:00+0000",
        'last_name': "HarfordA",
    }
    expected_m_uri = 'http://localhost/user/2'
    expected_m_status = User.STATUS_DISABLED
    expected_m_created_at = None
    expected_m_updated_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {
        'email': expected_m_email,
        'is_verified': expected_m_is_verified,
        'profile': expected_m_profile,
        'roles': [expected_m_role_id],
        'status': expected_m_status,
        'username': expected_m_username,
        'password': 'user9Pass2'
    }

    user_2 = User()
    user_2.id = expected_m_id

    role_3 = Role()
    role_3.id = 3
    role_3.name = 'SERVICE'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [user_2, role_3]

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    db_mock = mocker.patch('modules.users.routes_admin.db')
    db_mock.commit.return_value = None

    result = put_user(expected_m_id)

    print(result[0].json)

    assert result[1] == expected_status
    assert 'user' in result[0].json
    assert len(result[0].json['user']) == expected_m_length
    assert result[0].json['user']['id'] == expected_m_id
    assert result[0].json['user']['username'] == expected_m_username
    assert result[0].json['user']['email'] == expected_m_email
    assert result[0].json['user']['is_verified'] == expected_m_is_verified
    assert result[0].json['user']['roles'] == expected_m_roles
    assert result[0].json['user']['terms_of_services'] == \
        expected_m_terms_of_services
    assert result[0].json['user']['uri'] == expected_m_uri
    assert result[0].json['user']['profile'] == expected_m_profile
    assert result[0].json['user']['status'] == expected_m_status
    assert bool(re_datetime.match(
        result[0].json['user']['password_changed_at']))
    assert bool(re_datetime.match(result[0].json['user']['status_changed_at']))
    assert result[0].json['user']['created_at'] == expected_m_created_at
    assert result[0].json['user']['updated_at'] == expected_m_updated_at


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_user_no_password_ok(app, mocker):
    expected_status = 200
    expected_m_length = 13
    expected_m_email = 'user2a@test.com'
    expected_m_id = 2
    expected_m_is_verified = False
    expected_m_username = 'user2a'
    expected_m_role_id = 3
    expected_m_roles = [{'id': expected_m_role_id, 'name': 'SERVICE'}]
    expected_m_terms_of_services = []
    expected_m_profile = None
    expected_m_uri = 'http://localhost/user/2'
    expected_m_status = User.STATUS_DISABLED
    expected_m_password_changed_at = None
    expected_m_created_at = None
    expected_m_updated_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {
        'email': expected_m_email,
        'is_verified': expected_m_is_verified,
        'roles': [expected_m_role_id],
        'status': expected_m_status,
        'username': expected_m_username
    }

    user_2 = User()
    user_2.id = expected_m_id

    role_3 = Role()
    role_3.id = 3
    role_3.name = 'SERVICE'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [user_2, role_3]

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    db_mock = mocker.patch('modules.users.routes_admin.db')
    db_mock.commit.return_value = None

    result = put_user(expected_m_id)

    assert result[1] == expected_status
    assert 'user' in result[0].json
    assert len(result[0].json['user']) == expected_m_length
    assert result[0].json['user']['id'] == expected_m_id
    assert result[0].json['user']['username'] == expected_m_username
    assert result[0].json['user']['email'] == expected_m_email
    assert result[0].json['user']['is_verified'] == expected_m_is_verified
    assert result[0].json['user']['roles'] == expected_m_roles
    assert result[0].json['user']['terms_of_services'] == \
        expected_m_terms_of_services
    assert result[0].json['user']['profile'] == expected_m_profile
    assert result[0].json['user']['uri'] == expected_m_uri
    assert result[0].json['user']['status'] == expected_m_status
    assert result[0].json['user']['password_changed_at'] == \
        expected_m_password_changed_at
    assert bool(re_datetime.match(result[0].json['user']['status_changed_at']))
    assert result[0].json['user']['created_at'] == expected_m_created_at
    assert result[0].json['user']['updated_at'] == expected_m_updated_at


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_user_required_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'email': ['Missing data for required field.'],
            'is_verified': ['Missing data for required field.'],
            'roles': ['Missing data for required field.'],
            'status': ['Missing data for required field.'],
            'username': ['Missing data for required field.']
        }
    }

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {'foo': "bar"}

    user_2 = User()
    user_2.id = 2

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.return_value = user_2

    result = put_user(2)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_user_unique_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'username': ['Value must be unique.'],
        'email': ['Value must be unique.']}}

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {
        'email': 'user1@test.com',
        'is_verified': False,
        'roles': [3],
        'status': User.STATUS_DISABLED,
        'username': 'user1',
        'password': 'user2PassA'
    }

    user_2 = User()
    user_2.id = 2

    role_3 = Role()
    role_3.id = 3
    role_3.name = 'SERVICE'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [user_2, role_3]

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = User()

    result = put_user(2)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_user_role_exists_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'roles': ['Invalid value.']}}

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {
        'email': 'user2a@test.com',
        'is_verified': False,
        'roles': [250],
        'status': User.STATUS_DISABLED,
        'username': 'user2a',
        'password': 'user2PassA'
    }

    user_2 = User()
    user_2.id = 2

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [user_2, None]

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_user(2)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_user_password_complexity_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'password': ['Please choose a more complex password.']}}

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {
        'email': 'user2a@test.com',
        'is_verified': False,
        'roles': [3],
        'status': User.STATUS_DISABLED,
        'username': 'user2a',
        'password': 'password'
    }

    user_2 = User()
    user_2.id = 2

    role_3 = Role()
    role_3.id = 3
    role_3.name = 'SERVICE'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [user_2, role_3]

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_user(2)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_user_unique_and_no_is_verified_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'email': ['Value must be unique.'],
        'is_verified': ['Missing data for required field.'],
        'username': ['Value must be unique.'],
    }}

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {
        'email': 'user1@test.com',
        'roles': [3],
        'status': User.STATUS_DISABLED,
        'username': 'user1',
        'password': 'user2PassA'
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    user_2 = User()
    user_2.id = 2

    role_3 = Role()
    role_3.id = 3
    role_3.name = 'SERVICE'

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [user_2, role_3]

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = User()

    result = put_user(2)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_user_username_numeric_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'username': ['Value must not be a number.']}}

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {
        'email': 'user2a@test.com',
        'is_verified': False,
        'roles': [3],
        'status': User.STATUS_DISABLED,
        'username': '1234',
        'password': 'user2PassA'
    }

    user_2 = User()
    user_2.id = 2

    role_3 = Role()
    role_3.id = 3
    role_3.name = 'SERVICE'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [user_2, role_3]

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_user(2)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_user_username_character_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'username': ['Value must contain only alphanumeric characters and the underscore.']
    }}

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {
        'email': 'user2a@test.com',
        'is_verified': False,
        'roles': [3],
        'status': User.STATUS_DISABLED,
        'username': 'user 2',
        'password': 'user2PassA'
    }

    user_2 = User()
    user_2.id = 2

    role_3 = Role()
    role_3.id = 3
    role_3.name = 'SERVICE'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [user_2, role_3]

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_user(2)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_user_min_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'username': ['Value must be between 2 and 40 characters long.'],
    }}

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {
        'email': 'user2a@test.com',
        'is_verified': False,
        'roles': [3],
        'status': User.STATUS_DISABLED,
        'username': 'u',
        'password': 'user2PassA'
    }

    user_2 = User()
    user_2.id = 2

    role_3 = Role()
    role_3.id = 3
    role_3.name = 'SERVICE'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [user_2, role_3]

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_user(2)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_user_max_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'username': ['Value must be between 2 and 40 characters long.'],
    }}

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {
        'email': 'user2a@test.com',
        'is_verified': False,
        'roles': [3],
        'status': User.STATUS_DISABLED,
        'username': 'u6PQS4vuu3FrghDqkvNTEgSh4BjuBsXjXGjGPW2y9',
        'password': 'user2PassA'
    }

    user_2 = User()
    user_2.id = 2

    role_3 = Role()
    role_3.id = 3
    role_3.name = 'SERVICE'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [user_2, role_3]

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_user(2)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_user_empty_roles_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'roles': ['Missing data for required field.']
    }}

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {
        'email': 'user2a@test.com',
        'is_verified': False,
        'roles': [],
        'status': User.STATUS_DISABLED,
        'username': 'user2a',
        'password': 'user2PassA'
    }

    user_2 = User()
    user_2.id = 2

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query
    query_mock.return_value \
        .get.return_value = user_2

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_user(2)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_user_type_fail(app, mocker):
    expected_status = 400
    expected_json = {
        "error": {
            'email': ["Not a valid email address."],
            'is_verified': ["Not a valid boolean."],
            'password': ["Not a valid string."],
            'roles': ['Missing data for required field.'],
            'status': ["Not a valid integer."],
            'username': ["Not a valid string."]
        }
    }

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {
        'email': 123,
        'is_verified': "bad",
        'status': "bad",
        'username': 123,
        'password': 123
    }

    user_2 = User()
    user_2.id = 2

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query
    query_mock.return_value \
        .get.return_value = user_2

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_user(2)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_user_route_ok(app, mocker, client):
    expected_status = 200
    expected_m_length = 13
    expected_m_email = 'user2a@test.com'
    expected_m_id = 2
    expected_m_is_verified = False
    expected_m_username = 'user2a'
    expected_m_role_id = 3
    expected_m_roles = [{'id': expected_m_role_id, 'name': 'SERVICE'}]
    expected_m_terms_of_services = []
    expected_m_profile = None
    expected_m_uri = 'http://localhost/user/2'
    expected_m_status = User.STATUS_DISABLED
    expected_m_created_at = None
    expected_m_updated_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    data = {
        'email': expected_m_email,
        'is_verified': expected_m_is_verified,
        'roles': [expected_m_role_id],
        'status': expected_m_status,
        'username': expected_m_username,
        'password': 'user2Pass2'
    }

    user_2 = User()
    user_2.id = 2

    role_3 = Role()
    role_3.id = 3
    role_3.name = 'SERVICE'

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

    # mock user login, unique(), unique_email() validation
    query_mock.return_value \
        .filter.return_value \
        .first.side_effect = [admin1, None, None]

    auth_db_mock = mocker.patch('modules.administrators.authentication.db')
    auth_db_mock.add.return_value = None
    auth_db_mock.commit.return_value = None

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [user_2, role_3]

    db_mock = mocker.patch('modules.users.routes_admin.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    # mock user login
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.put(
        "/user/{}?app_key=123".format(expected_m_id),
        json=data,
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert 'user' in response.json
    assert len(response.json['user']) == expected_m_length
    assert response.json['user']['id'] == expected_m_id
    assert response.json['user']['username'] == expected_m_username
    assert response.json['user']['email'] == expected_m_email
    assert response.json['user']['is_verified'] == expected_m_is_verified
    assert response.json['user']['roles'] == expected_m_roles
    assert response.json['user']['terms_of_services'] == \
        expected_m_terms_of_services
    assert response.json['user']['profile'] == expected_m_profile
    assert response.json['user']['uri'] == expected_m_uri
    assert response.json['user']['status'] == expected_m_status
    assert bool(re_datetime.match(
        response.json['user']['password_changed_at']))
    assert bool(re_datetime.match(response.json['user']['status_changed_at']))
    assert response.json['user']['created_at'] == expected_m_created_at
    assert response.json['user']['updated_at'] == expected_m_updated_at


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_user_route_no_app_key(app, client):
    expected_status = 401

    response = client.put("/user/1")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_user_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.put("/user/1?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_user_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.put("/user/1?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_delete_user_ok(app, mocker):
    expected_status = 204
    expected_content = ''

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = User()

    db_mock = mocker.patch('modules.users.routes_admin.db')
    db_mock.commit.return_value = None

    result = delete_user(7)

    assert result[1] == expected_status
    assert result[0] == expected_content


@pytest.mark.unit
@pytest.mark.admin_api
def test_delete_user_fail(app, mocker):
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = None

    try:
        delete_user(250)
        assert False
    except NotFound:
        assert True


@pytest.mark.unit
@pytest.mark.admin_api
def test_delete_user_route_ok(app, mocker, client):
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
        .first.return_value = admin1

    auth_db_mock = mocker.patch('modules.administrators.authentication.db')
    auth_db_mock.add.return_value = None
    auth_db_mock.commit.return_value = None

    # mock resource query
    query_mock.return_value \
        .get.return_value = User()

    # mock db commit
    db_mock = mocker.patch('modules.users.routes_admin.db')
    db_mock.commit.return_value = None

    # mock user login
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.delete("/user/7?app_key=123",
                             headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_delete_user_route_no_app_key(app, client):
    expected_status = 401

    response = client.delete("/user/7")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_delete_user_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.delete("/user/7?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_delete_user_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.delete("/user/57?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


# INTEGRATION TESTS


@pytest.mark.integration
@pytest.mark.admin_api
def test_get_users_route_with_data(client):
    expected_status = 200
    expected_json = {
        "limit": 10,
        "page": 1,
        "total": 7,
        "users": [
            {
                "created_at": "2018-12-01T00:00:00+0000",
                "email": "user1@test.com",
                "id": 1,
                "is_verified": False,
                "password_changed_at": "2018-12-04T00:00:00+0000",
                "profile": {
                    "first_name": "Fiona",
                    "joined_at": "2018-12-03T00:00:00+0000",
                    "last_name": "Farnham"
                },
                "roles": [],
                "status": 1,
                "status_changed_at": "2018-12-03T00:00:00+0000",
                "terms_of_services": [
                    {
                        "accept_date": "2019-01-07T08:00:00+0000",
                        "ip_address": "1.1.1.1",
                        "terms_of_service": {
                            "id": 2,
                            "version": "1.1"
                        }
                    },
                    {
                        "accept_date": "2018-12-03T08:00:00+0000",
                        "ip_address": "1.1.1.1",
                        "terms_of_service": {
                            "id": 1,
                            "version": "1.0"
                        }
                }
                ],
                "updated_at": "2018-12-02T00:00:00+0000",
                "uri": "http://localhost/user/1",
                "username": "user1"
            },
            {
                "created_at": "2018-12-05T00:00:00+0000",
                "email": "user2@test.com",
                "id": 2,
                "is_verified": True,
                "password_changed_at": None,
                "profile": {
                    "first_name": "Lynne",
                    "joined_at": "2018-12-07T00:00:00+0000",
                    "last_name": "Harford"
                },
                "roles": [
                    {
                        "id": 1,
                        "name": "USER"
                    }
                ],
                "status": 1,
                "status_changed_at": "2018-12-07T00:00:00+0000",
                "terms_of_services": [
                    {
                        "accept_date": "2019-01-17T08:00:00+0000",
                        "ip_address": "1.1.1.2",
                        "terms_of_service": {
                            "id": 2,
                            "version": "1.1"
                        }
                    },
                    {
                        "accept_date": "2018-12-12T08:00:00+0000",
                        "ip_address": "1.1.1.2",
                        "terms_of_service": {
                            "id": 1,
                            "version": "1.0"
                        }
                    }
                ],
                "updated_at": "2018-12-06T00:00:00+0000",
                "uri": "http://localhost/user/2",
                "username": "user2"
            },
            {
                "created_at": "2018-12-10T00:00:00+0000",
                "email": "user3@test.com",
                "id": 3,
                "is_verified": True,
                "password_changed_at": "2018-12-13T00:00:00+0000",
                "profile": {
                    "first_name": "Duane",
                    "joined_at": "2018-12-12T00:00:00+0000",
                    "last_name": "Hargrave"
                },
                "roles": [
                    {
                        "id": 1,
                        "name": "USER"
                    }
                ],
                "status": 1,
                "status_changed_at": "2018-12-12T00:00:00+0000",
                "terms_of_services": [
                    {
                        "accept_date": "2019-02-05T08:00:00+0000",
                        "ip_address": "1.1.1.3",
                        "terms_of_service": {
                            "id": 2,
                            "version": "1.1"
                        }
                    }
                ],
                "updated_at": "2018-12-11T00:00:00+0000",
                "uri": "http://localhost/user/3",
                "username": "user3"
            },
            {
                "created_at": "2018-12-20T00:00:00+0000",
                "email": "user5@test.com",
                "id": 5,
                "is_verified": False,
                "password_changed_at": "2018-12-23T00:00:00+0000",
                "profile": {
                    "first_name": "Elroy",
                    "joined_at": "2018-12-22T00:00:00+0000",
                    "last_name": "Hunnicutt"
                },
                "roles": [
                    {
                        "id": 1,
                        "name": "USER"
                    }
                ],
                "status": 2,
                "status_changed_at": "2018-12-22T00:00:00+0000",
                "terms_of_services": [],
                "updated_at": "2018-12-21T00:00:00+0000",
                "uri": "http://localhost/user/5",
                "username": "user5"
            },
            {
                "created_at": "2018-12-25T00:00:00+0000",
                "email": "user6@test.com",
                "id": 6,
                "is_verified": True,
                "password_changed_at": "2018-12-28T00:00:00+0000",
                "profile": {
                    "first_name": "Alease",
                    "joined_at": "2018-12-27T00:00:00+0000",
                    "last_name": "Richards"
                },
                "roles": [
                    {
                        "id": 1,
                        "name": "USER"
                    }
                ],
                "status": 5,
                "status_changed_at": "2018-12-27T00:00:00+0000",
                "terms_of_services": [],
                "updated_at": "2018-12-26T00:00:00+0000",
                "uri": "http://localhost/user/6",
                "username": "user6"
            },
            {
                "created_at": "2019-01-05T00:00:00+0000",
                "email": "user8@test.com",
                "id": 8,
                "is_verified": False,
                "password_changed_at": "2019-01-08T00:00:00+0000",
                "profile": {
                    "first_name": "Luke",
                    "joined_at": "2019-01-07T00:00:00+0000",
                    "last_name": "Tennyson"
                },
                "roles": [
                    {
                        "id": 1,
                        "name": "USER"
                    }
                ],
                "status": 1,
                "status_changed_at": "2019-01-07T00:00:00+0000",
                "terms_of_services": [],
                "updated_at": "2019-01-06T00:00:00+0000",
                "uri": "http://localhost/user/8",
                "username": "user8"
            },
            {
                "created_at": "2019-01-10T00:00:00+0000",
                "email": "service1@test.com",
                "id": 9,
                "is_verified": False,
                "password_changed_at": "2019-01-13T00:00:00+0000",
                "profile": None,
                "roles": [
                    {
                        "id": 3,
                        "name": "SERVICE"
                    }
                ],
                "status": 1,
                "status_changed_at": "2019-01-12T00:00:00+0000",
                "terms_of_services": [],
                "updated_at": "2019-01-11T00:00:00+0000",
                "uri": "http://localhost/user/9",
                "username": "service1"
            }
        ]
    }

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get(
        "/users?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json['users'][0] == expected_json['users'][0]
    assert response.json['users'][2] == expected_json['users'][2]
    assert response.json['users'][3] == expected_json['users'][3]
    assert response.json['users'][4] == expected_json['users'][4]
    assert response.json['users'][5] == expected_json['users'][5]
    assert response.json['users'][6] == expected_json['users'][6]
    assert response.json['users'][1]['id'] == expected_json['users'][1]['id']


@pytest.mark.integration
@pytest.mark.admin_api
def test_get_user_3_route_with_data(client):
    expected_status = 200
    expected_json = {
        "user": {
            "created_at": "2018-12-10T00:00:00+0000",
            "email": "user3@test.com",
            "id": 3,
            "is_verified": True,
            "password_changed_at": "2018-12-13T00:00:00+0000",
            "profile": {
                "first_name": "Duane",
                "joined_at": "2018-12-12T00:00:00+0000",
                "last_name": "Hargrave"
            },
            "roles": [
                {
                    "id": 1,
                    "name": "USER"
                }
            ],
            "status": 1,
            "status_changed_at": "2018-12-12T00:00:00+0000",
            "terms_of_services": [
                {
                    "accept_date": "2019-02-05T08:00:00+0000",
                    "ip_address": "1.1.1.3",
                    "terms_of_service": {
                        "id": 2,
                        "version": "1.1"
                    }
                }
            ],
            "updated_at": "2018-12-11T00:00:00+0000",
            "uri": "http://localhost/user/3",
            "username": "user3"
        }
    }

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get(
        "/user/3?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.integration
@pytest.mark.admin_api
def test_post_users_route_with_data(client, mocker):
    expected_status = 201
    expected_m_length = 13
    expected_m_email = 'user9@test.com'
    expected_m_id = 10
    expected_m_is_verified = False
    expected_m_username = 'user9'
    expected_m_role_id = 1
    expected_m_roles = [{'id': expected_m_role_id, 'name': 'USER'}]
    expected_m_terms_of_services = []
    expected_m_profile = None
    expected_m_uri = 'http://localhost/user/10'
    expected_m_status = User.STATUS_ENABLED
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}$")

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {
        'email': expected_m_email,
        'is_verified': expected_m_is_verified,
        'roles': [expected_m_role_id],
        'status': expected_m_status,
        'username': expected_m_username,
        'password': 'user9Pass'
    }

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.post(
        "/users?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert 'user' in response.json
    assert len(response.json['user']) == expected_m_length
    assert response.json['user']['id'] == expected_m_id
    assert response.json['user']['username'] == expected_m_username
    assert response.json['user']['email'] == expected_m_email
    assert response.json['user']['is_verified'] == expected_m_is_verified
    assert response.json['user']['roles'] == expected_m_roles
    assert response.json['user']['terms_of_services'] == \
        expected_m_terms_of_services
    assert response.json['user']['profile'] == expected_m_profile
    assert response.json['user']['uri'] == expected_m_uri
    assert response.json['user']['status'] == expected_m_status
    assert bool(re_datetime.match(
        response.json['user']['password_changed_at']))
    assert bool(re_datetime.match(
        response.json['user']['status_changed_at']))
    assert bool(re_datetime.match(
        response.json['user']['created_at']))
    assert bool(re_datetime.match(
        response.json['user']['updated_at']))


@pytest.mark.integration
@pytest.mark.admin_api
def test_put_user_route_with_data(client, mocker):
    expected_status = 200
    expected_m_length = 13
    expected_m_email = 'user2a@test.com'
    expected_m_id = 2
    expected_m_is_verified = False
    expected_m_username = 'user2a'
    expected_m_role_id = 3
    expected_m_roles = [{'id': expected_m_role_id, 'name': 'SERVICE'}]
    expected_m_terms_of_services_length = 2
    expected_m_profile = {
        "first_name": "Lynne",
        "joined_at": "2018-12-07T00:00:00+0000",
        "last_name": "Harford"
    }
    expected_m_uri = 'http://localhost/user/2'
    expected_m_status = User.STATUS_DISABLED
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}$")

    request_mock = mocker.patch('modules.users.routes_admin.request')
    request_mock.json = {
        'email': expected_m_email,
        'is_verified': expected_m_is_verified,
        'roles': [expected_m_role_id],
        'status': expected_m_status,
        'username': expected_m_username,
        'password': 'user2Pass2'
    }

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.put(
        "/user/{}?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW".format(
            expected_m_id), headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert 'user' in response.json
    assert len(response.json['user']) == expected_m_length
    assert response.json['user']['id'] == expected_m_id
    assert response.json['user']['username'] == expected_m_username
    assert response.json['user']['email'] == expected_m_email
    assert response.json['user']['is_verified'] == expected_m_is_verified
    assert response.json['user']['roles'] == expected_m_roles
    assert len(response.json['user']['terms_of_services']) == \
        expected_m_terms_of_services_length
    assert response.json['user']['profile'] == expected_m_profile
    assert response.json['user']['uri'] == expected_m_uri
    assert response.json['user']['status'] == expected_m_status
    assert bool(re_datetime.match(
        response.json['user']['password_changed_at']))
    assert bool(re_datetime.match(
        response.json['user']['status_changed_at']))
    assert bool(re_datetime.match(
        response.json['user']['created_at']))
    assert bool(re_datetime.match(
        response.json['user']['updated_at']))


@pytest.mark.integration
@pytest.mark.admin_api
def test_delete_user_7_route_with_data(client):
    expected_status = 204
    expected_json = None

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.delete(
        "/user/7?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json
