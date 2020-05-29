from copy import copy

import pytest
from sqlalchemy.orm.exc import NoResultFound

from fixtures import Fixtures
from app import create_app
from config import Config
from modules.terms_of_services.routes_public import get_terms_of_service
from modules.terms_of_services.model import TermsOfService
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
def test_get_terms_of_service_ok(app, mocker):
    expected_status = 200
    expected_properties = ['id',  'publish_date', 'text', 'version']

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .__iter__.return_value = [TermsOfService()]

    result = get_terms_of_service()

    assert result[1] == expected_status
    assert result[0].json['terms_of_service'] == {
        x: None for x in expected_properties}


@pytest.mark.unit
def test_get_terms_of_service_empty(app, mocker):
    expected_status = 204
    expected_content = ''

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .__iter__.return_value = []

    result = get_terms_of_service()

    assert result[1] == expected_status
    assert result[0] == expected_content


@pytest.mark.unit
def test_get_terms_of_service_ok_route(app, mocker, client):
    expected_status = 200
    expected_json = {
        'terms_of_service': {
            'id': None,
            'publish_date': None,
            'text': None,
            'version': None
        }
    }

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .__iter__.return_value = [TermsOfService()]

    response = client.get("/terms_of_service/current?app_key=123")

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.unit
def test_get_terms_of_service_empty_route(app, mocker, client):
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
        .__iter__.return_value = []

    response = client.get("/terms_of_service/current?app_key=123")

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.unit
def test_get_terms_of_service_route_no_app_key(app, client):
    expected_status = 401

    response = client.get("/terms_of_service/current")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
def test_get_terms_of_service_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.get("/terms_of_service/current?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


# INTEGRATION TESTS


@pytest.mark.integration
def test_get_terms_of_service_route_with_data(client):
    expected_status = 200
    expected_json = {
        "terms_of_service": {
            "id": 2,
            "publish_date": "2019-01-04T00:00:00+0000",
            "text": "This is TOS 2",
            "version": "1.1"
        }
    }

    response = client.get(
        "/terms_of_service/current?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW")

    assert response.status_code == expected_status
    assert response.json == expected_json
