from copy import copy
import re
import base64

import pytest
from werkzeug.exceptions import NotFound, Unauthorized
from sqlalchemy.orm.exc import NoResultFound

from fixtures import Fixtures
from app import create_app
from config import Config
from modules.user_account.routes_admin import get_account, put_account, \
    put_password
from modules.administrators.model import Administrator, \
    AdministratorPasswordHistory
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
def test_get_account_ok(app, mocker):
    expected_status = 200
    expected_json = {
        'email': None,
        'first_name': None,
        'id': None,
        'joined_at': None,
        'last_name': None,
        'password_changed_at': None,
        'uri': None,
        'username': None,
    }

    g_mock = mocker.patch('modules.user_account.routes_admin.g')
    g_mock.user = Administrator()

    result = get_account()

    assert result[1] == expected_status
    assert result[0].json['user_account'] == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_account_route_ok(app, mocker, client):
    expected_status = 200

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    g_mock = mocker.patch('modules.user_account.routes_admin.g')
    g_mock.user = Administrator()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.return_value = True

    response = client.get("/user_account?app_key=123")

    assert response.status_code == expected_status
    assert 'user_account' in  response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_account_route_no_app_key(app, client):
    expected_status = 401

    response = client.get("/user_account")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_account_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.get("/user_account?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_account_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.get("/user_account?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_account_profile_ok(app, mocker):
    expected_status = 200
    expected_m_length = 8
    expected_m_id = 1
    expected_m_username = "admin1a"
    expected_m_email = "admin1a@test.com"
    expected_m_first_name = "TommyA"
    expected_m_last_name = "LundA"
    expected_m_uri = "http://localhost/administrator/1"
    expected_m_password_changed_at = None
    expected_m_joined_at = None

    request_mock = mocker.patch('modules.user_account.routes_admin.request')
    request_mock.json = {
        'username': expected_m_username,
        'email': expected_m_email,
        'first_name': expected_m_first_name,
        'last_name': expected_m_last_name,
    }

    admin1 = Administrator()
    admin1.id = 1
    admin1.username = 'admin1'
    admin1.email = 'admin1@test.com'
    admin1.first_name = 'Tommy'
    admin1.last_name = 'Lund'

    g_mock = mocker.patch('modules.user_account.routes_admin.g')
    g_mock.user = admin1

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique_email() validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    db_mock = mocker.patch('modules.user_account.routes_admin.db')
    db_mock.commit.return_value = None

    result = put_account()

    assert result[1] == expected_status
    assert 'user_account' in result[0].json
    assert len(result[0].json['user_account']) == expected_m_length
    assert result[0].json['user_account']['id'] == expected_m_id
    assert result[0].json['user_account']['username'] == expected_m_username
    assert result[0].json['user_account']['email'] == expected_m_email
    assert result[0].json['user_account']['first_name'] == \
           expected_m_first_name
    assert result[0].json['user_account']['last_name'] == expected_m_last_name
    assert result[0].json['user_account']['uri'] == expected_m_uri
    assert result[0].json['user_account']['password_changed_at'] == \
           expected_m_password_changed_at
    assert result[0].json['user_account']['joined_at'] == expected_m_joined_at


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_account_required_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'username': ['Missing data for required field.'],
            'email': ['Missing data for required field.'],
            'first_name': ['Missing data for required field.'],
            'foo': ['Unknown field.'],
            'last_name': ['Missing data for required field.'],
        }
    }

    request_mock = mocker.patch('modules.user_account.routes_admin.request')
    request_mock.json = {'foo': "bar"}

    g_mock = mocker.patch('modules.user_account.routes_admin.g')
    g_mock.user = Administrator()

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique_email() validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_account()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_account_unique_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'username': ['Value must be unique.'],
        'email': ['Value must be unique.']}}

    request_mock = mocker.patch('modules.user_account.routes_admin.request')
    request_mock.json = {
        'username': 'admin2',
        'email': 'admin2@test.com',
        'first_name': "TommyA",
        'last_name': "LundA",
    }

    g_mock = mocker.patch('modules.user_account.routes_admin.g')
    g_mock.user = Administrator()

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique_email() validation
    query_mock.return_value \
        .filter.return_value \
        .first.side_effect = [Administrator(), Administrator()]

    result = put_account()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_account_username_numeric_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'username': ['Value must not be a number.']}}

    request_mock = mocker.patch('modules.user_account.routes_admin.request')
    request_mock.json = {
        'username': '1234',
        'email': 'admin1a@test.com',
        'first_name': "TommyA",
        'last_name': "LundA",
    }

    g_mock = mocker.patch('modules.user_account.routes_admin.g')
    g_mock.user = Administrator()

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique_email() validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_account()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_account_username_character_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'username': ['Value must contain only alphanumeric characters and the underscore.']}}

    request_mock = mocker.patch('modules.user_account.routes_admin.request')
    request_mock.json = {
        'username': 'admin 1',
        'email': 'admin1a@test.com',
        'first_name': "TommyA",
        'last_name': "LundA",
    }

    g_mock = mocker.patch('modules.user_account.routes_admin.g')
    g_mock.user = Administrator()

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique_email() validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_account()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_account_email_format_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'email': ['Not a valid email address.']}}

    request_mock = mocker.patch('modules.user_account.routes_admin.request')
    request_mock.json = {
        'username': 'admin1',
        'email': 'admin1atest.com',
        'first_name': "TommyA",
        'last_name': "LundA",
    }

    g_mock = mocker.patch('modules.user_account.routes_admin.g')
    g_mock.user = Administrator()

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique_email() validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_account()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_account_min_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'first_name': ['Value must be between 1 and 40 characters long.'],
        'last_name': ['Value must be between 2 and 40 characters long.'],
        'username': ['Value must be between 2 and 40 characters long.'],
    }}

    request_mock = mocker.patch('modules.user_account.routes_admin.request')
    request_mock.json = {
        'username': 'a',
        'email': 'admin1a@test.com',
        'first_name': "",
        'last_name': "L",
    }

    g_mock = mocker.patch('modules.user_account.routes_admin.g')
    g_mock.user = Administrator()

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique_email() validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_account()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_account_max_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'first_name': ['Value must be between 1 and 40 characters long.'],
        'last_name': ['Value must be between 2 and 40 characters long.'],
        'username': ['Value must be between 2 and 40 characters long.'],
    }}

    request_mock = mocker.patch('modules.user_account.routes_admin.request')
    request_mock.json = {
        'username': 'Dz6RD8Rh7fj5bsPXmJDKdAPFRfcHq7NeNtjyrM9Gb',
        'email': 'admin1a@test.com',
        'first_name': "VTThbgrzTU8tSsD3p85LDG9Efr3twA6NvqEUVrgeq",
        'last_name': "ZgtpaPWMnYYzfSvZwq9cFkMMazbVjcYbQeWQYAt4m",
    }

    g_mock = mocker.patch('modules.user_account.routes_admin.g')
    g_mock.user = Administrator()

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique_email() validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_account()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_account_type_fail(app, mocker):
    expected_status = 400
    expected_json = {
        "error": {
            'email': ["Not a valid email address."],
            'first_name': ["Not a valid string."],
            'last_name': ["Not a valid string."],
            'username': ["Not a valid string."],
        }
    }

    request_mock = mocker.patch('modules.user_account.routes_admin.request')
    request_mock.json = {
        'username': 123,
        'email': 123,
        'first_name': 123,
        'last_name': 123,
    }

    g_mock = mocker.patch('modules.user_account.routes_admin.g')
    g_mock.user = Administrator()

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique_email() validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_account()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_account_route_ok(app, mocker, client):
    expected_status = 200
    expected_m_length = 8
    expected_m_id = 1
    expected_m_username = "admin1a"
    expected_m_email = "admin1a@test.com"
    expected_m_first_name = "TommyA"
    expected_m_last_name = "LundA"
    expected_m_uri = "http://localhost/administrator/1"
    expected_m_password_changed_at = None
    expected_m_joined_at = None

    request_mock = mocker.patch('modules.user_account.routes_admin.request')
    request_mock.json = {
        'username': expected_m_username,
        'email': expected_m_email,
        'first_name': expected_m_first_name,
        'last_name': expected_m_last_name,
    }

    admin1 = Administrator()
    admin1.id = 1
    admin1.username = 'admin1'
    admin1.email = 'admin1@test.com'
    admin1.first_name = 'Tommy'
    admin1.last_name = 'Lund'

    g_mock = mocker.patch('modules.user_account.routes_admin.g')
    g_mock.user = admin1

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock unique(), unique_email() validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    db_mock = mocker.patch('modules.user_account.routes_admin.db')
    db_mock.commit.return_value = None

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.return_value = True

    response = client.put("/user_account?app_key=123")

    assert response.status_code == expected_status
    assert 'user_account' in response.json
    assert len(response.json['user_account']) == expected_m_length
    assert response.json['user_account']['id'] == expected_m_id
    assert response.json['user_account']['username'] == expected_m_username
    assert response.json['user_account']['email'] == expected_m_email
    assert response.json['user_account']['first_name'] == \
           expected_m_first_name
    assert response.json['user_account']['last_name'] == expected_m_last_name
    assert response.json['user_account']['uri'] == expected_m_uri
    assert response.json['user_account']['password_changed_at'] == \
           expected_m_password_changed_at
    assert response.json['user_account']['joined_at'] == expected_m_joined_at


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_account_route_no_app_key(app, client):
    expected_status = 401

    response = client.put("/user_account")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_account_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.put("/user_account?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_account_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.put("/user_account?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_password_ok(app, mocker):
    expected_status = 200
    expected_m_json = {'success': 'true'}

    request_mock = mocker.patch('modules.user_account.routes_admin.request')
    request_mock.json = {
        'previous_password': "admin1pass",
        'password1': "admin1Pass2",
        'password2': "admin1Pass2",
    }

    role = Role()
    role.password_policy = True
    role.password_reuse_history = 10

    admin1 = Administrator()
    admin1.password = "admin1pass"
    admin1.roles = [role]

    g_mock = mocker.patch('modules.user_account.routes_admin.g')
    g_mock.user = admin1

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    pw_history1 = AdministratorPasswordHistory()
    pw_history1.password = "$2b$04$fpn.utPgc5S3InjyWvm1auoGq/NgpG1/Cjnu6WJNNzz6AZBeUAes2"

    # mock password history
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .__iter__.return_value = [pw_history1]

    db_mock = mocker.patch('modules.user_account.routes_admin.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    result = put_password()

    assert result[1] == expected_status
    assert result[0].json == expected_m_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_password_required_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'password1': ['Missing data for required field.'],
            'password2': ['Missing data for required field.'],
            'previous_password': ['Missing data for required field.'],
        }
    }

    request_mock = mocker.patch('modules.user_account.routes_admin.request')
    request_mock.json = {'foo': "bar"}

    g_mock = mocker.patch('modules.user_account.routes_admin.g')
    g_mock.user = Administrator()

    result = put_password()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_password_previous_password_incorrect_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'previous_password': ['Incorrect password.']}}

    request_mock = mocker.patch('modules.user_account.routes_admin.request')
    request_mock.json = {
        'previous_password': "bad_pass",
        'password1': "admin1Pass2",
        'password2': "admin1Pass2",
    }

    admin1 = Administrator()
    admin1.password = "admin1pass"

    g_mock = mocker.patch('modules.user_account.routes_admin.g')
    g_mock.user = admin1

    result = put_password()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_password_password1_complexity_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'password1': ['Please choose a more complex password.']}}

    request_mock = mocker.patch('modules.user_account.routes_admin.request')
    request_mock.json = {
        'previous_password': "admin1pass",
        'password1': "password",
        'password2': "password",
    }

    admin1 = Administrator()
    admin1.password = "admin1pass"

    g_mock = mocker.patch('modules.user_account.routes_admin.g')
    g_mock.user = admin1

    result = put_password()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_password_password2_match_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'password2': ['New passwords must match.']}}

    request_mock = mocker.patch('modules.user_account.routes_admin.request')
    request_mock.json = {
        'previous_password': "admin1pass",
        'password1': "admin1Pass2",
        'password2': "admin1Pass3",
    }

    admin1 = Administrator()
    admin1.password = "admin1pass"

    g_mock = mocker.patch('modules.user_account.routes_admin.g')
    g_mock.user = admin1

    result = put_password()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_password_password_history_reuse_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'password1': ['This password has recently been used.']}}

    request_mock = mocker.patch('modules.user_account.routes_admin.request')
    request_mock.json = {
        'previous_password': "admin1Pass",
        'password1': "admin1Pass2",
        'password2': "admin1Pass2",
    }

    role = Role()
    role.password_policy = True
    role.password_reuse_history = 10

    admin1 = Administrator()
    admin1.password = "admin1Pass"
    admin1.roles = [role]

    g_mock = mocker.patch('modules.user_account.routes_admin.g')
    g_mock.user = admin1

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    pw_history1 = AdministratorPasswordHistory()
    pw_history1.password = "$2b$04$R6qjwKEIkvLLBvyfJMqjPeopGW3mz98maNA0VC9VMNkSoYGmrHaIK"

    # mock password history
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .__iter__.return_value = [pw_history1]

    db_mock = mocker.patch('modules.user_account.routes_admin.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    result = put_password()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_password_route_ok(app, mocker, client):
    expected_status = 200
    expected_m_json = {'success': 'true'}

    request_mock = mocker.patch('modules.user_account.routes_admin.request')
    request_mock.json = {
        'previous_password': "admin1pass",
        'password1': "admin1Pass2",
        'password2': "admin1Pass2",
    }

    role = Role()
    role.password_policy = True
    role.password_reuse_history = 10

    admin1 = Administrator()
    admin1.password = "admin1pass"
    admin1.roles = [role]

    g_mock = mocker.patch('modules.user_account.routes_admin.g')
    g_mock.user = admin1

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    pw_history1 = AdministratorPasswordHistory()
    pw_history1.password = "$2b$04$fpn.utPgc5S3InjyWvm1auoGq/NgpG1/Cjnu6WJNNzz6AZBeUAes2"

    # mock password history
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .__iter__.return_value = [pw_history1]

    db_mock = mocker.patch('modules.user_account.routes_admin.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.return_value = True

    response = client.put("/user_account/password?app_key=123")

    assert response.status_code == expected_status

    assert response.status_code == expected_status
    assert response.json == expected_m_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_password_route_no_app_key(app, client):
    expected_status = 401

    response = client.put("/user_account/password")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_password_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.put("/user_account/password?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_password_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.put("/user_account/password?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


# INTEGRATION TESTS


@pytest.mark.integration
@pytest.mark.admin_api
def test_get_account_route_with_data(client):
    expected_status = 200
    expected_json = {
            "user_account": {
            "email": "admin1@test.com",
            "first_name": "Tommy",
            "id": 1,
            "joined_at": "2018-11-01T00:00:00+0000",
            "last_name": "Lund",
            "password_changed_at": "2018-11-04T00:00:00+0000",
            "uri": "http://localhost/administrator/1",
            "username": "admin1"
        }
    }

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get(
        "/user_account?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.integration
@pytest.mark.admin_api
def test_put_account_route_with_data(client, mocker):
    expected_status = 200
    expected_m_length = 8
    expected_m_id = 1
    expected_m_username = "admin1a"
    expected_m_email = "admin1a@test.com"
    expected_m_first_name = "TommyA"
    expected_m_last_name = "LundA"
    expected_m_uri = "http://localhost/administrator/1"
    expected_m_password_changed_at = "2018-11-04T00:00:00+0000"
    expected_m_joined_at = "2018-11-01T00:00:00+0000"

    request_mock = mocker.patch('modules.user_account.routes_admin.request')
    request_mock.json = {
        'username': expected_m_username,
        'email': expected_m_email,
        'first_name': expected_m_first_name,
        'last_name': expected_m_last_name,
    }

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.put(
        "/user_account?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert 'user_account' in response.json
    assert len(response.json['user_account']) == expected_m_length
    assert response.json['user_account']['id'] == expected_m_id
    assert response.json['user_account']['username'] == expected_m_username
    assert response.json['user_account']['email'] == expected_m_email
    assert response.json['user_account']['first_name'] == \
           expected_m_first_name
    assert response.json['user_account']['last_name'] == expected_m_last_name
    assert response.json['user_account']['uri'] == expected_m_uri
    assert response.json['user_account']['password_changed_at'] == \
           expected_m_password_changed_at
    assert response.json['user_account']['joined_at'] == expected_m_joined_at


@pytest.mark.integration
@pytest.mark.admin_api
def test_put_password_route_with_data(client, mocker):
    expected_status = 200
    expected_m_json = {'success': 'true'}

    request_mock = mocker.patch('modules.user_account.routes_admin.request')
    request_mock.json = {
        'previous_password': "admin1pass",
        'password1': "admin1Pass2",
        'password2': "admin1Pass2",
    }

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.put(
        "/user_account/password?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_m_json
