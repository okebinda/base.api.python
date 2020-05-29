from copy import copy
import re
import base64

import pytest
from werkzeug.exceptions import NotFound, Unauthorized
from sqlalchemy.orm.exc import NoResultFound

from fixtures import Fixtures
from app import create_app
from config import Config
from modules.app_keys.routes_admin import get_app_keys, post_app_keys, \
    get_app_key, put_app_key, delete_app_key
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
def test_get_app_keys(app, mocker):
    expected_status = 200
    expected_length = 2
    expected_properties = ['application', 'created_at', 'id', 'key', 'status',
                           'status_changed_at', 'updated_at']
    expected_limit = 10
    expected_page = 1
    expected_total = 2

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [AppKey()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    result = get_app_keys()

    assert result[1] == expected_status
    assert len(result[0].json['app_keys']) == expected_length
    assert result[0].json['app_keys'][0] == {
        x: None for x in expected_properties}
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_app_keys_limit_10_page_2_of_3(app, mocker):
    expected_status = 200
    expected_length = 10
    expected_properties = ['application', 'created_at', 'id', 'key', 'status',
                           'status_changed_at', 'updated_at']
    expected_limit = 10
    expected_page = 2
    expected_total = 25
    expected_previous_uri = 'http://localhost/app_keys/1/10'
    expected_next_uri = 'http://localhost/app_keys/3/10'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [AppKey()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    result = get_app_keys(expected_page, expected_limit)

    assert result[1] == expected_status
    assert len(result[0].json['app_keys']) == expected_length
    assert result[0].json['app_keys'][0] == {
        x: None for x in expected_properties}
    assert result[0].json['previous_uri'] == expected_previous_uri
    assert result[0].json['next_uri'] == expected_next_uri
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_app_keys_empty(app, mocker):
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

    result = get_app_keys(5, 10)

    assert result[1] == expected_status
    assert result[0] == expected_content


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_app_keys_route(app, mocker, client):
    expected_status = 200
    expected_length = 10
    expected_limit = 10
    expected_page = 1
    expected_total = 15
    expected_next_uri = 'http://localhost/app_keys/2/10'

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
        .__iter__.return_value = [AppKey()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.return_value = True

    response = client.get("/app_keys?app_key=123")

    assert response.status_code == expected_status
    assert len(response.json['app_keys']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_app_keys_limit_5_page_2_of_3_route(app, mocker, client):
    expected_status = 200
    expected_length = 5
    expected_limit = 5
    expected_page = 2
    expected_total = 12
    expected_next_uri = 'http://localhost/app_keys/3/5'
    expected_previous_uri = 'http://localhost/app_keys/1/5'

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
        .__iter__.return_value = [AppKey()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.return_value = True

    response = client.get(
        "/app_keys/{}/{}?app_key=123".format(expected_page,
                                             expected_limit))

    assert response.status_code == expected_status
    assert len(response.json['app_keys']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri
    assert response.json['previous_uri'] == expected_previous_uri


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_app_keys_empty_route(app, mocker, client):
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

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.return_value = True

    response = client.get("/app_keys/3?app_key=123")

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_app_keys_route_no_app_key(app, client):
    expected_status = 401

    response = client.get("/app_keys")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_app_keys_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.get("/app_keys?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_app_keys_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.get("/app_keys?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_app_key_ok(app, mocker):
    expected_status = 200
    expected_properties = ['application', 'created_at', 'id', 'key', 'status',
                           'status_changed_at', 'updated_at']

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = AppKey()

    result = get_app_key(1)

    assert result[1] == expected_status
    assert result[0].json['app_key'] == {
        x: None for x in expected_properties}


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_app_key_not_found(app, mocker):
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = None

    try:
        get_app_key(250)
        assert False
    except NotFound:
        assert True


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_app_key_route_ok(app, mocker, client):
    expected_status = 200

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock resource query
    query_mock.return_value \
        .get.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.return_value = True

    response = client.get("/app_key/1?app_key=123")

    assert response.status_code == expected_status
    assert 'app_key' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_app_key_route_no_app_key(app, client):
    expected_status = 401

    response = client.get("/app_key/1")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_app_key_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.get("/app_key/1?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_app_key_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.get("/app_key/1?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_app_key_ok(app, mocker):
    expected_status = 201
    expected_m_length = 7
    expected_m_application = 'Test Application'
    expected_m_id = None
    expected_m_key = 'B8CzqaJWs9TmffSJjxDCFrepzhvYzrKz'
    expected_m_status = AppKey.STATUS_ENABLED
    expected_m_created_at = None
    expected_m_updated_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch('modules.app_keys.routes_admin.request')
    request_mock.json = {
        'application': expected_m_application,
        'key': expected_m_key,
        "status": expected_m_status
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    db_mock = mocker.patch('modules.app_keys.routes_admin.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    result = post_app_keys()

    assert result[1] == expected_status
    assert 'app_key' in result[0].json
    assert len(result[0].json['app_key']) == expected_m_length
    assert result[0].json['app_key']['application'] == expected_m_application
    assert result[0].json['app_key']['id'] == expected_m_id
    assert result[0].json['app_key']['key'] == expected_m_key
    assert result[0].json['app_key']['status'] == expected_m_status
    assert bool(re_datetime.match(
        result[0].json['app_key']['status_changed_at']))
    assert result[0].json['app_key']['created_at'] == expected_m_created_at
    assert result[0].json['app_key']['updated_at'] == expected_m_updated_at


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_app_key_unique_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {'key': ['Value must be unique.']}}

    request_mock = mocker.patch('modules.app_keys.routes_admin.request')
    request_mock.json = {
        'application': "Test Application",
        'key': "B8CzqaJWs9TmffSJjxDCFrepzhvYzrKz",
        "status": 1
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = AppKey()

    result = post_app_keys()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_app_key_required_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'application': ['Missing data for required field.'],
            'foo': ['Unknown field.'],
            'key': ['Missing data for required field.'],
            'status': ['Missing data for required field.'],
        }
    }

    request_mock = mocker.patch('modules.app_keys.routes_admin.request')
    request_mock.json = {'foo': "bar"}

    result = post_app_keys()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_app_key_min_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'application': [
                'Value must be between 2 and 200 characters long.'],
            'key': ['Value must be 32 characters long.'],
        }
    }

    request_mock = mocker.patch('modules.app_keys.routes_admin.request')
    request_mock.json = {
        'application': "T",
        'key': "B8CzqaJWs9TmffSJjxDCFrepzhvYzrK",
        "status": 1
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = post_app_keys()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_app_key_max_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'application': [
                'Value must be between 2 and 200 characters long.'],
            'key': ['Value must be 32 characters long.'],
        }
    }

    request_mock = mocker.patch('modules.app_keys.routes_admin.request')
    request_mock.json = {
        'application': "9xAqdEjnQ8uHmQjnSWUutERKfmgBFjWWsKkwKy4EBbpjeC8FuAXYH4bBqg5FVGapD47LTDsJmUU7dgUrxBVuSjhRUcQvxxukMvVs87ndpZ76DK9ZULFB77DjGDxmqJ5QHfEV6FjNXK2sbkFzdUBbbkPkcGpvgMqamdP33WpMFcDXpAftcRJyUJtMpVStZ3MMBS7LLVuBaDSBznGSfnpzTk6dS8zhnxpy8EayF6LSuKUjN3d2JkCrRDge5W8Rcmve",
        'key': "AFJdJ9JCUhASZ4cA2ptC7CA72bYKLZD28",
        "status": 1
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = post_app_keys()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_app_key_type_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'application': ['Not a valid string.'],
            'key': ['Not a valid string.'],
            'status': ['Not a valid integer.'],
        }
    }

    request_mock = mocker.patch('modules.app_keys.routes_admin.request')
    request_mock.json = {
        'application': 10,
        'key': 15,
        "status": 'enabled'
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = post_app_keys()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_app_key_route_ok(app, mocker, client):
    expected_status = 201
    expected_m_length = 7
    expected_m_application = 'Test Application'
    expected_m_id = None
    expected_m_key = 'B8CzqaJWs9TmffSJjxDCFrepzhvYzrKz'
    expected_m_status = AppKey.STATUS_ENABLED
    expected_m_created_at = None
    expected_m_updated_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch('modules.app_keys.routes_admin.request')
    request_mock.json = {
        'application': expected_m_application,
        'key': expected_m_key,
        "status": expected_m_status
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.return_value = True

    db_mock = mocker.patch('modules.app_keys.routes_admin.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    response = client.post("/app_keys?app_key=123")

    assert response.status_code == expected_status
    assert 'app_key' in response.json
    assert len(response.json['app_key']) == expected_m_length
    assert response.json['app_key']['application'] == expected_m_application
    assert response.json['app_key']['id'] == expected_m_id
    assert response.json['app_key']['key'] == expected_m_key
    assert response.json['app_key']['status'] == expected_m_status
    assert bool(re_datetime.match(
        response.json['app_key']['status_changed_at']))
    assert response.json['app_key']['created_at'] == expected_m_created_at
    assert response.json['app_key']['updated_at'] == expected_m_updated_at


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_app_key_route_no_app_key(app, client):
    expected_status = 401

    response = client.post("/app_keys")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_app_key_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.post("/app_keys?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_app_key_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.post("/app_keys?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_app_key_ok(app, mocker):
    expected_status = 200
    expected_m_length = 7
    expected_m_application = 'Test Application A'
    expected_m_id = 1
    expected_m_key = 'B8CzqaJWs9TmffSJjxDCFrepzhvYzrKA'
    expected_m_status = AppKey.STATUS_ENABLED
    expected_m_created_at = None
    expected_m_updated_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch('modules.app_keys.routes_admin.request')
    request_mock.json = {
        'application': expected_m_application,
        'key': expected_m_key,
        "status": expected_m_status
    }

    app_key_1 = AppKey()
    app_key_1.id = expected_m_id

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = app_key_1
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    db_mock = mocker.patch('modules.app_keys.routes_admin.db')
    db_mock.commit.return_value = None

    result = put_app_key(expected_m_id)

    assert result[1] == expected_status
    assert 'app_key' in result[0].json
    assert len(result[0].json['app_key']) == expected_m_length
    assert result[0].json['app_key']['application'] == expected_m_application
    assert result[0].json['app_key']['id'] == expected_m_id
    assert result[0].json['app_key']['key'] == expected_m_key
    assert result[0].json['app_key']['status'] == expected_m_status
    assert bool(re_datetime.match(
        result[0].json['app_key']['status_changed_at']))
    assert result[0].json['app_key']['created_at'] == expected_m_created_at
    assert result[0].json['app_key']['updated_at'] == expected_m_updated_at


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_app_key_unique_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {'key': ['Value must be unique.']}}

    request_mock = mocker.patch('modules.app_keys.routes_admin.request')
    request_mock.json = {
        'application': "Test Application",
        'key': "B8CzqaJWs9TmffSJjxDCFrepzhvYzrKz",
        "status": 1
    }

    app_key_1 = AppKey()
    app_key_1.id = 1

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = app_key_1
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = AppKey()

    result = put_app_key(1)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_app_key_required_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'application': ['Missing data for required field.'],
            'foo': ['Unknown field.'],
            'key': ['Missing data for required field.'],
            'status': ['Missing data for required field.'],
        }
    }

    request_mock = mocker.patch('modules.app_keys.routes_admin.request')
    request_mock.json = {'foo': "bar"}

    app_key_1 = AppKey()
    app_key_1.id = 1

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = app_key_1
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_app_key(1)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_app_key_min_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'application': [
                'Value must be between 2 and 200 characters long.'],
            'key': ['Value must be 32 characters long.'],
        }
    }

    request_mock = mocker.patch('modules.app_keys.routes_admin.request')
    request_mock.json = {
        'application': "T",
        'key': "B8CzqaJWs9TmffSJjxDCFrepzhvYzrK",
        "status": 1
    }

    app_key_1 = AppKey()
    app_key_1.id = 1

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = app_key_1
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_app_key(1)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_app_key_max_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'application': [
                'Value must be between 2 and 200 characters long.'],
            'key': ['Value must be 32 characters long.'],
        }
    }

    request_mock = mocker.patch('modules.app_keys.routes_admin.request')
    request_mock.json = {
        'application': "9xAqdEjnQ8uHmQjnSWUutERKfmgBFjWWsKkwKy4EBbpjeC8FuAXYH4bBqg5FVGapD47LTDsJmUU7dgUrxBVuSjhRUcQvxxukMvVs87ndpZ76DK9ZULFB77DjGDxmqJ5QHfEV6FjNXK2sbkFzdUBbbkPkcGpvgMqamdP33WpMFcDXpAftcRJyUJtMpVStZ3MMBS7LLVuBaDSBznGSfnpzTk6dS8zhnxpy8EayF6LSuKUjN3d2JkCrRDge5W8Rcmve",
        'key': "AFJdJ9JCUhASZ4cA2ptC7CA72bYKLZD28",
        "status": 1
    }

    app_key_1 = AppKey()
    app_key_1.id = 1

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = app_key_1
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_app_key(1)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_app_key_type_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'application': ['Not a valid string.'],
            'key': ['Not a valid string.'],
            'status': ['Not a valid integer.'],
        }
    }

    request_mock = mocker.patch('modules.app_keys.routes_admin.request')
    request_mock.json = {
        'application': 10,
        'key': 15,
        "status": 'enabled'
    }

    app_key_1 = AppKey()
    app_key_1.id = 1

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = app_key_1
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_app_key(1)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_app_key_route_ok(app, mocker, client):
    expected_status = 200
    expected_m_length = 7
    expected_m_application = 'Test Application A'
    expected_m_id = AppKey.STATUS_ENABLED
    expected_m_key = 'B8CzqaJWs9TmffSJjxDCFrepzhvYzrKA'
    expected_m_status = AppKey.STATUS_DISABLED
    expected_m_created_at = None
    expected_m_updated_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch('modules.app_keys.routes_admin.request')
    request_mock.json = {
        'application': expected_m_application,
        'key': expected_m_key,
        "status": expected_m_status
    }

    app_key_1 = AppKey()
    app_key_1.id = expected_m_id

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    query_mock.return_value \
        .get.return_value = app_key_1
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    db_mock = mocker.patch('modules.app_keys.routes_admin.db')
    db_mock.commit.return_value = None

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.return_value = True

    response = client.put("/app_key/{}?app_key=123".format(expected_m_id))

    assert response.status_code == expected_status
    assert 'app_key' in response.json
    assert len(response.json['app_key']) == expected_m_length
    assert response.json['app_key']['application'] == expected_m_application
    assert response.json['app_key']['id'] == expected_m_id
    assert response.json['app_key']['key'] == expected_m_key
    assert response.json['app_key']['status'] == expected_m_status
    assert bool(re_datetime.match(
        response.json['app_key']['status_changed_at']))
    assert response.json['app_key']['created_at'] == expected_m_created_at
    assert response.json['app_key']['updated_at'] == expected_m_updated_at


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_app_key_route_no_app_key(app, client):
    expected_status = 401

    response = client.put("/app_key/1")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_app_key_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.put("/app_key/1?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_app_key_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.put("/app_key/1?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_delete_app_key_ok(app, mocker):
    expected_status = 204
    expected_content = ''

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = AppKey()

    db_mock = mocker.patch('modules.app_keys.routes_admin.db')
    db_mock.commit.return_value = None

    result = delete_app_key(1)

    assert result[1] == expected_status
    assert result[0] == expected_content


@pytest.mark.unit
@pytest.mark.admin_api
def test_delete_app_key_fail(app, mocker):
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = None

    try:
        delete_app_key(250)
        assert False
    except NotFound:
        assert True


@pytest.mark.unit
@pytest.mark.admin_api
def test_delete_app_key_route_ok(app, mocker, client):
    expected_status = 204
    expected_json = None

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock resource query
    query_mock.return_value \
        .get.return_value = AppKey()

    # mock db commit
    db_mock = mocker.patch('modules.administrators.routes_admin.db')
    db_mock.commit.return_value = None

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.return_value = True

    response = client.delete("/app_key/5?app_key=123")

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_delete_app_key_route_no_app_key(app, client):
    expected_status = 401

    response = client.delete("/app_key/5")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_delete_app_key_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.delete("/app_key/5?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_delete_app_key_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.delete("/app_key/5?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


# INTEGRATION TESTS


@pytest.mark.integration
@pytest.mark.admin_api
def test_get_app_keys_route_with_data(client):
    expected_status = 200
    expected_json = {
        "app_keys": [
            {
                "application": "Application 1",
                "created_at": "2018-01-01T00:00:00+0000",
                "id": 1,
                "key": "7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
                "status": 1,
                "status_changed_at": "2018-01-03T00:00:00+0000",
                "updated_at": "2018-01-02T00:00:00+0000"
            },
            {
                "application": "Application 2",
                "created_at": "2018-01-05T00:00:00+0000",
                "id": 2,
                "key": "cvBtQGgL9gNnSZk4DmKnva4QMcpTV7Mx",
                "status": 1,
                "status_changed_at": "2018-01-07T00:00:00+0000",
                "updated_at": "2018-01-06T00:00:00+0000"
            },
            {
                "application": "Application 3",
                "created_at": "2018-01-10T00:00:00+0000",
                "id": 3,
                "key": "9CR45hFpTahbqDvmZFJdENAKz5VPqLG3",
                "status": 2,
                "status_changed_at": "2018-01-12T00:00:00+0000",
                "updated_at": "2018-01-11T00:00:00+0000"
            },
            {
                "application": "Application 6",
                "created_at": "2018-01-25T00:00:00+0000",
                "id": 6,
                "key": "kP4k7vun5RwTBbESwHrCuDdFUtRchbVf",
                "status": 5,
                "status_changed_at": "2018-01-27T00:00:00+0000",
                "updated_at": "2018-01-26T00:00:00+0000"
            }
        ],
        "limit": 10,
        "page": 1,
        "total": 4
    }

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get(
        "/app_keys?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.integration
@pytest.mark.admin_api
def test_get_app_key_1_route_with_data(client):
    expected_status = 200
    expected_json = {
        "app_key": {
            "application": "Application 1",
            "created_at": "2018-01-01T00:00:00+0000",
            "id": 1,
            "key": "7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
            "status": 1,
            "status_changed_at": "2018-01-03T00:00:00+0000",
            "updated_at": "2018-01-02T00:00:00+0000"
        }
    }

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get(
        "/app_key/1?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.integration
@pytest.mark.admin_api
def test_post_app_keys_route_with_data(client, mocker):
    expected_status = 201
    expected_m_length = 7
    expected_m_application = 'Test Application'
    expected_m_id = 7
    expected_m_key = 'B8CzqaJWs9TmffSJjxDCFrepzhvYzrKz'
    expected_m_status = AppKey.STATUS_ENABLED
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}$")

    request_mock = mocker.patch('modules.app_keys.routes_admin.request')
    request_mock.json = {
        'application': expected_m_application,
        'key': expected_m_key,
        "status": expected_m_status
    }

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.post(
        "/app_keys?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert 'app_key' in response.json
    assert len(response.json['app_key']) == expected_m_length
    assert response.json['app_key']['application'] == expected_m_application
    assert response.json['app_key']['id'] == expected_m_id
    assert response.json['app_key']['key'] == expected_m_key
    assert response.json['app_key']['status'] == expected_m_status
    assert bool(re_datetime.match(
        response.json['app_key']['status_changed_at']))
    assert bool(re_datetime.match(response.json['app_key']['created_at']))
    assert bool(re_datetime.match(response.json['app_key']['updated_at']))


@pytest.mark.integration
@pytest.mark.admin_api
def test_put_app_keys_route_with_data(client, mocker):
    expected_status = 200
    expected_m_length = 7
    expected_m_application = 'Application 2a'
    expected_m_id = 2
    expected_m_key = 'cvBtQGgL9gNnSZk4DmKnva4QMcpTV7MA'
    expected_m_status = AppKey.STATUS_DISABLED
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}$")

    request_mock = mocker.patch('modules.app_keys.routes_admin.request')
    request_mock.json = {
        'application': expected_m_application,
        'key': expected_m_key,
        "status": expected_m_status
    }

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.put(
        "/app_key/{}?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW".format(
            expected_m_id), headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert 'app_key' in response.json
    assert len(response.json['app_key']) == expected_m_length
    assert response.json['app_key']['application'] == expected_m_application
    assert response.json['app_key']['id'] == expected_m_id
    assert response.json['app_key']['key'] == expected_m_key
    assert response.json['app_key']['status'] == expected_m_status
    assert bool(re_datetime.match(
        response.json['app_key']['status_changed_at']))
    assert bool(re_datetime.match(response.json['app_key']['created_at']))
    assert bool(re_datetime.match(response.json['app_key']['updated_at']))


@pytest.mark.integration
@pytest.mark.admin_api
def test_delete_app_key_1_route_with_data(client):
    expected_status = 204
    expected_json = None

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.delete(
        "/app_key/5?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json
