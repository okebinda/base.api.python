from copy import copy
import base64

import pytest
from werkzeug.exceptions import NotFound, Unauthorized
from sqlalchemy.orm.exc import NoResultFound

from fixtures import Fixtures
from app import create_app
from config import Config
from modules.administrators.routes_auth import get_auth_token, \
    get_auth_token_check
from modules.administrators.model import Administrator
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
def test_get_auth_token_ok(app, mocker):
    expected_status = 200
    expected_r_expiration = 14400
    expected_r_user_id = 1
    expected_r_username = "admin1"

    admin1 = Administrator()
    admin1.id = 1
    admin1.username = 'admin1'

    g_mock = mocker.patch('modules.administrators.routes_auth.g')
    g_mock.user = admin1

    result = get_auth_token()

    assert result[1] == expected_status
    assert result[0].json['expiration'] == expected_r_expiration
    assert result[0].json['user_id'] == expected_r_user_id
    assert result[0].json['username'] == expected_r_username
    assert 'token' in result[0].json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_auth_token_route_ok(app, mocker, client):
    expected_status = 200
    expected_r_expiration = 14400
    expected_r_user_id = 1
    expected_r_username = "admin1"

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    admin1 = Administrator()
    admin1.id = 1
    admin1.username = 'admin1'

    g_mock = mocker.patch('modules.administrators.routes_auth.g')
    g_mock.user = admin1

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.return_value = True

    response = client.get("/token?app_key=123")

    assert response.status_code == expected_status
    assert response.json['expiration'] == expected_r_expiration
    assert response.json['user_id'] == expected_r_user_id
    assert response.json['username'] == expected_r_username
    assert 'token' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_token_route_no_app_key(app, client):
    expected_status = 401

    response = client.get("/token")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
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
@pytest.mark.admin_api
def test_get_token_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.get("/token?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_auth_token_check_ok(app):
    expected_status = 200
    expected_json = {'token_check': True}

    result = get_auth_token_check()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_auth_token_check_route_ok(app, mocker, client):
    expected_status = 200
    expected_json = {'token_check': True}

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.return_value = True

    response = client.get("/token/check?app_key=123")

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_auth_token_check_route_no_app_key(app, client):
    expected_status = 401

    response = client.get("/token/check")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
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
@pytest.mark.admin_api
def test_get_auth_token_check_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.get("/token/check?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


# INTEGRATION TESTS


@pytest.mark.integration
@pytest.mark.admin_api
def test_get_token_route_with_data(client):
    expected_status = 200
    expected_r_expiration = 14400
    expected_r_user_id = 1
    expected_r_username = "admin1"

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get(
        "/token?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json['expiration'] == expected_r_expiration
    assert response.json['user_id'] == expected_r_user_id
    assert response.json['username'] == expected_r_username
    assert 'token' in response.json


@pytest.mark.integration
@pytest.mark.admin_api
def test_get_auth_token_check_route_with_data(client):
    expected_status = 200
    expected_json = {'token_check': True}

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get(
        "/token/check?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json
