from copy import copy

import pytest

from fixtures import Fixtures
from app import create_app
from config import Config
from modules.health_check.routes_public import get_health_check


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
def test_get_health_check(app):
    with app.app_context():
        result = get_health_check()
        assert 'success' in result[0].json
        assert result[0].json['success'] is True
        assert result[1] == 200


# INTEGRATION TESTS


@pytest.mark.integration
def test_get_health_check_route(client):
    response = client.get("/health_check")
    assert response.status_code == 200
    assert response.json == {'success': True}


@pytest.mark.integration
@pytest.mark.admin_api
def test_get_health_check_route(client):
    response = client.get("/health_check")
    assert response.status_code == 200
    assert response.json == {'success': True}
