from copy import copy
import base64

import pytest
from werkzeug.exceptions import Unauthorized
from sqlalchemy.orm.exc import NoResultFound

from fixtures import Fixtures
from app import create_app
from config import Config
from modules.locations.routes_admin import get_countries, get_regions
from modules.locations.model import Country, Region
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
def test_get_countries(app, mocker):
    expected_status = 200
    expected_length = 2
    expected_json = {
        'code_2': None,
        'code_3': None,
        'created_at': None,
        'id': None,
        'name': None,
        'status': None,
        'status_changed_at': None,
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
        .__iter__.return_value = [Country()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    result = get_countries()

    assert result[1] == expected_status
    assert len(result[0].json['countries']) == expected_length
    assert result[0].json['countries'][0] == expected_json
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_countries_limit_10_page_2_of_3(app, mocker):
    expected_status = 200
    expected_length = 10
    expected_json = {
        'code_2': None,
        'code_3': None,
        'created_at': None,
        'id': None,
        'name': None,
        'status': None,
        'status_changed_at': None,
        'updated_at': None,
    }
    expected_limit = 10
    expected_page = 2
    expected_total = 25
    expected_previous_uri = 'http://localhost/countries/1/10'
    expected_next_uri = 'http://localhost/countries/3/10'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [Country()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    result = get_countries(expected_page, expected_limit)

    assert result[1] == expected_status
    assert len(result[0].json['countries']) == expected_length
    assert result[0].json['countries'][0] == expected_json
    assert result[0].json['previous_uri'] == expected_previous_uri
    assert result[0].json['next_uri'] == expected_next_uri
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_countries_empty(app, mocker):
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

    result = get_countries(5, 10)

    assert result[1] == expected_status
    assert result[0] == expected_content


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_countries_route(app, mocker, client):
    expected_status = 200
    expected_length = 10
    expected_limit = 10
    expected_page = 1
    expected_total = 30
    expected_next_uri = 'http://localhost/countries/2/10'

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
        .__iter__.return_value = [Country()] * expected_length
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

    response = client.get("/countries?app_key=123",
                          headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert len(response.json['countries']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_countries_limit_5_page_2_of_3_route(app, mocker, client):
    expected_status = 200
    expected_length = 5
    expected_limit = 5
    expected_page = 2
    expected_total = 12
    expected_next_uri = 'http://localhost/countries/3/5'
    expected_previous_uri = 'http://localhost/countries/1/5'

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
        .__iter__.return_value = [Country()] * expected_length
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
        "/countries/{}/{}?app_key=123".format(expected_page, expected_limit),
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert len(response.json['countries']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri
    assert response.json['previous_uri'] == expected_previous_uri


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_countries_empty_route(app, mocker, client):
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

    response = client.get("/countries/3?app_key=123",
                          headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_countries_route_no_app_key(app, client):
    expected_status = 401

    response = client.get("/countries")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_countries_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.get("/countries?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_countries_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.get("/countries?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_regions(app, mocker):
    expected_status = 200
    expected_length = 2
    expected_json = {
        'code_2': None,
        'country': None,
        'created_at': None,
        'id': None,
        'name': None,
        'status': None,
        'status_changed_at': None,
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
        .__iter__.return_value = [Region()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    result = get_regions()

    assert result[1] == expected_status
    assert len(result[0].json['regions']) == expected_length
    assert result[0].json['regions'][0] == expected_json
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_regions_limit_10_page_2_of_3(app, mocker):
    expected_status = 200
    expected_length = 10
    expected_json = {
        'code_2': None,
        'country': None,
        'created_at': None,
        'id': None,
        'name': None,
        'status': None,
        'status_changed_at': None,
        'updated_at': None,
    }
    expected_limit = 10
    expected_page = 2
    expected_total = 25
    expected_previous_uri = 'http://localhost/regions/1/10'
    expected_next_uri = 'http://localhost/regions/3/10'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [Region()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    result = get_regions(expected_page, expected_limit)

    assert result[1] == expected_status
    assert len(result[0].json['regions']) == expected_length
    assert result[0].json['regions'][0] == expected_json
    assert result[0].json['previous_uri'] == expected_previous_uri
    assert result[0].json['next_uri'] == expected_next_uri
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_regions_empty(app, mocker):
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

    result = get_regions(5, 10)

    assert result[1] == expected_status
    assert result[0] == expected_content


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_regions_filter(app, mocker):
    expected_status = 200
    expected_length = 2
    expected_json = {
        'code_2': None,
        'country': None,
        'created_at': None,
        'id': None,
        'name': None,
        'status': None,
        'status_changed_at': None,
        'updated_at': None,
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
        .__iter__.return_value = [Region()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .filter.return_value \
        .count.return_value = expected_total

    request_mock = mocker.patch('modules.locations.routes_admin.request')
    request_mock.args = {'country_id': 1}

    result = get_regions()

    assert result[1] == expected_status
    assert len(result[0].json['regions']) == expected_length
    assert result[0].json['regions'][0] == expected_json
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_regions_route(app, mocker, client):
    expected_status = 200
    expected_length = 10
    expected_limit = 10
    expected_page = 1
    expected_total = 30
    expected_next_uri = 'http://localhost/regions/2/10'

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
        .__iter__.return_value = [Region()] * expected_length
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

    response = client.get("/regions?app_key=123",
                          headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert len(response.json['regions']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_regions_limit_5_page_2_of_3_route(app, mocker, client):
    expected_status = 200
    expected_length = 5
    expected_limit = 5
    expected_page = 2
    expected_total = 12
    expected_next_uri = 'http://localhost/regions/3/5'
    expected_previous_uri = 'http://localhost/regions/1/5'

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
        .__iter__.return_value = [Region()] * expected_length
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
        "/regions/{}/{}?app_key=123".format(expected_page, expected_limit),
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert len(response.json['regions']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri
    assert response.json['previous_uri'] == expected_previous_uri


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_regions_empty_route(app, mocker, client):
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

    response = client.get("/regions/3?app_key=123",
                          headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_regions_filter_route(app, mocker, client):
    expected_status = 200
    expected_length = 10
    expected_limit = 10
    expected_page = 1
    expected_total = 15
    expected_next_uri = 'http://localhost/regions/2/10?country_id=1'

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
        .filter.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [Region()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .filter.return_value \
        .count.return_value = expected_total

    # mock user login
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get("/regions?country_id=1&app_key=123",
                          headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert len(response.json['regions']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_regions_route_no_app_key(app, client):
    expected_status = 401

    response = client.get("/regions")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_regions_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.get("/regions?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_regions_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.get("/regions?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


# INTEGRATION TESTS


@pytest.mark.integration
@pytest.mark.admin_api
def test_get_countries_route_with_data(client):
    expected_status = 200
    expected_json = {
        "countries": [
            {
                "code_2": "US",
                "code_3": "USA",
                "created_at": "2018-01-01T00:00:00+0000",
                "id": 1,
                "name": "United States",
                "status": 1,
                "status_changed_at": "2018-01-03T00:00:00+0000",
                "updated_at": "2018-01-02T00:00:00+0000"
            },
            {
                "code_2": "MX",
                "code_3": "MEX",
                "created_at": "2018-01-05T00:00:00+0000",
                "id": 2,
                "name": "Mexico",
                "status": 1,
                "status_changed_at": "2018-01-07T00:00:00+0000",
                "updated_at": "2018-01-06T00:00:00+0000"
            },
            {
                "code_2": "CA",
                "code_3": "CAN",
                "created_at": "2018-01-10T00:00:00+0000",
                "id": 3,
                "name": "Canada",
                "status": 1,
                "status_changed_at": "2018-01-12T00:00:00+0000",
                "updated_at": "2018-01-11T00:00:00+0000"
            },
            {
                "code_2": "FR",
                "code_3": "FRA",
                "created_at": "2018-01-15T00:00:00+0000",
                "id": 4,
                "name": "France",
                "status": 2,
                "status_changed_at": "2018-01-17T00:00:00+0000",
                "updated_at": "2018-01-16T00:00:00+0000"
            },
            {
                "code_2": "DE",
                "code_3": "DEU",
                "created_at": "2018-02-01T00:00:00+0000",
                "id": 7,
                "name": "Germany",
                "status": 5,
                "status_changed_at": "2018-02-03T00:00:00+0000",
                "updated_at": "2018-02-02T00:00:00+0000"
            }
        ],
        "limit": 10,
        "page": 1,
        "total": 5
    }

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get(
        "/countries?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.integration
@pytest.mark.admin_api
def test_get_regions_route_with_data(client):
    expected_status = 200
    expected_json = {
        "limit": 10,
        "page": 1,
        "regions": [
            {
                "code_2": "CA",
                "country": {
                    "code_2": "US",
                    "code_3": "USA",
                    "id": 1,
                    "name": "United States"
                },
                "created_at": "2018-01-01T00:00:00+0000",
                "id": 1,
                "name": "California",
                "status": 1,
                "status_changed_at": "2018-01-03T00:00:00+0000",
                "updated_at": "2018-01-02T00:00:00+0000"
            },
            {
                "code_2": "OR",
                "country": {
                    "code_2": "US",
                    "code_3": "USA",
                    "id": 1,
                    "name": "United States"
                },
                "created_at": "2018-01-05T00:00:00+0000",
                "id": 2,
                "name": "Oregon",
                "status": 1,
                "status_changed_at": "2018-01-07T00:00:00+0000",
                "updated_at": "2018-01-06T00:00:00+0000"
            },
            {
                "code_2": "WA",
                "country": {
                    "code_2": "US",
                    "code_3": "USA",
                    "id": 1,
                    "name": "United States"
                },
                "created_at": "2018-01-10T00:00:00+0000",
                "id": 3,
                "name": "Washington",
                "status": 1,
                "status_changed_at": "2018-01-12T00:00:00+0000",
                "updated_at": "2018-01-11T00:00:00+0000"
            },
            {
                "code_2": "AL",
                "country": {
                    "code_2": "US",
                    "code_3": "USA",
                    "id": 1,
                    "name": "United States"
                },
                "created_at": "2018-01-15T00:00:00+0000",
                "id": 4,
                "name": "Alabama",
                "status": 2,
                "status_changed_at": "2018-01-17T00:00:00+0000",
                "updated_at": "2018-01-16T00:00:00+0000"
            },
            {
                "code_2": "AR",
                "country": {
                    "code_2": "US",
                    "code_3": "USA",
                    "id": 1,
                    "name": "United States"
                },
                "created_at": "2018-02-01T00:00:00+0000",
                "id": 7,
                "name": "Arkansas",
                "status": 5,
                "status_changed_at": "2018-02-03T00:00:00+0000",
                "updated_at": "2018-02-02T00:00:00+0000"
            },
            {
                "code_2": "BC",
                "country": {
                    "code_2": "CA",
                    "code_3": "CAN",
                    "id": 3,
                    "name": "Canada"
                },
                "created_at": "2018-02-05T00:00:00+0000",
                "id": 8,
                "name": "British Columbia",
                "status": 1,
                "status_changed_at": "2018-02-07T00:00:00+0000",
                "updated_at": "2018-02-06T00:00:00+0000"
            }
        ],
        "total": 6
    }

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get(
        "/regions?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json
