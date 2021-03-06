from copy import copy
import base64

import pytest
from werkzeug.exceptions import Unauthorized
from sqlalchemy.orm.exc import NoResultFound

from fixtures import Fixtures
from app import create_app
from config import Config
from modules.logins.routes_admin import get_logins
from modules.logins.model import Login
from modules.app_keys.model import AppKey
from modules.administrators.model import Administrator
from modules.roles.model import Role


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
def test_get_logins(app, mocker):
    expected_status = 200
    expected_length = 2
    expected_json = {
        'api': None,
        'attempt_date': None,
        'created_at': None,
        'id': None,
        'ip_address': None,
        'success': None,
        'user_id': None,
        'username': None,
        'updated_at': None,
    }
    expected_limit = 25
    expected_page = 1
    expected_total = 2

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [Login()] * expected_length
    query_mock.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    result = get_logins()

    assert result[1] == expected_status
    assert len(result[0].json['logins']) == expected_length
    assert result[0].json['logins'][0] == expected_json
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_logins_limit_10_page_2_of_3(app, mocker):
    expected_status = 200
    expected_length = 10
    expected_json = {
        'api': None,
        'attempt_date': None,
        'created_at': None,
        'id': None,
        'ip_address': None,
        'success': None,
        'user_id': None,
        'username': None,
        'updated_at': None,
    }
    expected_limit = 10
    expected_page = 2
    expected_total = 25
    expected_previous_uri = 'http://localhost/logins/1/10'
    expected_next_uri = 'http://localhost/logins/3/10'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [Login()] * expected_length
    query_mock.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    result = get_logins(expected_page, expected_limit)

    assert result[1] == expected_status
    assert len(result[0].json['logins']) == expected_length
    assert result[0].json['logins'][0] == expected_json
    assert result[0].json['previous_uri'] == expected_previous_uri
    assert result[0].json['next_uri'] == expected_next_uri
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_logins_empty(app, mocker):
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

    result = get_logins(5, 10)

    assert result[1] == expected_status
    assert result[0] == expected_content


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_logins_filter(app, mocker):
    expected_status = 200
    expected_length = 2
    expected_json = {
        'api': None,
        'attempt_date': None,
        'created_at': None,
        'id': None,
        'ip_address': None,
        'success': None,
        'user_id': None,
        'username': None,
        'updated_at': None,
    }
    expected_limit = 25
    expected_page = 1
    expected_total = 2

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .order_by.return_value \
        .filter.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [Login()] * expected_length
    query_mock.return_value \
        .order_by.return_value \
        .filter.return_value \
        .count.return_value = expected_total

    request_mock = mocker.patch('modules.logins.routes_admin.request')
    request_mock.args = {'user_id': 1}  # could by any other filter criteria

    result = get_logins()

    assert result[1] == expected_status
    assert len(result[0].json['logins']) == expected_length
    assert result[0].json['logins'][0] == expected_json
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_logins_route(app, mocker, client):
    expected_status = 200
    expected_length = 25
    expected_limit = 25
    expected_page = 1
    expected_total = 30
    expected_next_uri = 'http://localhost/logins/2/25'

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
        .__iter__.return_value = [Login()] * expected_length
    query_mock.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    # mock user login
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get("/logins?app_key=123",
                          headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert len(response.json['logins']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_logins_limit_5_page_2_of_3_route(app, mocker, client):
    expected_status = 200
    expected_length = 5
    expected_limit = 5
    expected_page = 2
    expected_total = 12
    expected_next_uri = 'http://localhost/logins/3/5'
    expected_previous_uri = 'http://localhost/logins/1/5'

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
        .__iter__.return_value = [Login()] * expected_length
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
        "/logins/{}/{}?app_key=123".format(expected_page, expected_limit),
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert len(response.json['logins']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri
    assert response.json['previous_uri'] == expected_previous_uri


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_logins_empty_route(app, mocker, client):
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
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = []
    query_mock.return_value \
        .order_by.return_value \
        .count.return_value = 15

    # mock user login
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get("/logins/3?app_key=123",
                          headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_logins_filter_route(app, mocker, client):
    expected_status = 200
    expected_length = 25
    expected_limit = 25
    expected_page = 1
    expected_total = 30
    expected_next_uri = 'http://localhost/logins/2/25?user_id=1'

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
        .__iter__.return_value = [Login()] * expected_length
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

    response = client.get("/logins?user_id=1&app_key=123",
                          headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert len(response.json['logins']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_logins_route_no_app_key(app, client):
    expected_status = 401

    response = client.get("/logins")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_logins_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.get("/logins?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_logins_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.get("/logins?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


# INTEGRATION TESTS


@pytest.mark.integration
@pytest.mark.admin_api
def test_get_logins_route_with_data(client):
    expected_status = 200
    expected_json = {
        "limit": 25,
        "logins": [
            {
                "api": 1,
                "attempt_date": "2018-12-01T08:32:55+0000",
                "created_at": "2018-12-01T08:32:56+0000",
                "id": 1,
                "ip_address": "1.1.1.1",
                "success": True,
                "updated_at": "2018-12-01T08:32:57+0000",
                "user_id": 1,
                "username": "admin1"
            },
            {
                "api": 1,
                "attempt_date": "2018-12-02T12:02:21+0000",
                "created_at": "2018-12-02T12:02:22+0000",
                "id": 2,
                "ip_address": "1.1.1.1",
                "success": False,
                "updated_at": "2018-12-02T12:02:23+0000",
                "user_id": 1,
                "username": "admin1"
            },
            {
                "api": 1,
                "attempt_date": "2018-12-02T21:00:00+0000",
                "created_at": "2018-12-02T22:00:00+0000",
                "id": 3,
                "ip_address": "1.1.1.1",
                "success":True,
                "updated_at": "2018-12-02T23:00:00+0000",
                "user_id": 1,
                "username": "admin1"
            },
            {
                "api": 2,
                "attempt_date": "2018-12-10T20:47:30+0000",
                "created_at": "2018-12-10T20:47:31+0000",
                "id": 4,
                "ip_address": "1.1.1.2",
                "success": True,
                "updated_at": "2018-12-10T20:47:32+0000",
                "user_id": 2,
                "username": "user2"
            },
            {
                "api": 2,
                "attempt_date": "2018-12-22T23:11:53+0000",
                "created_at": "2018-12-22T23:11:54+0000",
                "id": 5,
                "ip_address": "9.9.9.9",
                "success": False,
                "updated_at": "2018-12-22T23:11:55+0000",
                "user_id": 2,
                "username": "user2"
            },
            {
                "api": 2,
                "attempt_date": "2018-12-22T23:12:28+0000",
                "created_at": "2018-12-22T23:12:29+0000",
                "id": 6,
                "ip_address": "9.9.9.9",
                "success": False,
                "updated_at": "2018-12-22T23:12:30+0000",
                "user_id": 2,
                "username": "user2"
            },
            {
                "api": 2,
                "attempt_date": "2018-12-15T07:32:18+0000",
                "created_at": "2018-12-15T07:32:19+0000",
                "id": 7,
                "ip_address": "1.1.1.3",
                "success": True,
                "updated_at": "2018-12-15T07:32:20+0000",
                "user_id": 3,
                "username": "user3"
            },
            {
                "api": 2,
                "attempt_date": "2019-01-08T02:40:21+0000",
                "created_at": "2019-01-08T02:40:22+0000",
                "id": 8,
                "ip_address": "9.9.9.9",
                "success": False,
                "updated_at": "2019-01-08T02:40:23+0000",
                "user_id": None,
                "username": "root"
            }
        ],
        "page": 1,
        "total": 9
    }

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get(
        "/logins?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json['limit'] == expected_json['limit']
    assert response.json['page'] == expected_json['page']
    assert response.json['total'] == expected_json['total']
    assert response.json['logins'][0] == expected_json['logins'][0]
    assert response.json['logins'][1] == expected_json['logins'][1]
    assert response.json['logins'][2] == expected_json['logins'][2]
    assert response.json['logins'][3] == expected_json['logins'][3]
    assert response.json['logins'][4] == expected_json['logins'][4]
    assert response.json['logins'][5] == expected_json['logins'][5]
    assert response.json['logins'][6] == expected_json['logins'][6]
    assert response.json['logins'][7] == expected_json['logins'][7]


@pytest.mark.integration
@pytest.mark.admin_api
def test_get_logins_filter_route_with_data(client):
    expected_status = 200
    expected_json = {
        "limit": 25,
        "logins": [
            {
                "api": 1,
                "attempt_date": "2018-12-01T08:32:55+0000",
                "created_at": "2018-12-01T08:32:56+0000",
                "id": 1,
                "ip_address": "1.1.1.1",
                "success": True,
                "updated_at": "2018-12-01T08:32:57+0000",
                "user_id": 1,
                "username": "admin1"
            },
            {
                "api": 1,
                "attempt_date": "2018-12-02T12:02:21+0000",
                "created_at": "2018-12-02T12:02:22+0000",
                "id": 2,
                "ip_address": "1.1.1.1",
                "success": False,
                "updated_at": "2018-12-02T12:02:23+0000",
                "user_id": 1,
                "username": "admin1"
            },
            {
                "api": 1,
                "attempt_date": "2018-12-02T21:00:00+0000",
                "created_at": "2018-12-02T22:00:00+0000",
                "id": 3,
                "ip_address": "1.1.1.1",
                "success": True,
                "updated_at": "2018-12-02T23:00:00+0000",
                "user_id": 1,
                "username": "admin1"
            }
        ],
        "page": 1,
        "total": 3
    }

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get(
        "/logins?ip_address=1.1.1.1&app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json
