import pytest

from fixtures import Fixtures
from app import create_app
from config import Config
from modules.logins.routes_admin import get_logins
from modules.logins.model import Login


@pytest.fixture
def app(request):
    Config.TESTING = True
    app = create_app(Config)

    if 'unit' in request.keywords:
        # unit tests don't get data fixtures
        yield app
    else:
        # other tests need the test data set
        fixtures = Fixtures(app)
        fixtures.setup()
        yield app
        fixtures.teardown()


# UNIT TESTS


@pytest.mark.unit
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
def test_get_logins_route(app, mocker, client):
    expected_status = 200
    expected_length = 25
    expected_limit = 25
    expected_page = 1
    expected_total = 30
    expected_next_uri = 'http://localhost/logins/2/25'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [Login()] * expected_length
    query_mock.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    response = client.get("/logins")

    assert response.status_code == expected_status
    assert len(response.json['logins']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri


@pytest.mark.unit
def test_get_logins_limit_5_page_2_of_3_route(app, mocker, client):
    expected_status = 200
    expected_length = 5
    expected_limit = 5
    expected_page = 2
    expected_total = 12
    expected_next_uri = 'http://localhost/logins/3/5'
    expected_previous_uri = 'http://localhost/logins/1/5'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [Login()] * expected_length
    query_mock.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    response = client.get("/logins/{}/{}".format(expected_page,
                                                 expected_limit))

    assert response.status_code == expected_status
    assert len(response.json['logins']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri
    assert response.json['previous_uri'] == expected_previous_uri


@pytest.mark.unit
def test_get_logins_empty_route(app, mocker, client):
    expected_status = 204
    expected_json = None

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = []
    query_mock.return_value \
        .order_by.return_value \
        .count.return_value = 15

    response = client.get("/logins/3")

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.unit
def test_get_logins_filter_route(app, mocker, client):
    expected_status = 200
    expected_length = 25
    expected_limit = 25
    expected_page = 1
    expected_total = 30
    expected_next_uri = 'http://localhost/logins/2/25?user_id=1'

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

    response = client.get("/logins?user_id=1")

    assert response.status_code == expected_status
    assert len(response.json['logins']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri


# INTEGRATION TESTS


@pytest.mark.integration
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
        "total": 8
    }

    response = client.get("/logins")

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.integration
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

    response = client.get("/logins?ip_address=1.1.1.1")

    assert response.status_code == expected_status
    assert response.json == expected_json
