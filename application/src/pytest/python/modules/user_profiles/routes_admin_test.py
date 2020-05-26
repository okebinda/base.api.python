import re

import pytest
from werkzeug.exceptions import NotFound

from fixtures import Fixtures
from app import create_app
from config import Config
from modules.user_profiles.routes_admin import get_user_profiles, \
    post_user_profiles, get_user_profile, put_user_profile, delete_user_profile
from modules.user_profiles.model import UserProfile
from modules.users.model import User


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
def test_get_user_profiles(app, mocker):
    expected_status = 200
    expected_length = 2
    expected_json = {
        'created_at': None,
        'first_name': None,
        'id': None,
        'joined_at': None,
        'last_name': None,
        'status': None,
        'status_changed_at': None,
        'user_id': None,
        'updated_at': None,

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
        .__iter__.return_value = [UserProfile()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    result = get_user_profiles()

    assert result[1] == expected_status
    assert len(result[0].json['user_profiles']) == expected_length
    assert result[0].json['user_profiles'][0] == expected_json
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
def test_get_user_profiles_limit_10_page_2_of_3(app, mocker):
    expected_status = 200
    expected_length = 10
    expected_json = {
        'created_at': None,
        'first_name': None,
        'id': None,
        'joined_at': None,
        'last_name': None,
        'status': None,
        'status_changed_at': None,
        'user_id': None,
        'updated_at': None,

    }
    expected_limit = 10
    expected_page = 2
    expected_total = 25
    expected_previous_uri = 'http://localhost/user_profiles/1/10'
    expected_next_uri = 'http://localhost/user_profiles/3/10'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [UserProfile()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    result = get_user_profiles(expected_page, expected_limit)

    assert result[1] == expected_status
    assert len(result[0].json['user_profiles']) == expected_length
    assert result[0].json['user_profiles'][0] == expected_json
    assert result[0].json['previous_uri'] == expected_previous_uri
    assert result[0].json['next_uri'] == expected_next_uri
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
def test_get_user_profiles_empty(app, mocker):
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

    result = get_user_profiles(5, 10)

    assert result[1] == expected_status
    assert result[0] == expected_content


@pytest.mark.unit
def test_get_user_profiles_route(app, mocker, client):
    expected_status = 200
    expected_length = 10
    expected_limit = 10
    expected_page = 1
    expected_total = 15
    expected_next_uri = 'http://localhost/user_profiles/2/10'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [UserProfile()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    response = client.get("/user_profiles")

    assert response.status_code == expected_status
    assert len(response.json['user_profiles']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri


@pytest.mark.unit
def test_get_user_profiles_limit_5_page_2_of_3_route(app, mocker, client):
    expected_status = 200
    expected_length = 5
    expected_limit = 5
    expected_page = 2
    expected_total = 12
    expected_next_uri = 'http://localhost/user_profiles/3/5'
    expected_previous_uri = 'http://localhost/user_profiles/1/5'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [UserProfile()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    response = client.get("/user_profiles/{}/{}".format(expected_page,
                                                        expected_limit))

    assert response.status_code == expected_status
    assert len(response.json['user_profiles']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri
    assert response.json['previous_uri'] == expected_previous_uri


@pytest.mark.unit
def test_get_user_profiles_empty_route(app, mocker, client):
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

    response = client.get("/user_profiles/3")

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.unit
def test_get_user_profile_ok(app, mocker):
    expected_status = 200
    expected_json = {
        'created_at': None,
        'first_name': None,
        'id': None,
        'joined_at': None,
        'last_name': None,
        'status': None,
        'status_changed_at': None,
        'user_id': None,
        'updated_at': None,

    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = UserProfile()

    result = get_user_profile(1)

    assert result[1] == expected_status
    assert result[0].json['user_profile'] == expected_json


@pytest.mark.unit
def test_get_user_profile_not_found(app, mocker):
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = None

    try:
        get_user_profile(250)
        assert False
    except NotFound:
        assert True


@pytest.mark.unit
def test_post_user_profile_ok(app, mocker):
    expected_status = 201
    expected_m_length = 9
    expected_m_id = None
    expected_m_user_id = 9
    expected_m_first_name = "Service"
    expected_m_last_name = "Account"
    expected_m_joined_at = "2019-02-04T00:00:00+0000"
    expected_m_status = UserProfile.STATUS_ENABLED
    expected_m_created_at = None
    expected_m_updated_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch('modules.user_profiles.routes_admin.request')
    request_mock.json = {
        'user_id': expected_m_user_id,
        'first_name': expected_m_first_name,
        'last_name': expected_m_last_name,
        'joined_at': expected_m_joined_at,
        'status': expected_m_status,
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock exists() validation
    user_9 = User()
    user_9.id = 9
    query_mock.return_value \
        .get.return_value = user_9

    db_mock = mocker.patch('modules.user_profiles.routes_admin.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    result = post_user_profiles()

    assert result[1] == expected_status
    assert 'user_profile' in result[0].json
    assert len(result[0].json['user_profile']) == expected_m_length
    assert result[0].json['user_profile']['id'] == expected_m_id
    assert result[0].json['user_profile']['user_id'] == expected_m_user_id
    assert result[0].json['user_profile']['first_name'] == \
        expected_m_first_name
    assert result[0].json['user_profile']['last_name'] == expected_m_last_name
    assert result[0].json['user_profile']['joined_at'] == expected_m_joined_at
    assert result[0].json['user_profile']['status'] == expected_m_status
    assert bool(re_datetime.match(
        result[0].json['user_profile']['status_changed_at']))
    assert result[0].json['user_profile']['created_at'] == \
        expected_m_created_at
    assert result[0].json['user_profile']['updated_at'] == \
        expected_m_updated_at


@pytest.mark.unit
def test_post_user_profiles_required_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'user_id': ['Missing data for required field.'],
            'first_name': ['Missing data for required field.'],
            'foo': ['Unknown field.'],
            'joined_at': ['Missing data for required field.'],
            'last_name': ['Missing data for required field.'],
            'status': ['Missing data for required field.'],
        }
    }

    request_mock = mocker.patch('modules.user_profiles.routes_admin.request')
    request_mock.json = {'foo': "bar"}

    result = post_user_profiles()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_user_profiles_user_exists_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'user_id': ['Invalid value.']}}

    request_mock = mocker.patch('modules.user_profiles.routes_admin.request')
    request_mock.json = {
        'user_id': 250,
        'first_name': "Service",
        'last_name': "Account",
        'joined_at': "2019-02-04T00:00:00+0000",
        'status': UserProfile.STATUS_ENABLED
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock exists() validation
    query_mock.return_value \
        .get.return_value = None

    result = post_user_profiles()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_user_profiles_min_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'first_name': ["Value must be between 1 and 40 characters long."],
        'last_name': ["Value must be between 2 and 40 characters long."],
    }}

    request_mock = mocker.patch('modules.user_profiles.routes_admin.request')
    request_mock.json = {
        'user_id': 9,
        'first_name': "",
        'last_name': "A",
        'joined_at': "2019-02-04T00:00:00+0000",
        'status': UserProfile.STATUS_ENABLED
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock exists() validation
    user_9 = User()
    user_9.id = 9
    query_mock.return_value \
        .get.return_value = user_9

    result = post_user_profiles()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_user_profiles_max_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'first_name': ["Value must be between 1 and 40 characters long."],
        'last_name': ["Value must be between 2 and 40 characters long."],
    }}

    request_mock = mocker.patch('modules.user_profiles.routes_admin.request')
    request_mock.json = {
        'user_id': 9,
        'first_name': "LRUNzhfsbfrfZ4BT9N6R3SNYVfAAuQdQdTSmrwFew",
        'last_name': "z3Sytm4QrL8g7J4kgugEABnhwXZAnCZmrngUCeeXm",
        'joined_at': "2019-02-04T00:00:00+0000",
        'status': UserProfile.STATUS_ENABLED
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock exists() validation
    user_9 = User()
    user_9.id = 9
    query_mock.return_value \
        .get.return_value = user_9

    result = post_user_profiles()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_user_profiles_type_fail(app, mocker):
    expected_status = 400
    expected_json = {
        "error": {
            'user_id': ['Not a valid integer.'],
            'first_name': ['Not a valid string.'],
            'joined_at': ['Not a valid datetime.'],
            'last_name': ['Not a valid string.'],
            'status': ['Not a valid integer.'],
        }
    }

    request_mock = mocker.patch('modules.user_profiles.routes_admin.request')
    request_mock.json = {
        'user_id': 'bad',
        'first_name': 123,
        'joined_at': 123,
        'last_name': 123,
        'status': "bad",
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock exists() validation
    query_mock.return_value \
        .get.return_value = None

    result = post_user_profiles()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_user_route_ok(app, mocker, client):
    expected_status = 201
    expected_m_length = 9
    expected_m_id = None
    expected_m_user_id = 9
    expected_m_first_name = "Service"
    expected_m_last_name = "Account"
    expected_m_joined_at = "2019-02-04T00:00:00+0000"
    expected_m_status = UserProfile.STATUS_ENABLED
    expected_m_created_at = None
    expected_m_updated_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch('modules.user_profiles.routes_admin.request')
    request_mock.json = {
        'user_id': expected_m_user_id,
        'first_name': expected_m_first_name,
        'last_name': expected_m_last_name,
        'joined_at': expected_m_joined_at,
        'status': expected_m_status,
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock exists() validation
    user_9 = User()
    user_9.id = 9
    query_mock.return_value \
        .get.return_value = user_9

    db_mock = mocker.patch('modules.user_profiles.routes_admin.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    response = client.post("/user_profiles")

    assert response.status_code == expected_status
    assert 'user_profile' in response.json
    assert len(response.json['user_profile']) == expected_m_length
    assert response.json['user_profile']['id'] == expected_m_id
    assert response.json['user_profile']['user_id'] == expected_m_user_id
    assert response.json['user_profile']['first_name'] == \
        expected_m_first_name
    assert response.json['user_profile']['last_name'] == expected_m_last_name
    assert response.json['user_profile']['joined_at'] == expected_m_joined_at
    assert response.json['user_profile']['status'] == expected_m_status
    assert bool(re_datetime.match(
        response.json['user_profile']['status_changed_at']))
    assert response.json['user_profile']['created_at'] == \
        expected_m_created_at
    assert response.json['user_profile']['updated_at'] == \
        expected_m_updated_at


@pytest.mark.unit
def test_put_user_profile_ok(app, mocker):
    expected_status = 200
    expected_m_length = 9
    expected_m_id = 2
    expected_m_user_id = 9
    expected_m_first_name = "LynneA"
    expected_m_last_name = "HarfordA"
    expected_m_joined_at = "2018-12-09T08:00:00+0000"
    expected_m_status = UserProfile.STATUS_DISABLED
    expected_m_created_at = None
    expected_m_updated_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch('modules.user_profiles.routes_admin.request')
    request_mock.json = {
        'user_id': expected_m_user_id,
        'first_name': expected_m_first_name,
        'last_name': expected_m_last_name,
        'joined_at': expected_m_joined_at,
        'status': expected_m_status,
    }

    user_profile_2 = UserProfile()
    user_profile_2.id = expected_m_id

    user_9 = User()
    user_9.id = 9

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [user_profile_2, user_9]

    db_mock = mocker.patch('modules.user_profiles.routes_admin.db')
    db_mock.commit.return_value = None

    result = put_user_profile(expected_m_id)

    assert result[1] == expected_status
    assert 'user_profile' in result[0].json
    assert len(result[0].json['user_profile']) == expected_m_length
    assert result[0].json['user_profile']['id'] == expected_m_id
    assert result[0].json['user_profile']['user_id'] == expected_m_user_id
    assert result[0].json['user_profile']['first_name'] == \
        expected_m_first_name
    assert result[0].json['user_profile']['last_name'] == expected_m_last_name
    assert result[0].json['user_profile']['joined_at'] == expected_m_joined_at
    assert result[0].json['user_profile']['status'] == expected_m_status
    assert bool(re_datetime.match(
        result[0].json['user_profile']['status_changed_at']))
    assert result[0].json['user_profile']['created_at'] == \
        expected_m_created_at
    assert result[0].json['user_profile']['updated_at'] == \
        expected_m_updated_at


@pytest.mark.unit
def test_put_user_profile_required_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'user_id': ['Missing data for required field.'],
            'first_name': ['Missing data for required field.'],
            'foo': ['Unknown field.'],
            'joined_at': ['Missing data for required field.'],
            'last_name': ['Missing data for required field.'],
            'status': ['Missing data for required field.'],
        }
    }

    request_mock = mocker.patch('modules.user_profiles.routes_admin.request')
    request_mock.json = {'foo': "bar"}

    user_profile_2 = UserProfile()
    user_profile_2.id = 2

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.return_value = [user_profile_2, None]

    result = put_user_profile(2)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_put_user_profile_user_exists_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'user_id': ['Invalid value.']}}

    request_mock = mocker.patch('modules.user_profiles.routes_admin.request')
    request_mock.json = {
        'user_id': 250,
        'first_name': "LynneA",
        'last_name': "HarfordA",
        'joined_at': "2018-12-09T08:00:00+0000",
        'status': UserProfile.STATUS_DISABLED
    }

    user_profile_2 = UserProfile()
    user_profile_2.id = 2

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [user_profile_2, None]

    result = put_user_profile(2)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_put_user_profile_min_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'first_name': ["Value must be between 1 and 40 characters long."],
        'last_name': ["Value must be between 2 and 40 characters long."],
    }}

    request_mock = mocker.patch('modules.user_profiles.routes_admin.request')
    request_mock.json = {
        'user_id': 9,
        'first_name': "",
        'last_name': "H",
        'joined_at': "2018-12-09T08:00:00+0000",
        'status': UserProfile.STATUS_DISABLED
    }

    user_profile_2 = UserProfile()
    user_profile_2.id = 2

    user_9 = User()
    user_9.id = 9

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [user_profile_2, user_9]

    result = put_user_profile(2)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_put_user_profile_max_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'first_name': ["Value must be between 1 and 40 characters long."],
        'last_name': ["Value must be between 2 and 40 characters long."],
    }}

    request_mock = mocker.patch('modules.user_profiles.routes_admin.request')
    request_mock.json = {
        'user_id': 9,
        'first_name': "pSJxpg6GC2qRnekNVDKMkYqNqAbd7X5UzsKuhVzf4",
        'last_name': "J5ATwnHEfD5YqSQNTDcb9bFbaD6ZRZvL3b9ugjyUK",
        'joined_at': "2018-12-09T08:00:00+0000",
        'status': UserProfile.STATUS_DISABLED
    }

    user_profile_2 = UserProfile()
    user_profile_2.id = 2

    user_9 = User()
    user_9.id = 9

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [user_profile_2, user_9]

    result = put_user_profile(2)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_put_user_profile_type_fail(app, mocker):
    expected_status = 400
    expected_json = {
        "error": {
            'user_id': ['Not a valid integer.'],
            'first_name': ['Not a valid string.'],
            'joined_at': ['Not a valid datetime.'],
            'last_name': ['Not a valid string.'],
            'status': ['Not a valid integer.'],
        }
    }

    request_mock = mocker.patch('modules.user_profiles.routes_admin.request')
    request_mock.json = {
        'user_id': 'bad',
        'first_name': 123,
        'joined_at': 123,
        'last_name': 123,
        'status': "bad",
    }

    user_profile_2 = UserProfile()
    user_profile_2.id = 2

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query
    query_mock.return_value \
        .get.side_effect = [user_profile_2, None]

    result = put_user_profile(2)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_put_user_profile_route_ok(app, mocker, client):
    expected_status = 200
    expected_m_length = 9
    expected_m_id = 2
    expected_m_user_id = 9
    expected_m_first_name = "LynneA"
    expected_m_last_name = "HarfordA"
    expected_m_joined_at = "2018-12-09T08:00:00+0000"
    expected_m_status = UserProfile.STATUS_DISABLED
    expected_m_created_at = None
    expected_m_updated_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch('modules.user_profiles.routes_admin.request')
    request_mock.json = {
        'user_id': expected_m_user_id,
        'first_name': expected_m_first_name,
        'last_name': expected_m_last_name,
        'joined_at': expected_m_joined_at,
        'status': expected_m_status,
    }

    user_profile_2 = UserProfile()
    user_profile_2.id = expected_m_id

    user_9 = User()
    user_9.id = 9

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock initial resource query and exists() validation
    query_mock.return_value \
        .get.side_effect = [user_profile_2, user_9]

    db_mock = mocker.patch('modules.user_profiles.routes_admin.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    response = client.put("/user_profile/{}".format(expected_m_id))

    assert response.status_code == expected_status
    assert 'user_profile' in response.json
    assert len(response.json['user_profile']) == expected_m_length
    assert response.json['user_profile']['id'] == expected_m_id
    assert response.json['user_profile']['user_id'] == expected_m_user_id
    assert response.json['user_profile']['first_name'] == \
        expected_m_first_name
    assert response.json['user_profile']['last_name'] == expected_m_last_name
    assert response.json['user_profile']['joined_at'] == expected_m_joined_at
    assert response.json['user_profile']['status'] == expected_m_status
    assert bool(re_datetime.match(
        response.json['user_profile']['status_changed_at']))
    assert response.json['user_profile']['created_at'] == \
        expected_m_created_at
    assert response.json['user_profile']['updated_at'] == \
        expected_m_updated_at


@pytest.mark.unit
def test_delete_user_profile_ok(app, mocker):
    expected_status = 204
    expected_content = ''

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = UserProfile()

    db_mock = mocker.patch('modules.user_profiles.routes_admin.db')
    db_mock.commit.return_value = None

    result = delete_user_profile(7)

    assert result[1] == expected_status
    assert result[0] == expected_content


@pytest.mark.unit
def test_delete_user_fail(app, mocker):
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = None

    try:
        delete_user_profile(250)
        assert False
    except NotFound:
        assert True


# # INTEGRATION TESTS


@pytest.mark.integration
def test_get_user_profiles_route_with_data(client):
    expected_status = 200
    expected_json = {
        "limit": 10,
        "page": 1,
        "total": 6,
        "user_profiles": [
            {
                "created_at": "2018-12-01T00:00:00+0000",
                "first_name": "Fiona",
                "id": 1,
                "joined_at": "2018-12-03T00:00:00+0000",
                "last_name": "Farnham",
                "status": 1,
                "status_changed_at": "2018-12-04T00:00:00+0000",
                "updated_at": "2018-12-02T00:00:00+0000",
                "user_id": 1
            },
            {
                "created_at": "2018-12-05T00:00:00+0000",
                "first_name": "Lynne",
                "id": 2,
                "joined_at": "2018-12-07T00:00:00+0000",
                "last_name": "Harford",
                "status": 1,
                "status_changed_at": "2018-12-08T00:00:00+0000",
                "updated_at": "2018-12-06T00:00:00+0000",
                "user_id": 2
            },
            {
                "created_at": "2018-12-10T00:00:00+0000",
                "first_name": "Duane",
                "id": 3,
                "joined_at": "2018-12-12T00:00:00+0000",
                "last_name": "Hargrave",
                "status": 1,
                "status_changed_at": "2018-12-13T00:00:00+0000",
                "updated_at": "2018-12-11T00:00:00+0000",
                "user_id": 3
            },
            {
                "created_at": "2018-12-20T00:00:00+0000",
                "first_name": "Elroy",
                "id": 5,
                "joined_at": "2018-12-22T00:00:00+0000",
                "last_name": "Hunnicutt",
                "status": 2,
                "status_changed_at": "2018-12-23T00:00:00+0000",
                "updated_at": "2018-12-21T00:00:00+0000",
                "user_id": 5
            },
            {
                "created_at": "2018-12-25T00:00:00+0000",
                "first_name": "Alease",
                "id": 6,
                "joined_at": "2018-12-27T00:00:00+0000",
                "last_name": "Richards",
                "status": 5,
                "status_changed_at": "2018-12-28T00:00:00+0000",
                "updated_at": "2018-12-26T00:00:00+0000",
                "user_id": 6
            },
            {
                "created_at": "2019-01-05T00:00:00+0000",
                "first_name": "Luke",
                "id": 8,
                "joined_at": "2019-01-07T00:00:00+0000",
                "last_name": "Tennyson",
                "status": 1,
                "status_changed_at": "2019-01-08T00:00:00+0000",
                "updated_at": "2019-01-06T00:00:00+0000",
                "user_id": 8
            }
        ]
    }

    response = client.get("/user_profiles")

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.integration
def test_get_user_profile_2_route_with_data(client):
    expected_status = 200
    expected_json = {
        "user_profile": {
            "created_at": "2018-12-05T00:00:00+0000",
            "first_name": "Lynne",
            "id": 2,
            "joined_at": "2018-12-07T00:00:00+0000",
            "last_name": "Harford",
            "status": 1,
            "status_changed_at": "2018-12-08T00:00:00+0000",
            "updated_at": "2018-12-06T00:00:00+0000",
            "user_id": 2
        }
    }

    response = client.get("/user_profile/2")

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.integration
def test_post_user_profiles_route_with_data(client, mocker):
    expected_status = 201
    expected_m_length = 9
    expected_m_id = 9
    expected_m_user_id = 9
    expected_m_first_name = "Service"
    expected_m_last_name = "Account"
    expected_m_joined_at = "2019-02-04T00:00:00+0000"
    expected_m_status = UserProfile.STATUS_ENABLED
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}$")

    request_mock = mocker.patch('modules.user_profiles.routes_admin.request')
    request_mock.json = {
        'user_id': expected_m_user_id,
        'first_name': expected_m_first_name,
        'last_name': expected_m_last_name,
        'joined_at': expected_m_joined_at,
        'status': expected_m_status,
    }

    response = client.post("/user_profiles")

    assert response.status_code == expected_status
    assert 'user_profile' in response.json
    assert len(response.json['user_profile']) == expected_m_length
    assert response.json['user_profile']['id'] == expected_m_id
    assert response.json['user_profile']['user_id'] == expected_m_user_id
    assert response.json['user_profile']['first_name'] == \
        expected_m_first_name
    assert response.json['user_profile']['last_name'] == expected_m_last_name
    assert response.json['user_profile']['joined_at'] == expected_m_joined_at
    assert response.json['user_profile']['status'] == expected_m_status
    assert bool(re_datetime.match(
        response.json['user_profile']['status_changed_at']))
    assert bool(re_datetime.match(
        response.json['user_profile']['created_at']))
    assert bool(re_datetime.match(
        response.json['user_profile']['updated_at']))


@pytest.mark.integration
def test_put_user_profile_route_with_data(client, mocker):
    expected_status = 200
    expected_m_length = 9
    expected_m_id = 2
    expected_m_user_id = 9
    expected_m_first_name = "LynneA"
    expected_m_last_name = "HarfordA"
    expected_m_joined_at = "2018-12-09T08:00:00+0000"
    expected_m_status = UserProfile.STATUS_DISABLED
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}$")

    request_mock = mocker.patch('modules.user_profiles.routes_admin.request')
    request_mock.json = {
        'user_id': expected_m_user_id,
        'first_name': expected_m_first_name,
        'last_name': expected_m_last_name,
        'joined_at': expected_m_joined_at,
        'status': expected_m_status,
    }

    response = client.put("/user_profile/{}".format(expected_m_id))

    assert response.status_code == expected_status
    assert 'user_profile' in response.json
    assert len(response.json['user_profile']) == expected_m_length
    assert response.json['user_profile']['id'] == expected_m_id
    assert response.json['user_profile']['user_id'] == expected_m_user_id
    assert response.json['user_profile']['first_name'] == \
        expected_m_first_name
    assert response.json['user_profile']['last_name'] == expected_m_last_name
    assert response.json['user_profile']['joined_at'] == expected_m_joined_at
    assert response.json['user_profile']['status'] == expected_m_status
    assert bool(re_datetime.match(
        response.json['user_profile']['status_changed_at']))
    assert bool(re_datetime.match(
        response.json['user_profile']['created_at']))
    assert bool(re_datetime.match(
        response.json['user_profile']['updated_at']))


@pytest.mark.integration
def test_delete_user_profile_7_route_with_data(client):
    expected_status = 204
    expected_json = None

    response = client.delete("/user_profile/7")

    assert response.status_code == expected_status
    assert response.json == expected_json
