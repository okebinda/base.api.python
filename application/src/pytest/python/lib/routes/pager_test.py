import pytest
from flask import Blueprint

from app import create_app
from config import Config
from lib.routes.pager import Pager


@pytest.fixture
def app():
    Config.TESTING = True
    app = create_app(Config)
    return app


# UNIT TESTS


@pytest.mark.unit
def test_pager_get_uris(app):
    with app.app_context():

        # mock a route
        def mock_path(page=1, limit=10):
            pass
        public = Blueprint('pager_test', __name__)
        public.route("/mock_path/<int:page>/<int:limit>",
                     methods=['GET'])(mock_path)
        app.register_blueprint(public)

        # single page of results
        assert Pager.get_uris('pager_test.mock_path', 1, 20, 10, {}) == {}

        # first page of results
        assert Pager.get_uris(
            'pager_test.mock_path', 1, 10, 50, {}
        ) == {'next_uri': 'http://localhost/mock_path/2/10'}

        # second page of results
        assert Pager.get_uris(
            'pager_test.mock_path', 2, 15, 50, {}
        ) == {'previous_uri': 'http://localhost/mock_path/1/15',
              'next_uri': 'http://localhost/mock_path/3/15'}

        # last page of results
        assert Pager.get_uris(
            'pager_test.mock_path', 5, 10, 50, {}
        ) == {'previous_uri': 'http://localhost/mock_path/4/10'}

        # first page of results with args
        assert Pager.get_uris(
            'pager_test.mock_path', 1, 10, 50, {'foo': 'bar'}
        ) == {'next_uri': 'http://localhost/mock_path/2/10?foo=bar'}

        # second page of results with args
        assert Pager.get_uris(
            'pager_test.mock_path', 2, 15, 50, {'foo': 'bar'}
        ) == {'previous_uri': 'http://localhost/mock_path/1/15?foo=bar',
              'next_uri': 'http://localhost/mock_path/3/15?foo=bar'}

        # last page of results with args
        assert Pager.get_uris(
            'pager_test.mock_path', 5, 10, 50, {'foo': 'bar'}
        ) == {'previous_uri': 'http://localhost/mock_path/4/10?foo=bar'}
