import pytest

from app import create_app
from config import Config
from modules.app_keys.model import AppKey
from fixtures import Fixtures


@pytest.fixture
def app(request):
    Config.TESTING = True
    app = create_app(Config)

    if 'unit' in request.keywords:
        # unit tests don't get data fixtures
        yield app
    else:
        # other tests need the test data set
        fixtures = Fixtures(app)
        fixtures.setup()
        yield app
        fixtures.teardown()


# INTEGRATION TESTS


@pytest.mark.integration
def test_app_key_get_1(app):
    app_key = AppKey.query.get(1)
    assert app_key.id == 1
    assert app_key.application == "Application 1"
    assert app_key.key == "7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW"
    assert app_key.status == AppKey.STATUS_ENABLED
    assert app_key.status_changed_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-01-03T00:00:00+0000"
    assert app_key.created_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-01-01T00:00:00+0000"
    assert app_key.updated_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-01-02T00:00:00+0000"
