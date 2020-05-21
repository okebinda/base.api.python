import pytest

from app import create_app
from config import Config
from modules.health_check.routes_public import get_health_check


@pytest.fixture
def app():
    Config.TESTING = True
    app = create_app(Config)
    return app


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
