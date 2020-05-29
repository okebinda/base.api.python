from copy import copy

import pytest
from sqlalchemy.orm.exc import NoResultFound

from fixtures import Fixtures
from app import create_app
from config import Config
from modules.password_resets.routes_admin import get_password_resets
from modules.password_resets.model import PasswordReset
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
def test_get_password_resets(app, mocker):
    expected_status = 200
    expected_length = 2
    expected_json = {
        'code': None,
        'created_at': None,
        'id': None,
        'ip_address': None,
        'is_used': None,
        'requested_at': None,
        'status': None,
        'status_changed_at': None,
        'updated_at': None,
        'user': None,
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
        .__iter__.return_value = [PasswordReset()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    result = get_password_resets()

    assert result[1] == expected_status
    assert len(result[0].json['password_resets']) == expected_length
    assert result[0].json['password_resets'][0] == expected_json
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_password_resets_limit_10_page_2_of_3(app, mocker):
    expected_status = 200
    expected_length = 10
    expected_json = {
        'code': None,
        'created_at': None,
        'id': None,
        'ip_address': None,
        'is_used': None,
        'requested_at': None,
        'status': None,
        'status_changed_at': None,
        'updated_at': None,
        'user': None,
    }
    expected_limit = 10
    expected_page = 2
    expected_total = 25
    expected_previous_uri = 'http://localhost/password_resets/1/10'
    expected_next_uri = 'http://localhost/password_resets/3/10'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [PasswordReset()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    result = get_password_resets(expected_page, expected_limit)

    assert result[1] == expected_status
    assert len(result[0].json['password_resets']) == expected_length
    assert result[0].json['password_resets'][0] == expected_json
    assert result[0].json['previous_uri'] == expected_previous_uri
    assert result[0].json['next_uri'] == expected_next_uri
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_password_resets_empty(app, mocker):
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

    result = get_password_resets(5, 10)

    assert result[1] == expected_status
    assert result[0] == expected_content


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_password_resets_filter(app, mocker):
    expected_status = 200
    expected_length = 2
    expected_json = {
        'code': None,
        'created_at': None,
        'id': None,
        'ip_address': None,
        'is_used': None,
        'requested_at': None,
        'status': None,
        'status_changed_at': None,
        'updated_at': None,
        'user': None,
    }
    expected_limit = 10
    expected_page = 1
    expected_total = 2

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .filter.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [PasswordReset()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .filter.return_value \
        .count.return_value = expected_total

    request_mock = mocker.patch('modules.password_resets.routes_admin.request')
    request_mock.args = {'user_id': 1}  # could by any other filter criteria

    result = get_password_resets()

    assert result[1] == expected_status
    assert len(result[0].json['password_resets']) == expected_length
    assert result[0].json['password_resets'][0] == expected_json
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_password_resets_route(app, mocker, client):
    expected_status = 200
    expected_length = 10
    expected_limit = 10
    expected_page = 1
    expected_total = 15
    expected_next_uri = 'http://localhost/password_resets/2/10'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [PasswordReset()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    response = client.get("/password_resets?app_key=123")

    assert response.status_code == expected_status
    assert len(response.json['password_resets']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_password_resets_limit_5_page_2_of_3_route(app, mocker, client):
    expected_status = 200
    expected_length = 5
    expected_limit = 5
    expected_page = 2
    expected_total = 12
    expected_next_uri = 'http://localhost/password_resets/3/5'
    expected_previous_uri = 'http://localhost/password_resets/1/5'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [PasswordReset()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    response = client.get("/password_resets/{}/{}?app_key=123".format(
        expected_page, expected_limit))

    assert response.status_code == expected_status
    assert len(response.json['password_resets']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri
    assert response.json['previous_uri'] == expected_previous_uri


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_password_resets_empty_route(app, mocker, client):
    expected_status = 204
    expected_json = None

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

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

    response = client.get("/password_resets/3?app_key=123")

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_password_resets_filter_route(app, mocker, client):
    expected_status = 200
    expected_length = 10
    expected_limit = 10
    expected_page = 1
    expected_total = 15
    expected_next_uri = 'http://localhost/password_resets/2/10?user_id=1'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .filter.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [PasswordReset()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .filter.return_value \
        .count.return_value = expected_total

    response = client.get("/password_resets?user_id=1&app_key=123")

    assert response.status_code == expected_status
    assert len(response.json['password_resets']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_password_resets_route_no_app_key(app, client):
    expected_status = 401

    response = client.get("/password_resets")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_password_resets_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.get("/password_resets?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


# INTEGRATION TESTS


@pytest.mark.integration
@pytest.mark.admin_api
def test_get_password_resets_route_with_data(client):
    expected_status = 200
    expected_json = {
        "limit": 10,
        "page": 1,
        "password_resets": [
            {
                "code": "HD7SF2",
                "created_at": "2019-01-10T00:00:00+0000",
                "id": 1,
                "ip_address": "1.1.1.1",
                "is_used": True,
                "requested_at": "2019-01-10T07:13:49+0000",
                "status": 1,
                "status_changed_at": "2019-01-12T00:00:00+0000",
                "updated_at": "2019-01-11T00:00:00+0000",
                "user": {
                    "id": 1,
                    "uri": "http://localhost/user/1",
                    "username": "user1"
                }
            },
            {
                "code": "M5AF8G",
                "created_at": "2019-01-12T00:00:00+0000",
                "id": 2,
                "ip_address": "1.1.1.2",
                "is_used": True,
                "requested_at": "2019-01-12T14:02:51+0000",
                "status": 1,
                "status_changed_at": "2019-01-14T00:00:00+0000",
                "updated_at": "2019-01-13T00:00:00+0000",
                "user": {
                    "id": 2,
                    "uri": "http://localhost/user/2",
                    "username": "user2"
                }
            },
            {
                "code": "QQ94ND",
                "created_at": "2019-01-15T00:00:00+0000",
                "id": 3,
                "ip_address": "1.1.1.1",
                "is_used": True,
                "requested_at": "2019-01-15T20:46:15+0000",
                "status": 2,
                "status_changed_at": "2019-01-17T00:00:00+0000",
                "updated_at": "2019-01-16T00:00:00+0000",
                "user": {
                    "id": 1,
                    "uri": "http://localhost/user/1",
                    "username": "user1"
                }
            },
            {
                "code": "XAY87R",
                "created_at": "2019-01-20T00:00:00+0000",
                "id": 5,
                "ip_address": "1.1.1.3",
                "is_used": True,
                "requested_at": "2019-01-20T03:37:10+0000",
                "status": 5,
                "status_changed_at": "2019-01-22T00:00:00+0000",
                "updated_at": "2019-01-21T00:00:00+0000",
                "user": {
                    "id": 3,
                    "uri": "http://localhost/user/3",
                    "username": "user3"
                }
            },
            {
                "code": "AM8A4N",
                "created_at": "2019-01-28T00:00:00+0000",
                "id": 7,
                "ip_address": "1.2.3.4",
                "is_used": False,
                "requested_at": "2019-01-28T09:38:58+0000",
                "status": 1,
                "status_changed_at": "2019-01-30T00:00:00+0000",
                "updated_at": "2019-01-29T00:00:00+0000",
                "user": {
                    "id": 2,
                    "uri": "http://localhost/user/2",
                    "username": "user2"
                }
            },
            {
                "code": "PRQ7M2",
                "created_at": "2020-05-27T17:57:23+0000",
                "id": 8,
                "ip_address": "1.2.3.4",
                "is_used": True,
                "requested_at": "2020-05-27T17:57:23+0000",
                "status": 1,
                "status_changed_at": "2020-05-27T17:57:23+0000",
                "updated_at": "2020-05-27T17:57:23+0000",
                "user": {
                    "id": 2,
                    "uri": "http://localhost/user/2",
                    "username": "user2"
                }
            },
            {
                "code": "J91NP0",
                "created_at": "2020-05-27T17:57:23+0000",
                "id": 9,
                "ip_address": "1.2.3.4",
                "is_used": False,
                "requested_at": "2020-05-27T17:57:23+0000",
                "status": 1,
                "status_changed_at": "2020-05-27T17:57:23+0000",
                "updated_at": "2020-05-27T17:57:23+0000",
                "user": {
                    "id": 2,
                    "uri": "http://localhost/user/2",
                    "username": "user2"
                }
            }
        ],
        "total": 7
    }

    response = client.get("/password_resets?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW")

    assert response.status_code == expected_status
    assert response.json['limit'] == expected_json['limit']
    assert response.json['page'] == expected_json['page']
    assert response.json['total'] == expected_json['total']
    assert response.json['password_resets'][0] == \
        expected_json['password_resets'][0]
    assert response.json['password_resets'][1] == \
        expected_json['password_resets'][1]
    assert response.json['password_resets'][2] == \
        expected_json['password_resets'][2]
    assert response.json['password_resets'][3] == \
        expected_json['password_resets'][3]
    assert response.json['password_resets'][4] == \
        expected_json['password_resets'][4]
    assert response.json['password_resets'][5]['code'] == \
        expected_json['password_resets'][5]['code']
    assert response.json['password_resets'][6]['code'] == \
        expected_json['password_resets'][6]['code']


@pytest.mark.integration
@pytest.mark.admin_api
def test_get_password_resets_filter_route_with_data(client):
    expected_status = 200
    expected_json = {
        "limit": 10,
        "page": 1,
        "password_resets": [
            {
                "code": "HD7SF2",
                "created_at": "2019-01-10T00:00:00+0000",
                "id": 1,
                "ip_address": "1.1.1.1",
                "is_used": True,
                "requested_at": "2019-01-10T07:13:49+0000",
                "status": 1,
                "status_changed_at": "2019-01-12T00:00:00+0000",
                "updated_at": "2019-01-11T00:00:00+0000",
                "user": {
                    "id": 1,
                    "uri": "http://localhost/user/1",
                    "username": "user1"
                }
            },
            {
                "code": "QQ94ND",
                "created_at": "2019-01-15T00:00:00+0000",
                "id": 3,
                "ip_address": "1.1.1.1",
                "is_used": True,
                "requested_at": "2019-01-15T20:46:15+0000",
                "status": 2,
                "status_changed_at": "2019-01-17T00:00:00+0000",
                "updated_at": "2019-01-16T00:00:00+0000",
                "user": {
                    "id": 1,
                    "uri": "http://localhost/user/1",
                    "username": "user1"
                }
            }
        ],
        "total": 2
    }

    response = client.get(
        "/password_resets?user_id=1&app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW")

    assert response.status_code == expected_status
    assert response.json == expected_json
