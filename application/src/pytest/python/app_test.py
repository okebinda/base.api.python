# import pytest
# from werkzeug.exceptions import NotFound
#
# from app import create_app
# from config import Config
# from lib.errors.handlers import error_404
#
#
# @pytest.fixture
# def app():
#     Config.TESTING = True
#     app = create_app(Config)
#     return app
#
#
# @pytest.mark.unit
# def test_error_404(app):
#     with app.app_context():
#         result = error_404(NotFound())
#         assert 'error' in result.json
#         assert result.json['error'] == "Not found"
#         assert result == 404
#
#
# @pytest.mark.integration
# def test_get_404_route(client):
#     response = client.get("/bad_path")
#     assert response.status_code == 404
#     assert response.json == {'error': 'Not found'}
