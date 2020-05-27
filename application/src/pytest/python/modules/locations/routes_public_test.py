from copy import copy

import pytest

from fixtures import Fixtures
from app import create_app
from config import Config
from modules.locations.routes_public import get_countries, get_regions
from modules.locations.model import Country, Region


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
def test_get_countries(app, mocker):
    expected_status = 200
    expected_length = 2
    expected_properties = ['code_2', 'code_3', 'id', 'name', 'regions_uri']
    expected_limit = 250
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
    assert result[0].json['countries'][0] == {
        x: None for x in expected_properties}
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
def test_get_countries_limit_10_page_2_of_3(app, mocker):
    expected_status = 200
    expected_length = 10
    expected_properties = ['code_2', 'code_3', 'id', 'name', 'regions_uri']
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
    assert result[0].json['countries'][0] == {
        x: None for x in expected_properties}
    assert result[0].json['previous_uri'] == expected_previous_uri
    assert result[0].json['next_uri'] == expected_next_uri
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
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
def test_get_regions(app, mocker):
    expected_status = 200
    expected_length = 3
    expected_properties = ['code_2', 'id', 'name']
    expected_limit = 100
    expected_page = 1
    expected_total = 3

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

    result = get_regions('US')

    assert result[1] == expected_status
    assert len(result[0].json['regions']) == expected_length
    assert result[0].json['regions'][0] == {
        x: None for x in expected_properties}
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
def test_get_regions_limit_10_page_2_of_3(app, mocker):
    expected_status = 200
    expected_length = 3
    expected_properties = ['code_2', 'id', 'name']
    expected_limit = 10
    expected_page = 2
    expected_total = 25
    expected_previous_uri = 'http://localhost/regions/US/1/10'
    expected_next_uri = 'http://localhost/regions/US/3/10'

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

    result = get_regions('US', expected_page, expected_limit)

    assert result[1] == expected_status
    assert len(result[0].json['regions']) == expected_length
    assert result[0].json['regions'][0] == {
        x: None for x in expected_properties}
    assert result[0].json['previous_uri'] == expected_previous_uri
    assert result[0].json['next_uri'] == expected_next_uri
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
def test_get_regions_empty(app, mocker):
    expected_status = 204
    expected_content = ''

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .filter.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = []
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .filter.return_value \
        .count.return_value = 15

    result = get_regions('US', 5, 10)

    assert result[1] == expected_status
    assert result[0] == expected_content


# INTEGRATION TESTS


@pytest.mark.integration
def test_get_countries_route(client):
    expected_status = 200
    expected_json = {
        "countries": [
            {
                "code_2": "CA",
                "code_3": "CAN",
                "id": 3,
                "name": "Canada",
                "regions_uri": "http://localhost/regions/CA"
            },
            {
                "code_2": "MX",
                "code_3": "MEX",
                "id": 2,
                "name": "Mexico",
                "regions_uri": "http://localhost/regions/MX"
            },
            {
                "code_2": "US",
                "code_3": "USA",
                "id": 1,
                "name": "United States",
                "regions_uri": "http://localhost/regions/US"
            }
        ],
        "limit": 250,
        "page": 1,
        "total": 3
    }

    response = client.get("/countries")

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.integration
def test_get_regions_route(client):
    expected_status = 200
    expected_json = {
        "limit": 100,
        "page": 1,
        "regions": [
            {
                "code_2": "CA",
                "id": 1,
                "name": "California"
            },
            {
                "code_2": "OR",
                "id": 2,
                "name": "Oregon"
            },
            {
                "code_2": "WA",
                "id": 3,
                "name": "Washington"
            }
        ],
        "total": 3
    }

    response = client.get("/regions/US")

    assert response.status_code == expected_status
    assert response.json == expected_json
