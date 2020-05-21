import pytest

from app import create_app
from config import Config
from lib.routes.query import Query


@pytest.fixture
def app():
    Config.TESTING = True
    app = create_app(Config)
    return app


# UNIT TESTS


@pytest.mark.unit
def test_query(app):
    # @todo: Create actual tests for Query
    with app.app_context():
        assert hasattr(Query, 'make')
