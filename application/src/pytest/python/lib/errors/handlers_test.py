import pytest
from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden, \
    NotFound, MethodNotAllowed, InternalServerError

from app import create_app
from config import Config
from lib.errors.handlers import error_400, error_401, error_403, error_404, \
    error_405, error_500


@pytest.fixture
def app():
    Config.TESTING = True
    app = create_app(Config)
    return app


# UNIT TESTS


@pytest.mark.unit
def test_error_400(app):
    with app.app_context():
        result = error_400(BadRequest())
        assert 'error' in result.json
        assert result.json['error'] == "Bad data"
        assert result == 400


@pytest.mark.unit
def test_error_401(app):
    with app.app_context():
        result = error_401(Unauthorized())
        assert 'error' in result.json
        assert result.json['error'] == "Unauthorized"
        assert result == 401


@pytest.mark.unit
def test_error_401_custom_description(app):
    with app.app_context():
        result = error_401(Unauthorized("You shall not pass."))
        assert 'error' in result.json
        assert result.json['error'] == "You shall not pass."
        assert result == 401


@pytest.mark.unit
def test_error_403(app):
    with app.app_context():
        result = error_403(Forbidden())
        assert 'error' in result.json
        assert result.json['error'] == "Permission denied"
        assert result == 403


@pytest.mark.unit
def test_error_404(app):
    with app.app_context():
        result = error_404(NotFound())
        assert 'error' in result.json
        assert result.json['error'] == "Not found"
        assert result == 404


@pytest.mark.unit
def test_error_405(app):
    with app.app_context():
        result = error_405(MethodNotAllowed())
        assert 'error' in result.json
        assert result.json['error'] == "Method not allowed"
        assert result == 405


@pytest.mark.unit
def test_error_500(app):
    with app.app_context():
        result = error_500(InternalServerError())
        assert 'error' in result.json
        assert result.json['error'] == "Server error"
        assert result == 500


# INTEGRATION TESTS


@pytest.mark.integration
def test_get_404_route(client):
    response = client.get("/bad_path")
    assert response.status_code == 404
    assert response.json == {'error': 'Not found'}
