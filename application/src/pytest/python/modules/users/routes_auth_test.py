from copy import copy
import base64

import pytest
from werkzeug.exceptions import NotFound, Unauthorized
from sqlalchemy.orm.exc import NoResultFound

from fixtures import Fixtures
from app import create_app
from config import Config
from modules.users.routes_auth import get_auth_token, get_auth_token_check
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
def test_get_auth_token_ok(app, mocker):
    expected_status = 200
    expected_r_expiration = 14400
    expected_r_user_id = 2
    expected_r_username = "user2"

    user2 = User()
    user2.id = 2
    user2.username = 'user2'

    g_mock = mocker.patch('modules.users.routes_auth.g')
    g_mock.user = user2

    result = get_auth_token()

    assert result[1] == expected_status
    assert result[0].json['expiration'] == expected_r_expiration
    assert result[0].json['user_id'] == expected_r_user_id
    assert result[0].json['username'] == expected_r_username
    assert 'token' in result[0].json


@pytest.mark.unit
def test_get_auth_token_route_ok(app, mocker, client):
    expected_status = 200
    expected_r_expiration = 14400
    expected_r_user_id = 2
    expected_r_username = "user2"

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    role1 = Role()
    role1.id = 1
    role1.name = 'USER'
    role1.password_reset_days = 365
    role1.password_policy = True
    role1.password_reuse_history = 10

    user2 = User()
    user2.id = 2
    user2.username = expected_r_username
    user2.password = "user2pass"
    user2.roles = [role1]

    # mock user login db query
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = user2

    db_mock = mocker.patch('modules.users.authentication.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    # mock user login
    auth_mock = mocker.patch(
        'modules.users.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'user2:user2pass'.encode('ascii')).decode('utf-8')

    response = client.get("/token?app_key=123",
                          headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json['expiration'] == expected_r_expiration
    assert response.json['user_id'] == expected_r_user_id
    assert response.json['username'] == expected_r_username
    assert 'token' in response.json


@pytest.mark.unit
def test_get_auth_token_cap_whitespace_route_ok(app, mocker, client):
    expected_status = 200
    expected_r_expiration = 14400
    expected_r_user_id = 2
    expected_r_username = "user2"

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    role1 = Role()
    role1.id = 1
    role1.name = 'USER'
    role1.password_reset_days = 365
    role1.password_policy = True
    role1.password_reuse_history = 10

    user2 = User()
    user2.id = 2
    user2.username = expected_r_username
    user2.password = "user2pass"
    user2.roles = [role1]

    # mock user login db query
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = user2

    db_mock = mocker.patch('modules.users.authentication.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    # mock user login
    auth_mock = mocker.patch(
        'modules.users.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'User2 :user2pass'.encode('ascii')).decode('utf-8')

    response = client.get("/token?app_key=123",
                          headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json['expiration'] == expected_r_expiration
    assert response.json['user_id'] == expected_r_user_id
    assert response.json['username'] == expected_r_username
    assert 'token' in response.json


@pytest.mark.unit
def test_get_token_route_no_app_key(app, client):
    expected_status = 401

    response = client.get("/token")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
def test_get_token_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.get("/token?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
def test_get_token_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.users.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.get("/token?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
def test_get_auth_token_check_ok(app):
    expected_status = 200
    expected_json = {'token_check': True}

    result = get_auth_token_check()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_get_auth_token_check_route_ok(app, mocker, client):
    expected_status = 200
    expected_json = {'token_check': True}

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    role1 = Role()
    role1.id = 1
    role1.name = 'USER'
    role1.password_reset_days = 365
    role1.password_policy = True
    role1.password_reuse_history = 10

    user2 = User()
    user2.id = 2
    user2.username = "user2"
    user2.password = "user2pass"
    user2.roles = [role1]

    # mock user login db query
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = user2

    db_mock = mocker.patch('modules.users.authentication.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    # mock user login
    auth_mock = mocker.patch(
        'modules.users.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'user2:user2pass'.encode('ascii')).decode('utf-8')

    response = client.get("/token/check?app_key=123",
                          headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.unit
def test_get_auth_token_check_route_no_app_key(app, client):
    expected_status = 401

    response = client.get("/token/check")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
def test_get_auth_token_check_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.get("/token/check?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
def test_get_auth_token_check_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.users.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.get("/token/check?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


# INTEGRATION TESTS


@pytest.mark.integration
def test_get_token_route_with_data(client):
    expected_status = 200
    expected_r_expiration = 14400
    expected_r_user_id = 2
    expected_r_username = "user2"

    credentials = base64.b64encode(
        'user2:user2pass'.encode('ascii')).decode('utf-8')

    response = client.get(
        "/token?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json['expiration'] == expected_r_expiration
    assert response.json['user_id'] == expected_r_user_id
    assert response.json['username'] == expected_r_username
    assert 'token' in response.json


@pytest.mark.integration
def test_get_auth_token_check_route_with_data(client):
    expected_status = 200
    expected_json = {'token_check': True}

    credentials = base64.b64encode(
        'user2:user2pass'.encode('ascii')).decode('utf-8')

    response = client.get(
        "/token/check?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json
