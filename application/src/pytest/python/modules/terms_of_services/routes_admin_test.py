from copy import copy
import re
import base64

import pytest
from werkzeug.exceptions import NotFound, Unauthorized
from sqlalchemy.orm.exc import NoResultFound

from fixtures import Fixtures
from app import create_app
from config import Config
from modules.terms_of_services.routes_admin import get_terms_of_services, \
    post_terms_of_services, get_terms_of_service, put_terms_of_service, \
    delete_terms_of_service
from modules.terms_of_services.model import TermsOfService
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
def test_get_terms_of_services(app, mocker):
    expected_status = 200
    expected_length = 2
    expected_properties = ['created_at', 'id',  'publish_date', 'status',
                           'status_changed_at', 'text', 'updated_at',
                           'version']
    expected_limit = 10
    expected_page = 1
    expected_total = 2

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [TermsOfService()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    result = get_terms_of_services()

    assert result[1] == expected_status
    assert len(result[0].json['terms_of_services']) == expected_length
    assert result[0].json['terms_of_services'][0] == {
        x: None for x in expected_properties}
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_terms_of_services_limit_10_page_2_of_3(app, mocker):
    expected_status = 200
    expected_length = 10
    expected_properties = ['created_at', 'id', 'publish_date', 'status',
                           'status_changed_at', 'text', 'updated_at',
                           'version']
    expected_limit = 10
    expected_page = 2
    expected_total = 25
    expected_previous_uri = 'http://localhost/terms_of_services/1/10'
    expected_next_uri = 'http://localhost/terms_of_services/3/10'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [TermsOfService()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    result = get_terms_of_services(expected_page, expected_limit)

    assert result[1] == expected_status
    assert len(result[0].json['terms_of_services']) == expected_length
    assert result[0].json['terms_of_services'][0] == {
        x: None for x in expected_properties}
    assert result[0].json['previous_uri'] == expected_previous_uri
    assert result[0].json['next_uri'] == expected_next_uri
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_terms_of_services_empty(app, mocker):
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

    result = get_terms_of_services(5, 10)

    assert result[1] == expected_status
    assert result[0] == expected_content


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_terms_of_services_route(app, mocker, client):
    expected_status = 200
    expected_length = 10
    expected_limit = 10
    expected_page = 1
    expected_total = 15
    expected_next_uri = 'http://localhost/terms_of_services/2/10'

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
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [TermsOfService()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    # mock user login
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get("/terms_of_services?app_key=123",
                          headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert len(response.json['terms_of_services']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_terms_of_services_limit_5_page_2_of_3_route(app, mocker, client):
    expected_status = 200
    expected_length = 5
    expected_limit = 5
    expected_page = 2
    expected_total = 12
    expected_next_uri = 'http://localhost/terms_of_services/3/5'
    expected_previous_uri = 'http://localhost/terms_of_services/1/5'

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
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [TermsOfService()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    # mock user login
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get(
        "/terms_of_services/{}/{}?app_key=123".format(expected_page,
                                                      expected_limit),
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert len(response.json['terms_of_services']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri
    assert response.json['previous_uri'] == expected_previous_uri


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_terms_of_services_empty_route(app, mocker, client):
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
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get("/terms_of_services/3?app_key=123",
                          headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_terms_of_services_route_no_app_key(app, client):
    expected_status = 401

    response = client.get("/terms_of_services")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_terms_of_services_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.get("/terms_of_services?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_terms_of_services_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.get("/terms_of_services?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_terms_of_service_ok(app, mocker):
    expected_status = 200
    expected_properties = ['created_at', 'id', 'publish_date', 'status',
                           'status_changed_at', 'text', 'updated_at',
                           'version']

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = TermsOfService()

    result = get_terms_of_service(1)

    assert result[1] == expected_status
    assert result[0].json['terms_of_service'] == {
        x: None for x in expected_properties}


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_terms_of_service_not_found(app, mocker):
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = None

    try:
        get_terms_of_service(250)
        assert False
    except NotFound:
        assert True


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_terms_of_service_route_ok(app, mocker, client):
    expected_status = 200

    # mock db query
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

    # mock resource query
    query_mock.return_value \
        .get.return_value = TermsOfService()

    # mock user login
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get("/terms_of_service/1?app_key=123",
                          headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert 'terms_of_service' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_terms_of_service_route_no_app_key(app, client):
    expected_status = 401

    response = client.get("/terms_of_service/1")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_terms_of_service_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.get("/terms_of_service/1?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_terms_of_service_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.get("/terms_of_service/1?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_terms_of_services_ok(app, mocker):
    expected_status = 201
    expected_m_length = 8
    expected_m_id = None
    expected_m_text = "This is TOS 7"
    expected_m_version = "2.1"
    expected_m_publish_date = "2019-02-05T08:00:00+0000"
    expected_m_status = TermsOfService.STATUS_ENABLED
    expected_m_created_at = None
    expected_m_updated_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch(
        'modules.terms_of_services.routes_admin.request')
    request_mock.json = {
        'text': expected_m_text,
        'version': expected_m_version,
        "publish_date": expected_m_publish_date,
        "status": expected_m_status,
    }

    db_mock = mocker.patch('modules.terms_of_services.routes_admin.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    result = post_terms_of_services()

    assert result[1] == expected_status
    assert 'terms_of_service' in result[0].json
    assert len(result[0].json['terms_of_service']) == expected_m_length
    assert result[0].json['terms_of_service']['id'] == expected_m_id
    assert result[0].json['terms_of_service']['text'] == expected_m_text
    assert result[0].json['terms_of_service']['version'] == \
        expected_m_version
    assert result[0].json['terms_of_service']['publish_date'] == \
        expected_m_publish_date
    assert result[0].json['terms_of_service']['status'] == expected_m_status
    assert bool(re_datetime.match(
        result[0].json['terms_of_service']['status_changed_at']))
    assert result[0].json['terms_of_service']['created_at'] == \
        expected_m_created_at
    assert result[0].json['terms_of_service']['updated_at'] == \
        expected_m_updated_at


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_terms_of_services_required_fail(app, mocker):
    expected_status = 400
    expected_json = {
        "error": {
            "foo": ["Unknown field."],
            "publish_date": ["Missing data for required field."],
            "status": ["Missing data for required field."],
            "text": ["Missing data for required field."],
            "version": ["Missing data for required field."],
        }
    }

    request_mock = mocker.patch(
        'modules.terms_of_services.routes_admin.request')
    request_mock.json = {'foo': "bar"}

    result = post_terms_of_services()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_terms_of_services_min_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'version': ['Value must be between 1 and 10 characters long.'],
        }
    }

    request_mock = mocker.patch(
        'modules.terms_of_services.routes_admin.request')
    request_mock.json = {
        'text': "This is TOS 7",
        'version': "",
        "publish_date": "2019-02-05T08:00:00+0000",
        "status": 1,
    }

    result = post_terms_of_services()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_terms_of_services_max_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'version': ['Value must be between 1 and 10 characters long.'],
        }
    }

    request_mock = mocker.patch(
        'modules.terms_of_services.routes_admin.request')
    request_mock.json = {
        'text': "This is TOS 7",
        'version': "2.123456789",
        "publish_date": "2019-02-05T08:00:00+0000",
        "status": 1,
    }

    result = post_terms_of_services()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_terms_of_services_type_fail(app, mocker):
    expected_status = 400
    expected_json = {
        "error": {
            "text": ["Not a valid string."],
            "version": ["Not a valid string."],
            "publish_date": ["Not a valid datetime."],
            "status": ["Not a valid integer."]
        }
    }

    request_mock = mocker.patch(
        'modules.terms_of_services.routes_admin.request')
    request_mock.json = {
        'text': 123,
        'version': 123,
        "publish_date": "bad",
        "status": 'bad',
    }

    result = post_terms_of_services()

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_terms_of_services_route_ok(app, mocker, client):
    expected_status = 201
    expected_m_length = 8
    expected_m_id = None
    expected_m_text = "This is TOS 7"
    expected_m_version = "2.1"
    expected_m_publish_date = "2019-02-05T08:00:00+0000"
    expected_m_status = TermsOfService.STATUS_ENABLED
    expected_m_created_at = None
    expected_m_updated_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    data = {
        'text': expected_m_text,
        'version': expected_m_version,
        "publish_date": expected_m_publish_date,
        "status": expected_m_status,
    }

    # mock db query
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

    db_mock = mocker.patch('modules.terms_of_services.routes_admin.db')
    db_mock.add.return_value = None
    db_mock.commit.return_value = None

    # mock user login
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.post(
        "/terms_of_services?app_key=123",
        json=data,
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert 'terms_of_service' in response.json
    assert len(response.json['terms_of_service']) == expected_m_length
    assert response.json['terms_of_service']['id'] == expected_m_id
    assert response.json['terms_of_service']['text'] == expected_m_text
    assert response.json['terms_of_service']['version'] == \
        expected_m_version
    assert response.json['terms_of_service']['publish_date'] == \
        expected_m_publish_date
    assert response.json['terms_of_service']['status'] == expected_m_status
    assert bool(re_datetime.match(
        response.json['terms_of_service']['status_changed_at']))
    assert response.json['terms_of_service']['created_at'] == \
        expected_m_created_at
    assert response.json['terms_of_service']['updated_at'] == \
        expected_m_updated_at


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_terms_of_service_route_no_app_key(app, client):
    expected_status = 401

    response = client.post("/terms_of_services")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_terms_of_service_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.post("/terms_of_services?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_post_terms_of_services_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.post("/terms_of_services?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_terms_of_service_ok(app, mocker):
    expected_status = 200
    expected_m_length = 8
    expected_m_id = 1
    expected_m_text = "This is TOS 1a"
    expected_m_version = "1.0b"
    expected_m_publish_date = "2018-06-19T08:00:00+0000"
    expected_m_status = TermsOfService.STATUS_DISABLED
    expected_m_created_at = None
    expected_m_updated_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    request_mock = mocker.patch(
        'modules.terms_of_services.routes_admin.request')
    request_mock.json = {
        'text': expected_m_text,
        'version': expected_m_version,
        "publish_date": expected_m_publish_date,
        "status": expected_m_status,
    }

    tos_1 = TermsOfService()
    tos_1.id = expected_m_id

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = tos_1

    db_mock = mocker.patch('modules.terms_of_services.routes_admin.db')
    db_mock.commit.return_value = None

    result = put_terms_of_service(expected_m_id)

    assert result[1] == expected_status
    assert 'terms_of_service' in result[0].json
    assert len(result[0].json['terms_of_service']) == expected_m_length
    assert result[0].json['terms_of_service']['id'] == expected_m_id
    assert result[0].json['terms_of_service']['text'] == expected_m_text
    assert result[0].json['terms_of_service']['version'] == \
        expected_m_version
    assert result[0].json['terms_of_service']['publish_date'] == \
        expected_m_publish_date
    assert result[0].json['terms_of_service']['status'] == expected_m_status
    assert bool(re_datetime.match(
        result[0].json['terms_of_service']['status_changed_at']))
    assert result[0].json['terms_of_service']['created_at'] == \
        expected_m_created_at
    assert result[0].json['terms_of_service']['updated_at'] == \
        expected_m_updated_at


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_terms_of_service_required_fail(app, mocker):
    expected_status = 400
    expected_json = {
        "error": {
            "foo": ["Unknown field."],
            "publish_date": ["Missing data for required field."],
            "status": ["Missing data for required field."],
            "text": ["Missing data for required field."],
            "version": ["Missing data for required field."],
        }
    }

    request_mock = mocker.patch(
        'modules.terms_of_services.routes_admin.request')
    request_mock.json = {'foo': "bar"}

    tos_1 = TermsOfService()
    tos_1.id = 1

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = tos_1

    result = put_terms_of_service(1)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_terms_of_service_min_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'version': ['Value must be between 1 and 10 characters long.'],
        }
    }

    request_mock = mocker.patch(
        'modules.terms_of_services.routes_admin.request')
    request_mock.json = {
        'text': "This is TOS 1a",
        'version': "",
        "publish_date": "2019-02-05T08:00:00+0000",
        "status": 2,
    }

    tos_1 = TermsOfService()
    tos_1.id = 1

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = tos_1

    result = put_terms_of_service(1)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_terms_of_service_max_fail(app, mocker):
    expected_status = 400
    expected_json = {
        'error': {
            'version': ['Value must be between 1 and 10 characters long.'],
        }
    }

    request_mock = mocker.patch(
        'modules.terms_of_services.routes_admin.request')
    request_mock.json = {
        'text': "This is TOS 1a",
        'version': "2.123456789",
        "publish_date": "2019-02-05T08:00:00+0000",
        "status": 2,
    }

    tos_1 = TermsOfService()
    tos_1.id = 1

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = tos_1

    result = put_terms_of_service(1)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_terms_of_service_type_fail(app, mocker):
    expected_status = 400
    expected_json = {
        "error": {
            "text": ["Not a valid string."],
            "version": ["Not a valid string."],
            "publish_date": ["Not a valid datetime."],
            "status": ["Not a valid integer."]
        }
    }

    request_mock = mocker.patch(
        'modules.terms_of_services.routes_admin.request')
    request_mock.json = {
        'text': 123,
        'version': 123,
        "publish_date": "bad",
        "status": 'bad',
    }

    tos_1 = TermsOfService()
    tos_1.id = 1

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = tos_1

    result = put_terms_of_service(1)

    assert result[1] == expected_status
    assert result[0].json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_terms_of_service_route_ok(app, mocker, client):
    expected_status = 200
    expected_m_length = 8
    expected_m_id = 1
    expected_m_text = "This is TOS 1a"
    expected_m_version = "1.0b"
    expected_m_publish_date = "2018-06-19T08:00:00+0000"
    expected_m_status = TermsOfService.STATUS_DISABLED
    expected_m_created_at = None
    expected_m_updated_at = None
    # @todo: timezone
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    data = {
        'text': expected_m_text,
        'version': expected_m_version,
        "publish_date": expected_m_publish_date,
        "status": expected_m_status,
    }

    tos_1 = TermsOfService()
    tos_1.id = expected_m_id

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
        .get.return_value = tos_1

    db_mock = mocker.patch('modules.terms_of_services.routes_admin.db')
    db_mock.commit.return_value = None

    # mock user login
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.put(
        "/terms_of_service/{}?app_key=123".format(expected_m_id),
        json=data,
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert 'terms_of_service' in response.json
    assert len(response.json['terms_of_service']) == expected_m_length
    assert response.json['terms_of_service']['id'] == expected_m_id
    assert response.json['terms_of_service']['text'] == expected_m_text
    assert response.json['terms_of_service']['version'] == \
        expected_m_version
    assert response.json['terms_of_service']['publish_date'] == \
        expected_m_publish_date
    assert response.json['terms_of_service']['status'] == expected_m_status
    assert bool(re_datetime.match(
        response.json['terms_of_service']['status_changed_at']))
    assert response.json['terms_of_service']['created_at'] == \
        expected_m_created_at
    assert response.json['terms_of_service']['updated_at'] == \
        expected_m_updated_at


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_terms_of_service_route_no_app_key(app, client):
    expected_status = 401

    response = client.put("/terms_of_service/1")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_terms_of_service_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.put("/terms_of_service/1?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_put_terms_of_service_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.put("/terms_of_service/1?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_delete_terms_of_service_ok(app, mocker):
    expected_status = 204
    expected_content = ''

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = TermsOfService()

    db_mock = mocker.patch('modules.terms_of_services.routes_admin.db')
    db_mock.commit.return_value = None

    result = delete_terms_of_service(1)

    assert result[1] == expected_status
    assert result[0] == expected_content


@pytest.mark.unit
@pytest.mark.admin_api
def test_delete_terms_of_service_fail(app, mocker):
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = None

    try:
        delete_terms_of_service(250)
        assert False
    except NotFound:
        assert True


@pytest.mark.unit
@pytest.mark.admin_api
def test_delete_terms_of_service_route_ok(app, mocker, client):
    expected_status = 204
    expected_json = None

    # mock db query
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

    # mock resource query
    query_mock.return_value \
        .get.return_value = TermsOfService()

    # mock db commit
    db_mock = mocker.patch('modules.terms_of_services.routes_admin.db')
    db_mock.commit.return_value = None

    # mock user login
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.delete("/terms_of_service/4?app_key=123",
                             headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_delete_terms_of_service_route_no_app_key(app, client):
    expected_status = 401

    response = client.delete("/terms_of_service/4")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_delete_terms_of_service_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.delete("/terms_of_service/4?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_delete_terms_of_service_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.delete("/terms_of_service/4?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


# INTEGRATION TESTS


@pytest.mark.integration
@pytest.mark.admin_api
def test_get_terms_of_services_route_with_data(client):
    expected_status = 200
    expected_json = {
        "limit": 10,
        "page": 1,
        "terms_of_services": [
            {
                "created_at": "2018-06-15T00:00:00+0000",
                "id": 1,
                "publish_date": "2018-06-18T00:00:00+0000",
                "status": 1,
                "status_changed_at": "2018-06-17T00:00:00+0000",
                "text": "This is TOS 1",
                "updated_at": "2018-06-17T00:00:00+0000",
                "version": "1.0"
            },
            {
                "created_at": "2019-01-01T00:00:00+0000",
                "id": 2,
                "publish_date": "2019-01-04T00:00:00+0000",
                "status": 1,
                "status_changed_at": "2019-01-03T00:00:00+0000",
                "text": "This is TOS 2",
                "updated_at": "2019-01-02T00:00:00+0000",
                "version": "1.1"
            },
            {
                "created_at": "2019-01-20T00:00:00+0000",
                "id": 4,
                "publish_date": "2019-01-23T00:00:00+0000",
                "status": 2,
                "status_changed_at": "2019-01-22T00:00:00+0000",
                "text": "This is TOS 4",
                "updated_at": "2019-01-21T00:00:00+0000",
                "version": "1.3"
            },
            {
                "created_at": "2019-02-01T00:00:00+0000",
                "id": 6,
                "publish_date": "2019-02-04T00:00:00+0000",
                "status": 5,
                "status_changed_at": "2019-02-03T00:00:00+0000",
                "text": "This is TOS 6",
                "updated_at": "2019-02-02T00:00:00+0000",
                "version": "2.0"
            }
        ],
        "total": 4
    }

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get(
        "/terms_of_services?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.integration
@pytest.mark.admin_api
def test_get_terms_of_service_1_route_with_data(client):
    expected_status = 200
    expected_json = {
        "terms_of_service": {
            "created_at": "2018-06-15T00:00:00+0000",
            "id": 1,
            "publish_date": "2018-06-18T00:00:00+0000",
            "status": 1,
            "status_changed_at": "2018-06-17T00:00:00+0000",
            "text": "This is TOS 1",
            "updated_at": "2018-06-17T00:00:00+0000",
            "version": "1.0"
        }
    }

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get(
        "/terms_of_service/1?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.integration
@pytest.mark.admin_api
def test_post_terms_of_services_route_with_data(client, mocker):
    expected_status = 201
    expected_m_length = 8
    expected_m_id = 7
    expected_m_text = "This is TOS 7"
    expected_m_version = "2.1"
    expected_m_publish_date = "2019-02-05T08:00:00+0000"
    expected_m_status = TermsOfService.STATUS_ENABLED
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}$")

    request_mock = mocker.patch(
        'modules.terms_of_services.routes_admin.request')
    request_mock.json = {
        'text': expected_m_text,
        'version': expected_m_version,
        "publish_date": expected_m_publish_date,
        "status": expected_m_status,
    }

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.post(
        "/terms_of_services?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert 'terms_of_service' in response.json
    assert len(response.json['terms_of_service']) == expected_m_length
    assert response.json['terms_of_service']['id'] == expected_m_id
    assert response.json['terms_of_service']['text'] == expected_m_text
    assert response.json['terms_of_service']['version'] == \
        expected_m_version
    assert response.json['terms_of_service']['publish_date'] == \
        expected_m_publish_date
    assert response.json['terms_of_service']['status'] == expected_m_status
    assert bool(re_datetime.match(
        response.json['terms_of_service']['status_changed_at']))
    assert bool(re_datetime.match(
        response.json['terms_of_service']['created_at']))
    assert bool(re_datetime.match(
        response.json['terms_of_service']['updated_at']))


@pytest.mark.integration
@pytest.mark.admin_api
def test_put_terms_of_service_route_with_data(client, mocker):
    expected_status = 200
    expected_m_length = 8
    expected_m_id = 1
    expected_m_text = "This is TOS 1a"
    expected_m_version = "1.0b"
    expected_m_publish_date = "2018-06-19T08:00:00+0000"
    expected_m_status = TermsOfService.STATUS_DISABLED
    expected_m_created_at = "2018-06-15T00:00:00+0000"
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}$")

    request_mock = mocker.patch(
        'modules.terms_of_services.routes_admin.request')
    request_mock.json = {
        'text': expected_m_text,
        'version': expected_m_version,
        "publish_date": expected_m_publish_date,
        "status": expected_m_status,
    }

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.put(
        "/terms_of_service/{}?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW".format(
            expected_m_id), headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert 'terms_of_service' in response.json
    assert len(response.json['terms_of_service']) == expected_m_length
    assert response.json['terms_of_service']['id'] == expected_m_id
    assert response.json['terms_of_service']['text'] == expected_m_text
    assert response.json['terms_of_service']['version'] == \
        expected_m_version
    assert response.json['terms_of_service']['publish_date'] == \
        expected_m_publish_date
    assert response.json['terms_of_service']['status'] == expected_m_status
    assert bool(re_datetime.match(
        response.json['terms_of_service']['status_changed_at']))
    assert bool(re_datetime.match(
        response.json['terms_of_service']['updated_at']))
    assert response.json['terms_of_service']['created_at'] == \
        expected_m_created_at


@pytest.mark.integration
@pytest.mark.admin_api
def test_delete_terms_of_service_1_route_with_data(client):
    expected_status = 204
    expected_json = None

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.delete(
        "/terms_of_service/5?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json
