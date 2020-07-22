from copy import copy
import re
import base64

import pytest
from werkzeug.exceptions import NotFound, Unauthorized
from sqlalchemy.orm.exc import NoResultFound

from fixtures import Fixtures
from app import create_app
from config import Config
from modules.user_account.routes_public import post_user_account_step1, \
    post_user_account_step2, get_user_account, put_user_account, \
    delete_user_account, put_password, post_password_request_reset_code, \
    put_password_reset
from modules.users.model import User, UserTermsOfService, UserPasswordHistory
from modules.terms_of_services.model import TermsOfService
from modules.roles.model import Role
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
def test_post_user_account_step1_ok(app, mocker):
    expected_status = 201
    expected_m_length = 8
    expected_m_id = None
    expected_m_user_username = "user9"
    expected_m_user_email = "user9@test.com"
    expected_m_user_is_verified = False
    expected_m_user_first_name = None
    expected_m_user_last_name = None
    expected_m_user_joined_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        "username": expected_m_user_username,
        "email": expected_m_user_email,
        "password": "user9Pass",
        "password2": "user9Pass",
        "tos_id": 2
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock exists() validation
    query_mock.return_value \
        .get.return_value = TermsOfService()

    db_mock = mocker.patch('modules.user_account.routes_public.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    result = post_user_account_step1()

    assert result[1] == expected_status
    assert 'user_account' in result[0].json
    assert len(result[0].json['user_account']) == expected_m_length
    assert result[0].json['user_account']['id'] == expected_m_id
    assert result[0].json['user_account']['username'] == \
        expected_m_user_username
    assert result[0].json['user_account']['email'] == expected_m_user_email
    assert result[0].json['user_account']['is_verified'] == \
        expected_m_user_is_verified
    assert result[0].json['user_account']['first_name'] == \
        expected_m_user_first_name
    assert result[0].json['user_account']['last_name'] == \
        expected_m_user_last_name
    assert result[0].json['user_account']['joined_at'] == \
        expected_m_user_joined_at
    assert bool(re_datetime.match(
        result[0].json['user_account']['password_changed_at']))


@pytest.mark.unit
def test_post_user_account_step1_cap_username_ok(app, mocker):
    expected_status = 201
    expected_m_length = 8
    expected_m_id = None
    expected_m_user_username = "user9"
    expected_m_user_email = "user9@test.com"
    expected_m_user_is_verified = False
    expected_m_user_first_name = None
    expected_m_user_last_name = None
    expected_m_user_joined_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        "username": "User9",
        "email": expected_m_user_email,
        "password": "user9Pass",
        "password2": "user9Pass",
        "tos_id": 2
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock exists() validation
    query_mock.return_value \
        .get.return_value = TermsOfService()

    db_mock = mocker.patch('modules.user_account.routes_public.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    result = post_user_account_step1()

    assert result[1] == expected_status
    assert 'user_account' in result[0].json
    assert len(result[0].json['user_account']) == expected_m_length
    assert result[0].json['user_account']['id'] == expected_m_id
    assert result[0].json['user_account']['username'] == \
        expected_m_user_username
    assert result[0].json['user_account']['email'] == expected_m_user_email
    assert result[0].json['user_account']['is_verified'] == \
        expected_m_user_is_verified
    assert result[0].json['user_account']['first_name'] == \
        expected_m_user_first_name
    assert result[0].json['user_account']['last_name'] == \
        expected_m_user_last_name
    assert result[0].json['user_account']['joined_at'] == \
        expected_m_user_joined_at
    assert bool(re_datetime.match(
        result[0].json['user_account']['password_changed_at']))


@pytest.mark.unit
def test_post_user_account_step1_required_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'email': ['Missing data for required field.'],
            'foo': ['Unknown field.'],
            'password': ['Missing data for required field.'],
            'password2': ['Missing data for required field.'],
            'tos_id': ['Missing data for required field.'],
            'username': ['Missing data for required field.'],
        }
    }

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {'foo': "bar"}

    result = post_user_account_step1()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_user_account_step1_unique_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'username': ['Value must be unique.'],
        'email': ['Value must be unique.']}}

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        "username": "user1",
        "email": "user1@test.com",
        "password": "user9Pass",
        "password2": "user9Pass",
        "tos_id": 2
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = User()

    # mock exists() validation
    query_mock.return_value \
        .get.return_value = TermsOfService()

    result = post_user_account_step1()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_user_account_step1_tos_exists_password_match_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'tos_id': ['Invalid value.'],
        'password2': ['Passwords must match.'],
    }}

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        "username": "user9",
        "email": "user9@test.com",
        "password": "user9Pass",
        "password2": "user9Pass2",
        "tos_id": 250
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock exists() validation
    query_mock.return_value \
        .get.return_value = None

    result = post_user_account_step1()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_user_account_step1_min_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'username': ['Value must be between 2 and 40 characters long.']}}

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        "username": "u",
        "email": "user9@test.com",
        "password": "user9Pass",
        "password2": "user9Pass",
        "tos_id": 2
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock exists() validation
    query_mock.return_value \
        .get.return_value = TermsOfService()

    result = post_user_account_step1()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_user_account_step1_max_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'username': ['Value must be between 2 and 40 characters long.']}}

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        "username": "pf37Ebh9UKnqMbarsmjPgJS72HnQWmdnjK4Uh2DFW",
        "email": "user9@test.com",
        "password": "user9Pass",
        "password2": "user9Pass",
        "tos_id": 2
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock exists() validation
    query_mock.return_value \
        .get.return_value = TermsOfService()

    result = post_user_account_step1()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_user_account_step1_username_numeric_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'username': ['Value must not be a number.']}}

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        "username": "1234",
        "email": "user9@test.com",
        "password": "user9Pass",
        "password2": "user9Pass",
        "tos_id": 2
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock exists() validation
    query_mock.return_value \
        .get.return_value = TermsOfService()

    result = post_user_account_step1()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_user_account_step1_username_characters_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'username': ['Value must contain only alphanumeric characters and the underscore.']}}

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        "username": "user 9",
        "email": "user9@test.com",
        "password": "user9Pass",
        "password2": "user9Pass",
        "tos_id": 2
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock exists() validation
    query_mock.return_value \
        .get.return_value = TermsOfService()

    result = post_user_account_step1()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_user_account_step1_email_format_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'email': ['Not a valid email address.']}}

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        "username": "user9",
        "email": "user9test.com",
        "password": "user9Pass",
        "password2": "user9Pass",
        "tos_id": 2
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock exists() validation
    query_mock.return_value \
        .get.return_value = TermsOfService()

    result = post_user_account_step1()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_user_account_step1_password_complexity_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'password': ['Please choose a more complex password.']}}

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        "username": "user9",
        "email": "user9@test.com",
        "password": "password",
        "password2": "password",
        "tos_id": 2
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock exists() validation
    query_mock.return_value \
        .get.return_value = TermsOfService()

    result = post_user_account_step1()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_user_account_step1_type_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'email': ["Not a valid email address."],
            'password': ["Not a valid string."],
            'password2': ["Not a valid string."],
            'tos_id': ["Not a valid integer."],
            'username': ["Not a valid string."],
        }
    }

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        "username": 123,
        "email": 123,
        "password": 123,
        "password2": 123,
        "tos_id": "bad"
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock exists() validation
    query_mock.return_value \
        .get.return_value = None

    result = post_user_account_step1()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_user_account_step1_route_ok(app, mocker, client):
    expected_status = 201
    expected_m_length = 8
    expected_m_id = None
    expected_m_user_username = "user9"
    expected_m_user_email = "user9@test.com"
    expected_m_user_is_verified = False
    expected_m_user_first_name = None
    expected_m_user_last_name = None
    expected_m_user_joined_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        "username": expected_m_user_username,
        "email": expected_m_user_email,
        "password": "user9Pass",
        "password2": "user9Pass",
        "tos_id": 2
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    # mock exists() validation
    query_mock.return_value \
        .get.return_value = TermsOfService()

    db_mock = mocker.patch('modules.user_account.routes_public.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    response = client.post("/user_account/step1?app_key=123")

    assert response.status_code == expected_status
    assert 'user_account' in response.json
    assert len(response.json['user_account']) == expected_m_length
    assert response.json['user_account']['id'] == expected_m_id
    assert response.json['user_account']['username'] == \
        expected_m_user_username
    assert response.json['user_account']['email'] == expected_m_user_email
    assert response.json['user_account']['is_verified'] == \
        expected_m_user_is_verified
    assert response.json['user_account']['first_name'] == \
        expected_m_user_first_name
    assert response.json['user_account']['last_name'] == \
        expected_m_user_last_name
    assert response.json['user_account']['joined_at'] == \
        expected_m_user_joined_at
    assert bool(re_datetime.match(
        response.json['user_account']['password_changed_at']))


@pytest.mark.unit
def test_post_user_account_step1_route_no_app_key(app, mocker, client):
    expected_status = 401

    response = client.post("/user_account/step1")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
def test_post_user_account_step1_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.post("/user_account/step1?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
def test_post_user_account_step2_ok(app, mocker):
    expected_status = 201
    expected_m_length = 8
    expected_m_id = None
    expected_m_user_username = None
    expected_m_user_email = None
    expected_m_user_is_verified = None
    expected_m_user_password_changed_at = None
    expected_m_user_first_name = "Wilmer"
    expected_m_user_last_name = "Munson"
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        "first_name": expected_m_user_first_name,
        "last_name": expected_m_user_last_name,
    }

    db_mock = mocker.patch('modules.user_account.routes_public.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    g_mock = mocker.patch('modules.user_account.routes_public.g')
    g_mock.user = User()

    result = post_user_account_step2()

    assert result[1] == expected_status
    assert 'user_account' in result[0].json
    assert len(result[0].json['user_account']) == expected_m_length
    assert result[0].json['user_account']['id'] == expected_m_id
    assert result[0].json['user_account']['username'] == \
        expected_m_user_username
    assert result[0].json['user_account']['email'] == expected_m_user_email
    assert result[0].json['user_account']['is_verified'] == \
        expected_m_user_is_verified
    assert result[0].json['user_account']['first_name'] == \
        expected_m_user_first_name
    assert result[0].json['user_account']['last_name'] == \
        expected_m_user_last_name
    assert result[0].json['user_account']['password_changed_at'] == \
        expected_m_user_password_changed_at
    assert bool(re_datetime.match(
        result[0].json['user_account']['joined_at']))


@pytest.mark.unit
def test_post_user_account_step2_whitespace_ok(app, mocker):
    expected_status = 201
    expected_m_length = 8
    expected_m_id = None
    expected_m_user_username = None
    expected_m_user_email = None
    expected_m_user_is_verified = None
    expected_m_user_password_changed_at = None
    expected_m_user_first_name = "Wilmer"
    expected_m_user_last_name = "Munson"
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        "first_name": " Wilmer  ",
        "last_name": "   Munson ",
    }

    db_mock = mocker.patch('modules.user_account.routes_public.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    g_mock = mocker.patch('modules.user_account.routes_public.g')
    g_mock.user = User()

    result = post_user_account_step2()

    assert result[1] == expected_status
    assert 'user_account' in result[0].json
    assert len(result[0].json['user_account']) == expected_m_length
    assert result[0].json['user_account']['id'] == expected_m_id
    assert result[0].json['user_account']['username'] == \
        expected_m_user_username
    assert result[0].json['user_account']['email'] == expected_m_user_email
    assert result[0].json['user_account']['is_verified'] == \
        expected_m_user_is_verified
    assert result[0].json['user_account']['first_name'] == \
        expected_m_user_first_name
    assert result[0].json['user_account']['last_name'] == \
        expected_m_user_last_name
    assert result[0].json['user_account']['password_changed_at'] == \
        expected_m_user_password_changed_at
    assert bool(re_datetime.match(
        result[0].json['user_account']['joined_at']))


@pytest.mark.unit
def test_post_user_account_step2_required_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'first_name': ['Missing data for required field.'],
            'foo': ['Unknown field.'],
            'last_name': ['Missing data for required field.'],
        }
    }

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {'foo': "bar"}

    g_mock = mocker.patch('modules.user_account.routes_public.g')
    g_mock.user = User()

    result = post_user_account_step2()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_user_account_step2_min_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'first_name': ['Value must be between 1 and 40 characters long.'],
            'last_name': ['Value must be between 2 and 40 characters long.'],
        }
    }

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        "first_name": "",
        "last_name": "M",
    }

    g_mock = mocker.patch('modules.user_account.routes_public.g')
    g_mock.user = User()

    result = post_user_account_step2()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_user_account_step2_max_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'first_name': ['Value must be between 1 and 40 characters long.'],
            'last_name': ['Value must be between 2 and 40 characters long.'],
        }
    }

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        "first_name": "q5yCBGAspqgkJPx8fNsaVsDRhJCyRuS3xr2pf87bn",
        "last_name": "2mLdFUz8GLBTraGw756k4JzCxBhNuSWbGRJZTB9cR",
    }

    g_mock = mocker.patch('modules.user_account.routes_public.g')
    g_mock.user = User()

    result = post_user_account_step2()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_user_account_step2_type_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'first_name': ['Not a valid string.'],
            'last_name': ['Not a valid string.'],
        }
    }

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        "first_name": 123,
        "last_name": 123,
    }

    g_mock = mocker.patch('modules.user_account.routes_public.g')
    g_mock.user = User()

    result = post_user_account_step2()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_post_user_account_step2_route_ok(app, mocker, client):
    expected_status = 201
    expected_m_length = 8
    expected_m_id = None
    expected_m_user_username = None
    expected_m_user_email = None
    expected_m_user_is_verified = None
    expected_m_user_password_changed_at = None
    expected_m_user_first_name = "Wilmer"
    expected_m_user_last_name = "Munson"
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        "first_name": expected_m_user_first_name,
        "last_name": expected_m_user_last_name,
    }

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login db query
    role1 = Role()
    role1.id = 1
    role1.name = 'USER'
    role1.password_reset_days = 365

    user2 = User()
    user2.id = 2
    user2.password = 'user2pass'
    user2.roles = [role1]

    query_mock.return_value \
        .filter.return_value \
        .first.return_value = user2

    auth_db_mock = mocker.patch('modules.users.authentication.db')
    auth_db_mock.add.return_value = None
    auth_db_mock.commit.return_value = None

    db_mock = mocker.patch('modules.user_account.routes_public.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    g_mock = mocker.patch('modules.user_account.routes_public.g')
    g_mock.user = User()

    # mock user login
    auth_mock = mocker.patch('modules.users.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'user2:user2pass'.encode('ascii')).decode('utf-8')

    response = client.post(
        "/user_account/step2?app_key=123",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert 'user_account' in response.json
    assert len(response.json['user_account']) == expected_m_length
    assert response.json['user_account']['id'] == expected_m_id
    assert response.json['user_account']['username'] == \
        expected_m_user_username
    assert response.json['user_account']['email'] == expected_m_user_email
    assert response.json['user_account']['is_verified'] == \
        expected_m_user_is_verified
    assert response.json['user_account']['first_name'] == \
        expected_m_user_first_name
    assert response.json['user_account']['last_name'] == \
        expected_m_user_last_name
    assert response.json['user_account']['password_changed_at'] == \
        expected_m_user_password_changed_at
    assert bool(re_datetime.match(
        response.json['user_account']['joined_at']))


@pytest.mark.unit
def test_post_user_account_step2_route_no_app_key(app, mocker, client):
    expected_status = 401

    response = client.post("/user_account/step2")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
def test_post_user_account_step2_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.post("/user_account/step2?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
def test_post_user_account_step2_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.users.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.post("/user_account/step2?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
def test_get_user_account_ok(app, mocker):
    expected_status = 200
    expected_json = {
        'email': None,
        'first_name': None,
        'id': None,
        'is_verified': None,
        'joined_at': None,
        'last_name': None,
        'password_changed_at': None,
        'username': None,
    }

    g_mock = mocker.patch('modules.user_account.routes_public.g')
    g_mock.user = User()

    result = get_user_account()

    assert result[1] == expected_status
    assert result[0].json['user_account'] == expected_json


@pytest.mark.unit
def test_get_user_account_route_ok(app, mocker, client):
    expected_status = 200

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login db query
    role1 = Role()
    role1.id = 1
    role1.name = 'USER'
    role1.password_reset_days = 365

    user2 = User()
    user2.id = 2
    user2.password = 'user2pass'
    user2.roles = [role1]

    query_mock.return_value \
        .filter.return_value \
        .first.return_value = user2

    db_mock = mocker.patch('modules.users.authentication.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    # mock user login
    auth_mock = mocker.patch('modules.users.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'user2:user2pass'.encode('ascii')).decode('utf-8')

    response = client.get(
        "/user_account?app_key=123",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert 'user_account' in response.json


@pytest.mark.unit
def test_get_user_account_route_no_app_key(app, client):
    expected_status = 401

    response = client.get("/user_account")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
def test_get_user_account_route_bad_app_key(app, mocker, client):
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
def test_get_user_account_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.users.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.get("/user_account?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
def test_put_user_account_ok(app, mocker):
    expected_status = 200
    expected_m_length = 8
    expected_m_id = None
    expected_m_user_username = "user9"
    expected_m_user_email = "user9@test.com"
    expected_m_user_is_verified = None
    expected_m_user_first_name = "Wilmer"
    expected_m_user_last_name = "Munson"
    expected_m_user_password_changed_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        "username": expected_m_user_username,
        "email": expected_m_user_email,
        "first_name": expected_m_user_first_name,
        "last_name": expected_m_user_last_name,
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    db_mock = mocker.patch('modules.user_account.routes_public.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    g_mock = mocker.patch('modules.user_account.routes_public.g')
    g_mock.user = User()

    result = put_user_account()

    assert result[1] == expected_status
    assert 'user_account' in result[0].json
    assert len(result[0].json['user_account']) == expected_m_length
    assert result[0].json['user_account']['id'] == expected_m_id
    assert result[0].json['user_account']['username'] == \
        expected_m_user_username
    assert result[0].json['user_account']['email'] == expected_m_user_email
    assert result[0].json['user_account']['is_verified'] == \
        expected_m_user_is_verified
    assert result[0].json['user_account']['first_name'] == \
        expected_m_user_first_name
    assert result[0].json['user_account']['last_name'] == \
        expected_m_user_last_name
    assert result[0].json['user_account']['password_changed_at'] == \
        expected_m_user_password_changed_at
    assert bool(re_datetime.match(
        result[0].json['user_account']['joined_at']))


@pytest.mark.unit
def test_put_user_account_cap_username_ok(app, mocker):
    expected_status = 200
    expected_m_length = 8
    expected_m_id = None
    expected_m_user_username = "user9"
    expected_m_user_email = "user9@test.com"
    expected_m_user_is_verified = None
    expected_m_user_first_name = "Wilmer"
    expected_m_user_last_name = "Munson"
    expected_m_user_password_changed_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        "username": "User9",
        "email": expected_m_user_email,
        "first_name": expected_m_user_first_name,
        "last_name": expected_m_user_last_name,
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    db_mock = mocker.patch('modules.user_account.routes_public.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    g_mock = mocker.patch('modules.user_account.routes_public.g')
    g_mock.user = User()

    result = put_user_account()

    assert result[1] == expected_status
    assert 'user_account' in result[0].json
    assert len(result[0].json['user_account']) == expected_m_length
    assert result[0].json['user_account']['id'] == expected_m_id
    assert result[0].json['user_account']['username'] == \
        expected_m_user_username
    assert result[0].json['user_account']['email'] == expected_m_user_email
    assert result[0].json['user_account']['is_verified'] == \
        expected_m_user_is_verified
    assert result[0].json['user_account']['first_name'] == \
        expected_m_user_first_name
    assert result[0].json['user_account']['last_name'] == \
        expected_m_user_last_name
    assert result[0].json['user_account']['password_changed_at'] == \
        expected_m_user_password_changed_at
    assert bool(re_datetime.match(
        result[0].json['user_account']['joined_at']))


@pytest.mark.unit
def test_put_user_account_required_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'email': ['Missing data for required field.'],
            'first_name': ['Missing data for required field.'],
            'foo': ['Unknown field.'],
            'last_name': ['Missing data for required field.'],
            'username': ['Missing data for required field.'],
        }
    }

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {'foo': "bar"}

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    g_mock = mocker.patch('modules.user_account.routes_public.g')
    g_mock.user = User()

    result = put_user_account()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_put_user_account_unique_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'username': ['Value must be unique.'],
        'email': ['Value must be unique.']}}

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        "username": "user1",
        "email": "user1@test.com",
        "first_name": "Wilmer",
        "last_name": "Munson",
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = User()

    g_mock = mocker.patch('modules.user_account.routes_public.g')
    g_mock.user = User()

    result = put_user_account()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_put_user_account_min_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'first_name': ['Value must be between 1 and 40 characters long.'],
        'last_name': ['Value must be between 2 and 40 characters long.'],
        'username': ['Value must be between 2 and 40 characters long.'],
    }}

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        "username": "u",
        "email": "user9@test.com",
        "first_name": "",
        "last_name": "M",
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    g_mock = mocker.patch('modules.user_account.routes_public.g')
    g_mock.user = User()

    result = put_user_account()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_put_user_account_max_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'first_name': ['Value must be between 1 and 40 characters long.'],
        'last_name': ['Value must be between 2 and 40 characters long.'],
        'username': ['Value must be between 2 and 40 characters long.'],
    }}

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        "username": "ZSnrETVjjXdkqqYaxG5ePKh68nRT8rzcNWYfCLnV4",
        "email": "user9@test.com",
        "first_name": "DFaAUB2kKa7CxS7wZBqGMNtvseM8Uyjnpn2Met9DG",
        "last_name": "9PEAgwuDPsGvNDEW7b3Tf2UZdWZnJ3fPv8HGuZFdy",
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    g_mock = mocker.patch('modules.user_account.routes_public.g')
    g_mock.user = User()

    result = put_user_account()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_put_user_account_username_numeric_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'username': ['Value must not be a number.']}}

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        "username": "1234",
        "email": "user9@test.com",
        "first_name": "Wilmer",
        "last_name": "Munson",
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    g_mock = mocker.patch('modules.user_account.routes_public.g')
    g_mock.user = User()

    result = put_user_account()

    assert result[1] == expected_status
    assert result[0].json == expected_json



@pytest.mark.unit
def test_put_user_account_username_character_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'username': ['Value must contain only alphanumeric characters and the underscore.']}}

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        "username": "user 9",
        "email": "user9@test.com",
        "first_name": "Wilmer",
        "last_name": "Munson",
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    g_mock = mocker.patch('modules.user_account.routes_public.g')
    g_mock.user = User()

    result = put_user_account()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_put_user_account_type_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'email': ["Not a valid email address."],
            'first_name': ["Not a valid string."],
            'last_name': ["Not a valid string."],
            'username': ["Not a valid string."],
        }
    }

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        "username": 123,
        "email": 123,
        "first_name": 123,
        "last_name": 123,
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock unique(), unique() email validation
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    g_mock = mocker.patch('modules.user_account.routes_public.g')
    g_mock.user = User()

    result = put_user_account()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_put_user_account_route_ok(app, mocker, client):
    expected_status = 200
    expected_m_length = 8
    expected_m_id = None
    expected_m_user_username = "user9"
    expected_m_user_email = "user9@test.com"
    expected_m_user_is_verified = None
    expected_m_user_first_name = "Wilmer"
    expected_m_user_last_name = "Munson"
    expected_m_user_password_changed_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    data = {
        "username": expected_m_user_username,
        "email": expected_m_user_email,
        "first_name": expected_m_user_first_name,
        "last_name": expected_m_user_last_name,
    }

    g_mock = mocker.patch('modules.user_account.routes_public.g')
    g_mock.user = User()

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login db query
    role1 = Role()
    role1.id = 1
    role1.name = 'USER'
    role1.password_reset_days = 365

    user2 = User()
    user2.id = 2
    user2.password = 'user2pass'
    user2.roles = [role1]

    db_mock = mocker.patch('modules.users.authentication.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    # mock login user, unique(), unique_email() validation
    query_mock.return_value \
        .filter.return_value \
        .first.side_effect = [user2, None, None]

    db_mock = mocker.patch('modules.user_account.routes_public.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    # mock user login
    auth_mock = mocker.patch('modules.users.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'user2:user2pass'.encode('ascii')).decode('utf-8')

    response = client.put("/user_account?app_key=123", json=data,
                          headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert 'user_account' in response.json
    assert len(response.json['user_account']) == expected_m_length
    assert response.json['user_account']['id'] == expected_m_id
    assert response.json['user_account']['username'] == \
        expected_m_user_username
    assert response.json['user_account']['email'] == expected_m_user_email
    assert response.json['user_account']['is_verified'] == \
        expected_m_user_is_verified
    assert response.json['user_account']['first_name'] == \
        expected_m_user_first_name
    assert response.json['user_account']['last_name'] == \
        expected_m_user_last_name
    assert response.json['user_account']['password_changed_at'] == \
        expected_m_user_password_changed_at
    assert bool(re_datetime.match(
        response.json['user_account']['joined_at']))


@pytest.mark.unit
def test_put_user_account_route_no_app_key(app, client):
    expected_status = 401

    response = client.put("/user_account")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
def test_put_user_account_route_bad_app_key(app, mocker, client):
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
def test_put_user_account_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.users.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.put("/user_account?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
def test_delete_user_account_ok(app, mocker):
    expected_status = 204
    expected_content = ''

    g_mock = mocker.patch('modules.user_account.routes_public.g')
    g_mock.user = User()

    db_mock = mocker.patch('modules.user_account.routes_public.db')
    db_mock.commit.return_value = None

    result = delete_user_account()

    assert result[1] == expected_status
    assert result[0] == expected_content


@pytest.mark.unit
def test_delete_user_account_route_ok(app, mocker, client):
    expected_status = 204
    expected_json = None

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login db query
    role1 = Role()
    role1.id = 1
    role1.name = 'USER'
    role1.password_reset_days = 365

    user2 = User()
    user2.id = 2
    user2.password = 'user2pass'
    user2.roles = [role1]

    query_mock.return_value \
        .filter.return_value \
        .first.return_value = user2

    db_mock = mocker.patch('modules.users.authentication.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    db_mock = mocker.patch('modules.user_account.routes_public.db')
    db_mock.commit.return_value = None

    # mock user login
    auth_mock = mocker.patch('modules.users.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'user2:user2pass'.encode('ascii')).decode('utf-8')

    response = client.delete(
        "/user_account?app_key=123",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.unit
def test_delete_user_account_route_no_app_key(app, client):
    expected_status = 401

    response = client.delete("/user_account")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
def test_delete_user_account_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.delete("/user_account?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
def test_delete_user_account_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.users.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.delete("/user_account?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
def test_put_password_ok(app, mocker):
    expected_status = 200
    expected_m_json = {'success': 'true'}

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        'previous_password': "user2pass",
        'password1': "user2Pass2",
        'password2': "user2Pass2",
    }

    role = Role()
    role.password_policy = True
    role.password_reuse_history = 10

    user2 = User()
    user2.password = "user2pass"
    user2.roles = [role]

    g_mock = mocker.patch('modules.user_account.routes_public.g')
    g_mock.user = user2

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    pw_history1 = UserPasswordHistory()
    pw_history1.password = "$2b$04$CgyaUQX08T5ntiGMD7GRDeLqknLxn/QoC0z7x/Ks8JG8lDrMVL.Xm"

    # mock password history
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .__iter__.return_value = [pw_history1]

    db_mock = mocker.patch('modules.user_account.routes_public.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    result = put_password()

    assert result[1] == expected_status
    assert result[0].json == expected_m_json


@pytest.mark.unit
def test_put_password_required_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'password1': ['Missing data for required field.'],
            'password2': ['Missing data for required field.'],
            'previous_password': ['Missing data for required field.'],
        }
    }

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {'foo': "bar"}

    g_mock = mocker.patch('modules.user_account.routes_public.g')
    g_mock.user = User()

    result = put_password()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_put_password_previous_password_incorrect_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'previous_password': ['Incorrect password.']}}

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        'previous_password': "bad_pass",
        'password1': "user2Pass2",
        'password2': "user2Pass2",
    }

    user2 = User()
    user2.password = "user2pass"

    g_mock = mocker.patch('modules.user_account.routes_public.g')
    g_mock.user = user2

    result = put_password()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_put_password_password1_complexity_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'password1': ['Please choose a more complex password.']}}

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        'previous_password': "user2pass",
        'password1': "password",
        'password2': "password",
    }

    user2 = User()
    user2.password = "user2pass"

    g_mock = mocker.patch('modules.user_account.routes_public.g')
    g_mock.user = user2

    result = put_password()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_put_password_password2_match_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'password2': ['New passwords must match.']}}

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        'previous_password': "user2pass",
        'password1': "user2Pass2",
        'password2': "user2Pass3",
    }

    user2 = User()
    user2.password = "user2pass"

    g_mock = mocker.patch('modules.user_account.routes_public.g')
    g_mock.user = user2

    result = put_password()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_put_password_password_history_reuse_fail(app, mocker):
    expected_status = 400
    expected_json = {'error': {
        'password1': ['This password has recently been used.']}}

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        'previous_password': "user2pass",
        'password1': "user2Pass2",
        'password2': "user2Pass2",
    }

    role = Role()
    role.password_policy = True
    role.password_reuse_history = 10

    user2 = User()
    user2.password = "user2pass"
    user2.roles = [role]

    g_mock = mocker.patch('modules.user_account.routes_public.g')
    g_mock.user = user2

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    pw_history1 = UserPasswordHistory()
    pw_history1.password = "$2b$04$Mf9/Xlftvv0NVHJpXseo2u9z7cL.jnIycojralfDRAtHfqZOIS1xm"

    # mock password history
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .__iter__.return_value = [pw_history1]

    db_mock = mocker.patch('modules.user_account.routes_public.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    result = put_password()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
def test_put_password_route_ok(app, mocker, client):
    expected_status = 200
    expected_m_json = {'success': 'true'}

    data = {
        'previous_password': "user2pass",
        'password1': "user2Pass2",
        'password2': "user2Pass2",
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    role1 = Role()
    role1.id = 1
    role1.name = 'USER'
    role1.password_reset_days = 365
    role1.password_policy = True
    role1.password_reuse_history = 10

    user2 = User()
    user2.password = "user2pass"
    user2.roles = [role1]

    # mock user login db query
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = user2

    db_mock = mocker.patch('modules.users.authentication.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    g_mock = mocker.patch('modules.user_account.routes_public.g')
    g_mock.user = user2

    pw_history1 = UserPasswordHistory()
    pw_history1.password = "$2b$04$CgyaUQX08T5ntiGMD7GRDeLqknLxn/QoC0z7x/Ks8JG8lDrMVL.Xm"

    # mock password history
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .__iter__.return_value = [pw_history1]

    db_mock = mocker.patch('modules.user_account.routes_public.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    # mock user login
    auth_mock = mocker.patch('modules.users.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'user2:user2pass'.encode('ascii')).decode('utf-8')

    response = client.put("/user_account/password?app_key=123", json=data,
                          headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status

    assert response.status_code == expected_status
    assert response.json == expected_m_json


@pytest.mark.unit
def test_put_password_route_no_app_key(app, client):
    expected_status = 401

    response = client.put("/user_account/password")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
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
def test_put_password_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.users.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.put("/user_account/password?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
def test_post_password_request_reset_code_ok(app, mocker):
    expected_status = 201
    expected_m_json = {'success': 'true', 'sent': 1}

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        'email': "user2@test.com",
    }

    user2 = User()
    user2.id = 2

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock user from email
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = user2

    db_mock = mocker.patch('modules.user_account.routes_public.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    notify_mock = mocker.patch('modules.user_account.routes_public.Notify')
    notify_mock.return_value.send.return_value = 1

    result = post_password_request_reset_code()

    assert result[1] == expected_status
    assert result[0].json == expected_m_json


@pytest.mark.unit
def test_post_password_request_reset_code_required_fail(app, mocker):
    expected_status = 400
    expected_m_json = {'error': {
        'email': ["Missing data for required field."]
    }}

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        'foo': "bar",
    }

    result = post_password_request_reset_code()

    assert result[1] == expected_status
    assert result[0].json == expected_m_json


@pytest.mark.unit
def test_post_password_request_reset_code_not_found_fail(app, mocker):
    expected_status = 400
    expected_m_json = {'error': {
        'email': ["Email address not found."]
    }}

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        'email': "someaddress@test.com",
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock user from email
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = post_password_request_reset_code()

    assert result[1] == expected_status
    assert result[0].json == expected_m_json


@pytest.mark.unit
def test_post_password_request_reset_code_route_ok(app, mocker, client):
    expected_status = 201
    expected_m_json = {'success': 'true', 'sent': 1}

    data = {
        'email': "user2@test.com",
    }

    user2 = User()
    user2.id = 2

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock user from email
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = user2

    db_mock = mocker.patch('modules.user_account.routes_public.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    notify_mock = mocker.patch('modules.user_account.routes_public.Notify')
    notify_mock.return_value.send.return_value = 1

    response = client.post("/password/request-reset-code?app_key=123",
                           json=data)

    assert response.status_code == expected_status
    assert response.json == expected_m_json


@pytest.mark.unit
def test_post_password_request_reset_code_route_no_app_key(app, client):
    expected_status = 401

    response = client.post("/password/request-reset-code")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
def test_post_password_request_reset_code_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.post("/password/request-reset-code?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
def test_put_password_reset_ok(app, mocker):
    expected_status = 200
    expected_m_json = {'success': 'true'}

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        'code': "123ABC",
        'email': "user2@test.com",
        'password1': "newPass1",
        'password2': "newPass1",
    }

    user2 = User()
    user2.id = 2

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock user from email
    query_mock.return_value \
        .filter.return_value \
        .first.side_effect = [user2, PasswordReset()]

    db_mock = mocker.patch('modules.user_account.routes_public.db')
    db_mock.commit.return_value = None

    result = put_password_reset()

    assert result[1] == expected_status
    assert result[0].json == expected_m_json


@pytest.mark.unit
def test_put_password_reset_required_fail(app, mocker):
    expected_status = 400
    expected_m_json = {'error': {
        'code': ["Missing data for required field."],
        'email': ["Missing data for required field."],
        'password1': ["Missing data for required field."],
        'password2': ["Missing data for required field."],
    }}

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        'foo': "bar",
    }

    result = put_password_reset()

    assert result[1] == expected_status
    assert result[0].json == expected_m_json


@pytest.mark.unit
def test_put_password_reset_email_not_found_fail(app, mocker):
    expected_status = 400
    expected_m_json = {'error': {
        'email': ["Email address not found."],
    }}

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        'code': "123ABC",
        'email': "someaddress@test.com",
        'password1': "newPass1",
        'password2': "newPass1",
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock user from email
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    result = put_password_reset()

    assert result[1] == expected_status
    assert result[0].json == expected_m_json


@pytest.mark.unit
def test_put_password_reset_code_not_found_fail(app, mocker):
    expected_status = 400
    expected_m_json = {'error': {
        'code': ["Invalid reset code."],
    }}

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        'code': "BADCODE",
        'email': "user2@test.com",
        'password1': "newPass1",
        'password2': "newPass1",
    }

    user2 = User()
    user2.id = 2

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock user from email
    query_mock.return_value \
        .filter.return_value \
        .first.side_effect = [user2, None]

    result = put_password_reset()

    assert result[1] == expected_status
    assert result[0].json == expected_m_json


@pytest.mark.unit
def test_put_password_reset_password_complexity_fail(app, mocker):
    expected_status = 400
    expected_m_json = {'error': {
        'password1': ["Please choose a more complex password."],
    }}

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        'code': "ABC123",
        'email': "user2@test.com",
        'password1': "password",
        'password2': "password",
    }

    user2 = User()
    user2.id = 2

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock user from email
    query_mock.return_value \
        .filter.return_value \
        .first.side_effect = [user2, PasswordReset()]

    result = put_password_reset()

    assert result[1] == expected_status
    assert result[0].json == expected_m_json


@pytest.mark.unit
def test_put_password_reset_password_match_fail(app, mocker):
    expected_status = 400
    expected_m_json = {'error': {
        'password2': ["New passwords must match."],
    }}

    request_mock = mocker.patch('modules.user_account.routes_public.request')
    request_mock.json = {
        'code': "ABC123",
        'email': "user2@test.com",
        'password1': "newPass1",
        'password2': "newPass2",
    }

    user2 = User()
    user2.id = 2

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock user from email
    query_mock.return_value \
        .filter.return_value \
        .first.side_effect = [user2, PasswordReset()]

    result = put_password_reset()

    assert result[1] == expected_status
    assert result[0].json == expected_m_json


@pytest.mark.unit
def test_put_password_reset_route_ok(app, mocker, client):
    expected_status = 200
    expected_m_json = {'success': 'true'}

    data = {
        'code': "123ABC",
        'email': "user2@test.com",
        'password1': "newPass1",
        'password2': "newPass1",
    }

    user2 = User()
    user2.id = 2

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock user from email
    query_mock.return_value \
        .filter.return_value \
        .first.side_effect = [user2, PasswordReset()]

    db_mock = mocker.patch('modules.user_account.routes_public.db')
    db_mock.commit.return_value = None

    response = client.put("/password/reset?app_key=123", json=data)

    assert response.status_code == expected_status
    assert response.json == expected_m_json


@pytest.mark.unit
def test_put_password_reset_route_no_app_key(app, client):
    expected_status = 401

    response = client.put("/password/reset")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
def test_put_password_reset_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.put("/password/reset?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


# INTEGRATION TESTS


@pytest.mark.integration
def test_post_user_account_step1_route_with_data(client, mocker):
    expected_status = 201
    expected_m_length = 8
    expected_m_id = 10
    expected_m_user_username = "user9"
    expected_m_user_email = "user9@test.com"
    expected_m_user_is_verified = False
    expected_m_user_first_name = None
    expected_m_user_last_name = None
    expected_m_user_joined_at = None
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}$")

    request_environ_mock = mocker.patch(
        'modules.user_account.routes_public.request.environ')
    request_environ_mock.return_value = {
        'HTTP_X_REAL_IP': '1.1.1.1'
    }

    data = {
        "username": expected_m_user_username,
        "email": expected_m_user_email,
        "password": "user9Pass",
        "password2": "user9Pass",
        "tos_id": 2
    }

    response = client.post(
        "/user_account/step1?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        json=data)

    assert response.status_code == expected_status
    assert 'user_account' in response.json
    assert len(response.json['user_account']) == expected_m_length
    assert response.json['user_account']['id'] == expected_m_id
    assert response.json['user_account']['username'] == \
        expected_m_user_username
    assert response.json['user_account']['email'] == expected_m_user_email
    assert response.json['user_account']['is_verified'] == \
        expected_m_user_is_verified
    assert response.json['user_account']['first_name'] == \
        expected_m_user_first_name
    assert response.json['user_account']['last_name'] == \
        expected_m_user_last_name
    assert response.json['user_account']['joined_at'] == \
        expected_m_user_joined_at
    assert bool(re_datetime.match(
        response.json['user_account']['password_changed_at']))


@pytest.mark.integration
def test_post_user_account_step2_route_with_data(client, mocker):
    expected_status = 201
    expected_m_length = 8
    expected_m_id = 10
    expected_m_user_username = "user9"
    expected_m_user_email = "user9@test.com"
    expected_m_user_is_verified = False
    expected_m_user_first_name = "Wilmer"
    expected_m_user_last_name = "Munson"
    expected_m_user_joined_at = None
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}$")

    request_environ_mock = mocker.patch(
        'modules.user_account.routes_public.request.environ')
    request_environ_mock.return_value = {
        'HTTP_X_REAL_IP': '1.1.1.1'
    }

    data1 = {
        "username": expected_m_user_username,
        "email": expected_m_user_email,
        "password": "user9Pass",
        "password2": "user9Pass",
        "tos_id": 2
    }
    client.post(
        "/user_account/step1?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        json=data1)

    credentials = base64.b64encode(
        'user9:user9Pass'.encode('ascii')).decode('utf-8')

    data2 = {
        "first_name": expected_m_user_first_name,
        "last_name": expected_m_user_last_name,
    }
    response = client.post(
        "/user_account/step2?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        json=data2, headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert 'user_account' in response.json
    assert len(response.json['user_account']) == expected_m_length
    assert response.json['user_account']['id'] == expected_m_id
    assert response.json['user_account']['username'] == \
        expected_m_user_username
    assert response.json['user_account']['email'] == expected_m_user_email
    assert response.json['user_account']['is_verified'] == \
        expected_m_user_is_verified
    assert response.json['user_account']['first_name'] == \
        expected_m_user_first_name
    assert response.json['user_account']['last_name'] == \
        expected_m_user_last_name
    assert bool(re_datetime.match(
        response.json['user_account']['joined_at']))
    assert bool(re_datetime.match(
        response.json['user_account']['password_changed_at']))


@pytest.mark.integration
def test_get_user_account_route_with_data(client):
    expected_status = 200
    expected_json = {
        "user_account": {
            "email": "user2@test.com",
            "first_name": "Lynne",
            "id": 2,
            "is_verified": True,
            "joined_at": "2018-12-07T00:00:00+0000",
            "last_name": "Harford",
            "password_changed_at": None,
            "username": "user2"
        }
    }
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}$")

    credentials = base64.b64encode(
        'user2:user2pass'.encode('ascii')).decode('utf-8')

    response = client.get(
        "/user_account?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json['user_account']['email'] == \
        expected_json['user_account']['email']
    assert response.json['user_account']['first_name'] == \
        expected_json['user_account']['first_name']
    assert response.json['user_account']['id'] == \
        expected_json['user_account']['id']
    assert response.json['user_account']['is_verified'] == \
        expected_json['user_account']['is_verified']
    assert response.json['user_account']['joined_at'] == \
        expected_json['user_account']['joined_at']
    assert response.json['user_account']['last_name'] == \
        expected_json['user_account']['last_name']
    assert response.json['user_account']['username'] == \
        expected_json['user_account']['username']
    assert bool(re_datetime.match(
        response.json['user_account']['password_changed_at']))


@pytest.mark.integration
def test_put_user_account_route_with_data(client, mocker):
    expected_status = 200
    expected_m_length = 8
    expected_m_id = 2
    expected_m_user_username = "user2a"
    expected_m_user_email = "user2a@test.com"
    expected_m_user_is_verified = True
    expected_m_user_first_name = "Lynn"
    expected_m_user_last_name = "Harfourd"
    expected_m_user_joined_at = "2018-12-07T00:00:00+0000"
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}$")

    data = {
        "username": expected_m_user_username,
        "email": expected_m_user_email,
        "first_name": expected_m_user_first_name,
        "last_name": expected_m_user_last_name,
    }

    credentials = base64.b64encode(
        'user2:user2pass'.encode('ascii')).decode('utf-8')

    response = client.put(
        "/user_account?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        json=data, headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert 'user_account' in response.json
    assert len(response.json['user_account']) == expected_m_length
    assert response.json['user_account']['id'] == expected_m_id
    assert response.json['user_account']['username'] == \
        expected_m_user_username
    assert response.json['user_account']['email'] == expected_m_user_email
    assert response.json['user_account']['is_verified'] == \
        expected_m_user_is_verified
    assert response.json['user_account']['first_name'] == \
        expected_m_user_first_name
    assert response.json['user_account']['last_name'] == \
        expected_m_user_last_name
    assert response.json['user_account']['joined_at'] == \
        expected_m_user_joined_at
    assert bool(re_datetime.match(
        response.json['user_account']['password_changed_at']))


@pytest.mark.integration
def test_delete_user_account_route_with_data(client):
    expected_status = 204
    expected_json = None

    credentials = base64.b64encode(
        'user2:user2pass'.encode('ascii')).decode('utf-8')

    response = client.delete(
        "/user_account?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.integration
def test_put_password_route_with_data(client, mocker):
    expected_status = 200
    expected_m_json = {'success': 'true'}

    data = {
        'previous_password': "user2pass",
        'password1': "user2Pass2",
        'password2': "user2Pass2",
    }

    credentials = base64.b64encode(
        'user2:user2pass'.encode('ascii')).decode('utf-8')

    response = client.put(
        "/user_account/password?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        json=data,
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_m_json


@pytest.mark.integration
def test_post_password_request_reset_code_route_with_data(app, mocker, client):
    expected_status = 201
    expected_m_json = {'success': 'true', 'sent': 1}

    data = {
        'email': "user2@test.com",
    }

    notify_mock = mocker.patch('modules.user_account.routes_public.Notify')
    notify_mock.return_value.send.return_value = 1

    response = client.post(
        "/password/request-reset-code?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        json=data)

    assert response.status_code == expected_status
    assert response.json == expected_m_json


@pytest.mark.integration
def test_put_password_reset_route_with_data(app, mocker, client):
    expected_status = 200
    expected_m_json = {'success': 'true'}

    data = {
        'code': "J91NP0",
        'email': "user2@test.com",
        'password1': "user2PassR3s3t",
        'password2': "user2PassR3s3t",
    }

    response = client.put(
        "/password/reset?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        json=data)

    assert response.status_code == expected_status
    assert response.json == expected_m_json
