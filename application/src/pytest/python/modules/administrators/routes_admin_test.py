import re

import pytest
from werkzeug.exceptions import NotFound

from fixtures import Fixtures
from app import create_app
from config import Config
from modules.administrators.routes_admin import get_administrators, \
    post_administrator, get_administrator, put_administrator, \
    delete_administrator
from modules.administrators.model import Administrator
from modules.roles.model import Role


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
def test_get_administrators(app, mocker):
    expected_status = 200
    expected_length = 2
    expected_json = {
        'created_at': None,
        'email': None,
        'first_name': None,
        'id': None,
        'joined_at': None,
        'last_name': None,
        'password_changed_at': None,
        'roles': [],
        'status': None,
        'status_changed_at': None,
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
        .__iter__.return_value = [Administrator()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    result = get_administrators()

    assert result[1] == expected_status
    assert len(result[0].json['administrators']) == expected_length
    assert result[0].json['administrators'][0] == expected_json
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
def test_get_administrators_limit_10_page_2_of_3(app, mocker):
    expected_status = 200
    expected_length = 10
    expected_json = {
        'created_at': None,
        'email': None,
        'first_name': None,
        'id': None,
        'joined_at': None,
        'last_name': None,
        'password_changed_at': None,
        'roles': [],
        'status': None,
        'status_changed_at': None,
        'uri': None,
        'updated_at': None,
        'username': None
    }
    expected_limit = 10
    expected_page = 2
    expected_total = 25
    expected_previous_uri = 'http://localhost/administrators/1/10'
    expected_next_uri = 'http://localhost/administrators/3/10'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [Administrator()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    result = get_administrators(expected_page, expected_limit)

    assert result[1] == expected_status
    assert len(result[0].json['administrators']) == expected_length
    assert result[0].json['administrators'][0] == expected_json
    assert result[0].json['previous_uri'] == expected_previous_uri
    assert result[0].json['next_uri'] == expected_next_uri
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
def test_get_administrators_empty(app, mocker):
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

    result = get_administrators(5, 10)

    assert result[1] == expected_status
    assert result[0] == expected_content


@pytest.mark.unit
def test_get_administrators_by_role(app, mocker):
    expected_status = 200
    expected_length = 5
    expected_json = {
        'created_at': None,
        'email': None,
        'first_name': None,
        'id': None,
        'joined_at': None,
        'last_name': None,
        'password_changed_at': None,
        'roles': [],
        'status': None,
        'status_changed_at': None,
        'uri': None,
        'updated_at': None,
        'username': None
    }
    expected_limit = 5
    expected_page = 2
    expected_total = 14
    expected_previous_uri = 'http://localhost/administrators/1/5?role=1'
    expected_next_uri = 'http://localhost/administrators/3/5?role=1'

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.args = {'role': '1'}

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .filter.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [Administrator()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .filter.return_value \
        .count.return_value = expected_total

    result = get_administrators(expected_page, expected_limit)

    assert result[1] == expected_status
    assert len(result[0].json['administrators']) == expected_length
    assert result[0].json['administrators'][0] == expected_json
    assert result[0].json['previous_uri'] == expected_previous_uri
    assert result[0].json['next_uri'] == expected_next_uri
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
def test_get_administrators_route(app, mocker, client):
    expected_status = 200
    expected_length = 10
    expected_limit = 10
    expected_page = 1
    expected_total = 15
    expected_next_uri = 'http://localhost/administrators/2/10'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [Administrator()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    response = client.get("/administrators")

    assert response.status_code == expected_status
    assert len(response.json['administrators']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri


@pytest.mark.unit
def test_get_administrators_limit_5_page_2_of_3_route(app, mocker, client):
    expected_status = 200
    expected_length = 5
    expected_limit = 5
    expected_page = 2
    expected_total = 12
    expected_next_uri = 'http://localhost/administrators/3/5'
    expected_previous_uri = 'http://localhost/administrators/1/5'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [Administrator()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    response = client.get("/administrators/{}/{}".format(expected_page,
                                                         expected_limit))

    assert response.status_code == expected_status
    assert len(response.json['administrators']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri
    assert response.json['previous_uri'] == expected_previous_uri


@pytest.mark.unit
def test_get_administrators_empty_route(app, mocker, client):
    expected_status = 204
    expected_json = None

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

    response = client.get("/administrators/3")

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.unit
def test_get_administrator_ok(app, mocker):
    expected_status = 200
    expected_json = {
        'created_at': None,
        'email': None,
        'first_name': None,
        'id': None,
        'joined_at': None,
        'last_name': None,
        'password_changed_at': None,
        'roles': [],
        'status': None,
        'status_changed_at': None,
        'uri': None,
        'updated_at': None,
        'username': None
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = Administrator()

    result = get_administrator(1)

    assert result[1] == expected_status
    assert result[0].json['administrator'] == expected_json


@pytest.mark.unit
def test_get_administrator_not_found(app, mocker):
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = None

    try:
        get_administrator(250)
        assert False
    except NotFound:
        assert True


@pytest.mark.unit
def test_post_administrator_ok(app, mocker):
    expected_status = 201
    expected_m_length = 13
    expected_m_email = 'admin8@test.com'
    expected_m_id = None
    expected_m_first_name = 'Blanch'
    expected_m_last_name = 'Causer'
    expected_m_joined_at = '2019-02-10T00:00:00+0000'
    expected_m_username = 'admin8'
    expected_m_role_id = 2
    expected_m_roles = [{'id': expected_m_role_id, 'name': 'SUPER_ADMIN'}]
    expected_m_uri = None
    expected_m_status = Administrator.STATUS_ENABLED
    expected_m_created_at = None
    expected_m_updated_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {
        'email': expected_m_email,
        'first_name': expected_m_first_name,
        'joined_at': expected_m_joined_at,
        'last_name': expected_m_last_name,
        'roles': [expected_m_role_id],
        'status': expected_m_status,
        'username': expected_m_username,
        'password': 'user8Pass'
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock exists() validation
    role_2 = Role()
    role_2.id = 2
    role_2.name = 'SUPER_ADMIN'
    query_mock.return_value \
        .get.return_value = role_2

    db_mock = mocker.patch('modules.administrators.routes_admin.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    result = post_administrator()

    assert result[1] == expected_status
    assert 'administrator' in result[0].json
    assert len(result[0].json['administrator']) == expected_m_length
    assert result[0].json['administrator']['id'] == expected_m_id
    assert result[0].json['administrator']['username'] == expected_m_username
    assert result[0].json['administrator']['email'] == expected_m_email
    assert result[0].json['administrator']['first_name'] == \
        expected_m_first_name
    assert result[0].json['administrator']['last_name'] == expected_m_last_name
    assert result[0].json['administrator']['joined_at'] == expected_m_joined_at
    assert result[0].json['administrator']['roles'] == expected_m_roles
    assert result[0].json['administrator']['uri'] == expected_m_uri
    assert result[0].json['administrator']['status'] == expected_m_status
    assert bool(re_datetime.match(
        result[0].json['administrator']['password_changed_at']))
    assert bool(re_datetime.match(
        result[0].json['administrator']['status_changed_at']))
    assert result[0].json['administrator']['created_at'] == \
        expected_m_created_at
    assert result[0].json['administrator']['updated_at'] == \
        expected_m_updated_at


@pytest.mark.unit
def test_post_administrator_required_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'email': ['Missing data for required field.'],
            'first_name': ['Missing data for required field.'],
            'joined_at': ['Missing data for required field.'],
            'last_name': ['Missing data for required field.'],
            'password': ['Missing data for required field.'],
            'roles': ['Missing data for required field.'],
            'status': ['Missing data for required field.'],
            'username': ['Missing data for required field.']
        }
    }

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {'foo': "bar"}

    result = post_administrator()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_administrator_unique_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'username': ['Value must be unique.'],
        'email': ['Value must be unique.']}}

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {
        'email': 'admin2@test.com',
        'first_name': 'Blanch',
        'joined_at': '2019-02-10T00:00:00+0000',
        'last_name': 'Causer',
        'roles': [2],
        'status': Administrator.STATUS_ENABLED,
        'username': 'admin2',
        'password': 'user8Pass'
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = Administrator()

    # mock exists() validation
    role_2 = Role()
    role_2.id = 2
    role_2.name = 'SUPER_ADMIN'
    query_mock.return_value \
        .get.return_value = role_2

    result = post_administrator()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_administrator_role_exists_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'roles': ['Invalid value.']}}

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {
        'email': 'admin8@test.com',
        'first_name': 'Blanch',
        'joined_at': '2019-02-10T00:00:00+0000',
        'last_name': 'Causer',
        'roles': [250],
        'status': Administrator.STATUS_ENABLED,
        'username': 'admin8',
        'password': 'user8Pass'
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock exists() validation
    query_mock.return_value \
        .get.return_value = None

    result = post_administrator()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_administrator_password_complexity_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'password': ['Please choose a more complex password.']}}

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {
        'email': 'admin8@test.com',
        'first_name': 'Blanch',
        'joined_at': '2019-02-10T00:00:00+0000',
        'last_name': 'Causer',
        'roles': [2],
        'status': Administrator.STATUS_ENABLED,
        'username': 'admin8',
        'password': 'password'
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock exists() validation
    role_2 = Role()
    role_2.id = 2
    role_2.name = 'SUPER_ADMIN'
    query_mock.return_value \
        .get.return_value = role_2

    result = post_administrator()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_administrator_unique_and_no_first_name_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'email': ['Value must be unique.'],
        'first_name': ['Missing data for required field.'],
        'username': ['Value must be unique.'],
    }}

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {
        'email': 'admin2@test.com',
        'joined_at': '2019-02-10T00:00:00+0000',
        'last_name': 'Causer',
        'roles': [2],
        'status': Administrator.STATUS_ENABLED,
        'username': 'admin2',
        'password': 'user8Pass'
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = Administrator()

    # mock exists() validation
    role_2 = Role()
    role_2.id = 2
    role_2.name = 'SUPER_ADMIN'
    query_mock.return_value \
        .get.return_value = role_2

    result = post_administrator()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_administrator_username_numeric_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'username': ['Value must not be a number.']}}

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {
        'email': 'admin8@test.com',
        'first_name': 'Blanch',
        'joined_at': '2019-02-10T00:00:00+0000',
        'last_name': 'Causer',
        'roles': [2],
        'status': Administrator.STATUS_ENABLED,
        'username': '1234',
        'password': 'admin8Pass'
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock exists() validation
    role_2 = Role()
    role_2.id = 2
    role_2.name = 'SUPER_ADMIN'
    query_mock.return_value \
        .get.return_value = role_2

    result = post_administrator()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_administrator_username_character_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'username': ['Value must contain only alphanumeric characters and the underscore.']
    }}

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {
        'email': 'admin8@test.com',
        'first_name': 'Blanch',
        'joined_at': '2019-02-10T00:00:00+0000',
        'last_name': 'Causer',
        'roles': [2],
        'status': Administrator.STATUS_ENABLED,
        'username': 'a^j&s@',
        'password': 'admin8Pass'
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock exists() validation
    role_2 = Role()
    role_2.id = 2
    role_2.name = 'SUPER_ADMIN'
    query_mock.return_value \
        .get.return_value = role_2

    result = post_administrator()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_administrator_min_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'first_name': ['Value must be between 1 and 40 characters long.'],
        'last_name': ['Value must be between 2 and 40 characters long.'],
        'username': ['Value must be between 2 and 40 characters long.'],
    }}

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {
        'email': 'admin8@test.com',
        'first_name': '',
        'joined_at': '2019-02-10T00:00:00+0000',
        'last_name': 'C',
        'roles': [2],
        'status': Administrator.STATUS_ENABLED,
        'username': 'u',
        'password': 'admin8Pass'
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock exists() validation
    role_2 = Role()
    role_2.id = 2
    role_2.name = 'SUPER_ADMIN'
    query_mock.return_value \
        .get.return_value = role_2

    result = post_administrator()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_administrator_max_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'first_name': ['Value must be between 1 and 40 characters long.'],
        'last_name': ['Value must be between 2 and 40 characters long.'],
        'username': ['Value must be between 2 and 40 characters long.'],
    }}

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {
        'email': 'admin8@test.com',
        'first_name': 'm8nGwwrE2unvKF6MeQesaB2hN3dm89fTgeEJZEUT5',
        'joined_at': '2019-02-10T00:00:00+0000',
        'last_name': 'KVAQ3fFLk5kKg42SGtAZYQZYxLguNvm67j5dDkaqH',
        'roles': [2],
        'status': Administrator.STATUS_ENABLED,
        'username': 'wNTLdgz6H7XTJHU639w8GanQbHBVNrHZV2d3R6yRn',
        'password': 'admin8Pass'
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock exists() validation
    role_2 = Role()
    role_2.id = 2
    role_2.name = 'SUPER_ADMIN'
    query_mock.return_value \
        .get.return_value = role_2

    result = post_administrator()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_administrator_empty_roles_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'roles': ['Missing data for required field.']
    }}

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {
        'email': 'admin8@test.com',
        'first_name': 'Blanch',
        'joined_at': '2019-02-10T00:00:00+0000',
        'last_name': 'Causer',
        'roles': [],
        'status': Administrator.STATUS_ENABLED,
        'username': 'admin8',
        'password': 'admin8Pass'
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = post_administrator()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_administrator_type_fail(app, mocker):
    expected_status = 400
    expected_json = {
        "error": {
            'email': ["Not a valid email address."],
            'first_name': ["Not a valid string."],
            'joined_at': ["Not a valid datetime."],
            'last_name': ["Not a valid string."],
            'password': ["Not a valid string."],
            'roles': ['Missing data for required field.'],
            'status': ["Not a valid integer."],
            'username': ["Not a valid string."]
        }
    }

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {
        'email': 123,
        'first_name': 123,
        'joined_at': 123,
        'last_name': 123,
        'status': "bad",
        'username': 123,
        'password': 123
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = post_administrator()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_administrator_route_ok(app, mocker, client):
    expected_status = 201
    expected_m_length = 13
    expected_m_email = 'admin8@test.com'
    expected_m_id = None
    expected_m_first_name = 'Blanch'
    expected_m_last_name = 'Causer'
    expected_m_joined_at = '2019-02-10T00:00:00+0000'
    expected_m_username = 'admin8'
    expected_m_role_id = 2
    expected_m_roles = [{'id': expected_m_role_id, 'name': 'SUPER_ADMIN'}]
    expected_m_uri = None
    expected_m_status = Administrator.STATUS_ENABLED
    expected_m_created_at = None
    expected_m_updated_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {
        'email': expected_m_email,
        'first_name': expected_m_first_name,
        'joined_at': expected_m_joined_at,
        'last_name': expected_m_last_name,
        'roles': [expected_m_role_id],
        'status': expected_m_status,
        'username': expected_m_username,
        'password': 'user8Pass'
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock exists() validation
    role_2 = Role()
    role_2.id = 2
    role_2.name = 'SUPER_ADMIN'
    query_mock.return_value \
        .get.return_value = role_2

    db_mock = mocker.patch('modules.administrators.routes_admin.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    response = client.post("/administrators")

    assert response.status_code == expected_status
    assert 'administrator' in response.json
    assert len(response.json['administrator']) == expected_m_length
    assert response.json['administrator']['id'] == expected_m_id
    assert response.json['administrator']['username'] == expected_m_username
    assert response.json['administrator']['email'] == expected_m_email
    assert response.json['administrator']['first_name'] == \
        expected_m_first_name
    assert response.json['administrator']['last_name'] == expected_m_last_name
    assert response.json['administrator']['joined_at'] == expected_m_joined_at
    assert response.json['administrator']['roles'] == expected_m_roles
    assert response.json['administrator']['uri'] == expected_m_uri
    assert response.json['administrator']['status'] == expected_m_status
    assert bool(re_datetime.match(
        response.json['administrator']['password_changed_at']))
    assert bool(re_datetime.match(
        response.json['administrator']['status_changed_at']))
    assert response.json['administrator']['created_at'] == \
        expected_m_created_at
    assert response.json['administrator']['updated_at'] == \
        expected_m_updated_at


@pytest.mark.unit
def test_put_administrator_ok(app, mocker):
    expected_status = 200
    expected_m_length = 13
    expected_m_email = 'admin1a@test.com'
    expected_m_id = 1
    expected_m_first_name = 'TommyA'
    expected_m_last_name = 'LundB'
    expected_m_joined_at = '2018-11-09T08:00:00+0000'
    expected_m_username = 'admin1a'
    expected_m_role_id = 1
    expected_m_roles = [{'id': expected_m_role_id, 'name': 'USER'}]
    expected_m_uri = 'http://localhost/administrator/1'
    expected_m_status = Administrator.STATUS_DISABLED
    expected_m_created_at = None
    expected_m_updated_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {
        'email': expected_m_email,
        'first_name': expected_m_first_name,
        'joined_at': expected_m_joined_at,
        'last_name': expected_m_last_name,
        'password': 'admin8Pass2',
        'roles': [expected_m_role_id],
        'status': expected_m_status,
        'username': expected_m_username
    }

    administrator_1 = Administrator()
    administrator_1.id = expected_m_id

    role_1 = Role()
    role_1.id = 1
    role_1.name = 'USER'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [administrator_1, role_1]

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    db_mock = mocker.patch('modules.administrators.routes_admin.db')
    db_mock.commit.return_value = None

    result = put_administrator(expected_m_id)

    assert result[1] == expected_status
    assert 'administrator' in result[0].json
    assert len(result[0].json['administrator']) == expected_m_length
    assert result[0].json['administrator']['id'] == expected_m_id
    assert result[0].json['administrator']['username'] == expected_m_username
    assert result[0].json['administrator']['email'] == expected_m_email
    assert result[0].json['administrator']['first_name'] == \
        expected_m_first_name
    assert result[0].json['administrator']['last_name'] == expected_m_last_name
    assert result[0].json['administrator']['joined_at'] == expected_m_joined_at
    assert result[0].json['administrator']['roles'] == expected_m_roles
    assert result[0].json['administrator']['uri'] == expected_m_uri
    assert result[0].json['administrator']['status'] == expected_m_status
    assert bool(re_datetime.match(
        result[0].json['administrator']['password_changed_at']))
    assert bool(re_datetime.match(
        result[0].json['administrator']['status_changed_at']))
    assert result[0].json['administrator']['created_at'] == \
        expected_m_created_at
    assert result[0].json['administrator']['updated_at'] == \
        expected_m_updated_at


@pytest.mark.unit
def test_put_administrator_no_password_ok(app, mocker):
    expected_status = 200
    expected_m_length = 13
    expected_m_email = 'admin1a@test.com'
    expected_m_id = 1
    expected_m_first_name = 'TommyA'
    expected_m_last_name = 'LundB'
    expected_m_joined_at = '2018-11-09T08:00:00+0000'
    expected_m_username = 'admin1a'
    expected_m_role_id = 1
    expected_m_roles = [{'id': expected_m_role_id, 'name': 'USER'}]
    expected_m_uri = 'http://localhost/administrator/1'
    expected_m_status = Administrator.STATUS_DISABLED
    expected_m_password_changed_at = None
    expected_m_created_at = None
    expected_m_updated_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {
        'email': expected_m_email,
        'first_name': expected_m_first_name,
        'joined_at': expected_m_joined_at,
        'last_name': expected_m_last_name,
        'roles': [expected_m_role_id],
        'status': expected_m_status,
        'username': expected_m_username
    }

    administrator_1 = Administrator()
    administrator_1.id = expected_m_id

    role_1 = Role()
    role_1.id = 1
    role_1.name = 'USER'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [administrator_1, role_1]

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    db_mock = mocker.patch('modules.administrators.routes_admin.db')
    db_mock.commit.return_value = None

    result = put_administrator(expected_m_id)

    assert result[1] == expected_status
    assert 'administrator' in result[0].json
    assert len(result[0].json['administrator']) == expected_m_length
    assert result[0].json['administrator']['id'] == expected_m_id
    assert result[0].json['administrator']['username'] == expected_m_username
    assert result[0].json['administrator']['email'] == expected_m_email
    assert result[0].json['administrator']['first_name'] == \
        expected_m_first_name
    assert result[0].json['administrator']['last_name'] == expected_m_last_name
    assert result[0].json['administrator']['joined_at'] == expected_m_joined_at
    assert result[0].json['administrator']['roles'] == expected_m_roles
    assert result[0].json['administrator']['uri'] == expected_m_uri
    assert result[0].json['administrator']['status'] == expected_m_status
    assert bool(re_datetime.match(
        result[0].json['administrator']['status_changed_at']))
    assert result[0].json['administrator']['password_changed_at'] == \
        expected_m_password_changed_at
    assert result[0].json['administrator']['created_at'] == \
        expected_m_created_at
    assert result[0].json['administrator']['updated_at'] == \
        expected_m_updated_at


@pytest.mark.unit
def test_put_administrator_required_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'email': ['Missing data for required field.'],
            'first_name': ['Missing data for required field.'],
            'joined_at': ['Missing data for required field.'],
            'last_name': ['Missing data for required field.'],
            'roles': ['Missing data for required field.'],
            'status': ['Missing data for required field.'],
            'username': ['Missing data for required field.']
        }
    }

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {'foo': "bar"}

    administrator_1 = Administrator()
    administrator_1.id = 1

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.return_value = administrator_1

    result = put_administrator(1)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_put_administrator_unique_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'username': ['Value must be unique.'],
        'email': ['Value must be unique.']}}

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {
        'email': 'admin2@test.com',
        'first_name': 'TommyA',
        'joined_at': '2018-11-09T08:00:00+0000',
        'last_name': 'LundB',
        'roles': [1],
        'status': Administrator.STATUS_DISABLED,
        'username': 'admin2'
    }

    administrator_1 = Administrator()
    administrator_1.id = 1

    role_1 = Role()
    role_1.id = 1
    role_1.name = 'USER'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [administrator_1, role_1]

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = Administrator()

    result = put_administrator(1)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_put_administrator_role_exists_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'roles': ['Invalid value.']}}

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {
        'email': 'admin1a@test.com',
        'first_name': 'TommyA',
        'joined_at': '2018-11-09T08:00:00+0000',
        'last_name': 'LundB',
        'roles': [250],
        'status': Administrator.STATUS_DISABLED,
        'username': 'admin1a'
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    administrator_1 = Administrator()
    administrator_1.id = 1

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [administrator_1, None]

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_administrator(1)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_put_administrator_password_complexity_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'password': ['Please choose a more complex password.']}}

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {
        'email': 'admin1a@test.com',
        'first_name': 'TommyA',
        'joined_at': '2018-11-09T08:00:00+0000',
        'last_name': 'LundB',
        'roles': [1],
        'status': Administrator.STATUS_DISABLED,
        'username': 'admin1a',
        'password': 'password'
    }

    administrator_1 = Administrator()
    administrator_1.id = 1

    role_1 = Role()
    role_1.id = 1
    role_1.name = 'USER'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [administrator_1, role_1]

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_administrator(1)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_put_administrator_unique_and_no_first_name_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'email': ['Value must be unique.'],
        'first_name': ['Missing data for required field.'],
        'username': ['Value must be unique.'],
    }}

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {
        'email': 'admin2@test.com',
        'joined_at': '2018-11-09T08:00:00+0000',
        'last_name': 'LundB',
        'roles': [1],
        'status': Administrator.STATUS_DISABLED,
        'username': 'admin2'
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    administrator_1 = Administrator()
    administrator_1.id = 1

    role_1 = Role()
    role_1.id = 1
    role_1.name = 'USER'

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [administrator_1, role_1]

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = Administrator()

    result = put_administrator(1)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_put_administrator_username_numeric_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'username': ['Value must not be a number.']}}

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {
        'email': 'admin1a@test.com',
        'first_name': 'TommyA',
        'joined_at': '2018-11-09T08:00:00+0000',
        'last_name': 'LundB',
        'roles': [1],
        'status': Administrator.STATUS_DISABLED,
        'username': '1234'
    }

    administrator_1 = Administrator()
    administrator_1.id = 1

    role_1 = Role()
    role_1.id = 1
    role_1.name = 'USER'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [administrator_1, role_1]

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_administrator(1)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_put_administrator_username_character_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'username': ['Value must contain only alphanumeric characters and the underscore.']
    }}

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {
        'email': 'admin1a@test.com',
        'first_name': 'TommyA',
        'joined_at': '2018-11-09T08:00:00+0000',
        'last_name': 'LundB',
        'roles': [1],
        'status': Administrator.STATUS_DISABLED,
        'username': 'a$g&j@'
    }

    administrator_1 = Administrator()
    administrator_1.id = 1

    role_1 = Role()
    role_1.id = 1
    role_1.name = 'USER'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [administrator_1, role_1]

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_administrator(1)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_put_administrator_min_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'first_name': ['Value must be between 1 and 40 characters long.'],
        'last_name': ['Value must be between 2 and 40 characters long.'],
        'username': ['Value must be between 2 and 40 characters long.'],
    }}

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {
        'email': 'admin1a@test.com',
        'first_name': '',
        'joined_at': '2018-11-09T08:00:00+0000',
        'last_name': 'L',
        'roles': [1],
        'status': Administrator.STATUS_DISABLED,
        'username': 'u'
    }

    administrator_1 = Administrator()
    administrator_1.id = 1

    role_1 = Role()
    role_1.id = 1
    role_1.name = 'USER'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [administrator_1, role_1]

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_administrator(1)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_put_administrator_max_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'first_name': ['Value must be between 1 and 40 characters long.'],
        'last_name': ['Value must be between 2 and 40 characters long.'],
        'username': ['Value must be between 2 and 40 characters long.'],
    }}

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {
        'email': 'admin1a@test.com',
        'first_name': 'gK8pxsdZsPbgBN2xPnCCAb7BmgSyX2aUHLaC2r7ma',
        'joined_at': '2018-11-09T08:00:00+0000',
        'last_name': 'YgarSUnTRwqyZuwzeespERtfFNED2W3YVYs5mwDZg',
        'roles': [1],
        'status': Administrator.STATUS_DISABLED,
        'username': 'PMUBaSfTAuAQc3ytAL4nQUV7zBVw538WtBW5wB6FA'
    }

    administrator_1 = Administrator()
    administrator_1.id = 1

    role_1 = Role()
    role_1.id = 1
    role_1.name = 'USER'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [administrator_1, role_1]

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_administrator(1)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_put_administrator_empty_roles_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'roles': ['Missing data for required field.']
    }}

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {
        'email': 'admin1a@test.com',
        'first_name': 'TommyA',
        'joined_at': '2018-11-09T08:00:00+0000',
        'last_name': 'LundB',
        'roles': [],
        'status': Administrator.STATUS_DISABLED,
        'username': 'admin1a'
    }

    administrator_1 = Administrator()
    administrator_1.id = 1

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query
    query_mock.return_value \
        .get.return_value = administrator_1

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_administrator(1)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_put_administrator_type_fail(app, mocker):
    expected_status = 400
    expected_json = {
        "error": {
            'email': ["Not a valid email address."],
            'first_name': ["Not a valid string."],
            'joined_at': ["Not a valid datetime."],
            'last_name': ["Not a valid string."],
            'password': ["Not a valid string."],
            'roles': ['Missing data for required field.'],
            'status': ["Not a valid integer."],
            'username': ["Not a valid string."]
        }
    }

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {
        'email': 123,
        'first_name': 123,
        'joined_at': 123,
        'last_name': 123,
        'status': "bad",
        'username': 123,
        'password': 123
    }

    administrator_1 = Administrator()
    administrator_1.id = 1

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query
    query_mock.return_value \
        .get.return_value = administrator_1

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_administrator(1)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_put_administrator_route_ok(app, mocker, client):
    expected_status = 200
    expected_m_length = 13
    expected_m_email = 'admin1a@test.com'
    expected_m_id = 1
    expected_m_first_name = 'TommyA'
    expected_m_last_name = 'LundB'
    expected_m_joined_at = '2018-11-09T08:00:00+0000'
    expected_m_username = 'admin1a'
    expected_m_role_id = 1
    expected_m_roles = [{'id': expected_m_role_id, 'name': 'USER'}]
    expected_m_uri = 'http://localhost/administrator/1'
    expected_m_status = Administrator.STATUS_DISABLED
    expected_m_created_at = None
    expected_m_updated_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {
        'email': expected_m_email,
        'first_name': expected_m_first_name,
        'joined_at': expected_m_joined_at,
        'last_name': expected_m_last_name,
        'roles': [expected_m_role_id],
        'status': expected_m_status,
        'username': expected_m_username,
        'password': 'user8Pass2'
    }

    administrator_1 = Administrator()
    administrator_1.id = 1

    role_1 = Role()
    role_1.id = 1
    role_1.name = 'USER'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [administrator_1, role_1]

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    db_mock = mocker.patch('modules.administrators.routes_admin.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    response = client.put("/administrator/{}".format(expected_m_role_id))

    assert response.status_code == expected_status
    assert 'administrator' in response.json
    assert len(response.json['administrator']) == expected_m_length
    assert response.json['administrator']['id'] == expected_m_id
    assert response.json['administrator']['username'] == expected_m_username
    assert response.json['administrator']['email'] == expected_m_email
    assert response.json['administrator']['first_name'] == \
        expected_m_first_name
    assert response.json['administrator']['last_name'] == expected_m_last_name
    assert response.json['administrator']['joined_at'] == expected_m_joined_at
    assert response.json['administrator']['roles'] == expected_m_roles
    assert response.json['administrator']['uri'] == expected_m_uri
    assert response.json['administrator']['status'] == expected_m_status
    assert bool(re_datetime.match(
        response.json['administrator']['password_changed_at']))
    assert bool(re_datetime.match(
        response.json['administrator']['status_changed_at']))
    assert response.json['administrator']['created_at'] == \
        expected_m_created_at
    assert response.json['administrator']['updated_at'] == \
        expected_m_updated_at


@pytest.mark.unit
def test_delete_administrator_ok(app, mocker):
    expected_status = 204
    expected_content = ''

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = Administrator()

    db_mock = mocker.patch('modules.administrators.routes_admin.db')
    db_mock.commit.return_value = None

    result = delete_administrator(1)

    assert result[1] == expected_status
    assert result[0] == expected_content


@pytest.mark.unit
def test_delete_administrator_fail(app, mocker):
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = None

    try:
        delete_administrator(250)
        assert False
    except NotFound:
        assert True


# INTEGRATION TESTS


@pytest.mark.integration
def test_get_administrators_route_with_data(client):
    expected_status = 200
    expected_json = {
        "administrators": [
            {
                "created_at": "2018-11-01T00:00:00+0000",
                "email": "admin1@test.com",
                "first_name": "Tommy",
                "id": 1,
                "joined_at": "2018-11-01T00:00:00+0000",
                "last_name": "Lund",
                "password_changed_at": "2018-11-04T00:00:00+0000",
                "roles": [
                    {
                      "id": 2,
                      "name": "SUPER_ADMIN"
                    }
                ],
                "status": 1,
                "status_changed_at": "2018-11-03T00:00:00+0000",
                "updated_at": "2018-11-02T00:00:00+0000",
                "uri": "http://localhost/administrator/1",
                "username": "admin1"
            },
            {
                "created_at": "2018-11-05T00:00:00+0000",
                "email": "admin2@test.com",
                "first_name": "Selma",
                "id": 2,
                "joined_at": "2018-11-05T00:00:00+0000",
                "last_name": "Keyes",
                "password_changed_at": "2018-11-08T00:00:00+0000",
                "roles": [
                    {
                      "id": 2,
                      "name": "SUPER_ADMIN"
                    }
                ],
                "status": 1,
                "status_changed_at": "2018-11-07T00:00:00+0000",
                "updated_at": "2018-11-06T00:00:00+0000",
                "uri": "http://localhost/administrator/2",
                "username": "admin2"
            },
            {
                "created_at": "2018-11-10T00:00:00+0000",
                "email": "admin3@test.com",
                "first_name": "Victor",
                "id": 3,
                "joined_at": "2018-11-15T00:00:00+0000",
                "last_name": "Landon",
                "password_changed_at": "2018-11-13T00:00:00+0000",
                "roles": [],
                "status": 1,
                "status_changed_at": "2018-11-12T00:00:00+0000",
                "updated_at": "2018-11-11T00:00:00+0000",
                "uri": "http://localhost/administrator/3",
                "username": "admin3"
            },
            {
                "created_at": "2018-11-15T00:00:00+0000",
                "email": "admin4@test.com",
                "first_name": "Tamela",
                "id": 4,
                "joined_at": "2018-11-20T00:00:00+0000",
                "last_name": "Coburn",
                "password_changed_at": "2018-11-18T00:00:00+0000",
                "roles": [
                    {
                      "id": 2,
                      "name": "SUPER_ADMIN"
                    }
                ],
                "status": 2,
                "status_changed_at": "2018-11-17T00:00:00+0000",
                "updated_at": "2018-11-16T00:00:00+0000",
                "uri": "http://localhost/administrator/4",
                "username": "admin4"
            },
            {
                "created_at": "2018-12-01T00:00:00+0000",
                "email": "admin7@test.com",
                "first_name": "Nigel",
                "id": 7,
                "joined_at": "2018-11-10T00:00:00+0000",
                "last_name": "Sams",
                "password_changed_at": "2018-11-13T00:00:00+0000",
                "roles": [
                    {
                      "id": 2,
                      "name": "SUPER_ADMIN"
                    }
                ],
                "status": 5,
                "status_changed_at": "2018-12-03T00:00:00+0000",
                "updated_at": "2018-12-02T00:00:00+0000",
                "uri": "http://localhost/administrator/7",
                "username": "admin7"
            }
        ],
        "limit": 10,
        "page": 1,
        "total": 5
    }

    response = client.get("/administrators")

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.integration
def test_get_administrator_1_route_with_data(client):
    expected_status = 200
    expected_json = {
        "administrator": {
            "created_at": "2018-11-01T00:00:00+0000",
            "email": "admin1@test.com",
            "first_name": "Tommy",
            "id": 1,
            "joined_at": "2018-11-01T00:00:00+0000",
            "last_name": "Lund",
            "password_changed_at": "2018-11-04T00:00:00+0000",
            "roles": [
                {
                  "id": 2,
                  "name": "SUPER_ADMIN"
                }
            ],
            "status": 1,
            "status_changed_at": "2018-11-03T00:00:00+0000",
            "updated_at": "2018-11-02T00:00:00+0000",
            "uri": "http://localhost/administrator/1",
            "username": "admin1"
        }
    }

    response = client.get("/administrator/1")

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.integration
def test_post_administrators_route_with_data(client, mocker):
    expected_status = 201
    expected_m_length = 13
    expected_m_email = 'admin8@test.com'
    expected_m_id = 8
    expected_m_first_name = 'Blanch'
    expected_m_last_name = 'Causer'
    expected_m_joined_at = '2019-02-10T00:00:00+0000'
    expected_m_username = 'admin8'
    expected_m_role_id = 2
    expected_m_roles = [{'id': expected_m_role_id, 'name': 'SUPER_ADMIN'}]
    expected_m_uri = 'http://localhost/administrator/8'
    expected_m_status = Administrator.STATUS_ENABLED
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}$")

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {
        'email': expected_m_email,
        'first_name': expected_m_first_name,
        'joined_at': expected_m_joined_at,
        'last_name': expected_m_last_name,
        'roles': [expected_m_role_id],
        'status': expected_m_status,
        'username': expected_m_username,
        'password': 'user8Pass'
    }

    response = client.post("/administrators")

    assert response.status_code == expected_status
    assert 'administrator' in response.json
    assert len(response.json['administrator']) == expected_m_length
    assert response.json['administrator']['id'] == expected_m_id
    assert response.json['administrator']['username'] == expected_m_username
    assert response.json['administrator']['email'] == expected_m_email
    assert response.json['administrator']['first_name'] == \
        expected_m_first_name
    assert response.json['administrator']['last_name'] == expected_m_last_name
    assert response.json['administrator']['joined_at'] == expected_m_joined_at
    assert response.json['administrator']['roles'] == expected_m_roles
    assert response.json['administrator']['uri'] == expected_m_uri
    assert response.json['administrator']['status'] == expected_m_status
    assert bool(re_datetime.match(
        response.json['administrator']['password_changed_at']))
    assert bool(re_datetime.match(
        response.json['administrator']['status_changed_at']))
    assert bool(re_datetime.match(
        response.json['administrator']['created_at']))
    assert bool(re_datetime.match(
        response.json['administrator']['updated_at']))


@pytest.mark.integration
def test_put_administrator_route_with_data(client, mocker):
    expected_status = 200
    expected_m_length = 13
    expected_m_email = 'admin1a@test.com'
    expected_m_id = 1
    expected_m_first_name = 'TommyA'
    expected_m_last_name = 'LundB'
    expected_m_joined_at = '2018-11-09T08:00:00+0000'
    expected_m_username = 'admin1a'
    expected_m_role_id = 1
    expected_m_roles = [{'id': expected_m_role_id, 'name': 'USER'}]
    expected_m_uri = 'http://localhost/administrator/1'
    expected_m_status = Administrator.STATUS_DISABLED
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}$")

    request_mock = mocker.patch('modules.administrators.routes_admin.request')
    request_mock.json = {
        'email': expected_m_email,
        'first_name': expected_m_first_name,
        'joined_at': expected_m_joined_at,
        'last_name': expected_m_last_name,
        'roles': [expected_m_role_id],
        'status': expected_m_status,
        'username': expected_m_username,
        'password': 'user8Pass2'
    }

    response = client.put("/administrator/{}".format(expected_m_id))

    assert response.status_code == expected_status
    assert 'administrator' in response.json
    assert len(response.json['administrator']) == expected_m_length
    assert response.json['administrator']['id'] == expected_m_id
    assert response.json['administrator']['username'] == expected_m_username
    assert response.json['administrator']['email'] == expected_m_email
    assert response.json['administrator']['first_name'] == \
        expected_m_first_name
    assert response.json['administrator']['last_name'] == expected_m_last_name
    assert response.json['administrator']['joined_at'] == expected_m_joined_at
    assert response.json['administrator']['roles'] == expected_m_roles
    assert response.json['administrator']['uri'] == expected_m_uri
    assert response.json['administrator']['status'] == expected_m_status
    assert bool(re_datetime.match(
        response.json['administrator']['password_changed_at']))
    assert bool(re_datetime.match(
        response.json['administrator']['status_changed_at']))
    assert bool(re_datetime.match(
        response.json['administrator']['created_at']))
    assert bool(re_datetime.match(
        response.json['administrator']['updated_at']))


@pytest.mark.integration
def test_delete_administrator_1_route_with_data(client):
    expected_status = 204
    expected_json = None

    response = client.delete("/administrator/1")

    assert response.status_code == expected_status
    assert response.json == expected_json
