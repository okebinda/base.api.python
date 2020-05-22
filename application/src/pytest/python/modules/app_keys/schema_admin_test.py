import pytest

from app import create_app
from config import Config
from modules.app_keys.schema_admin import AppKeySchema
from modules.app_keys.model import AppKey
from fixtures import Fixtures


@pytest.fixture
def app(request):
    Config.TESTING = True
    app = create_app(Config)

    if 'unit' in request.keywords:
        # unit tests don't get data fixtures
        return app
    else:
        # other tests need the test data set
        fixtures = Fixtures(app)
        fixtures.setup()
        yield app
        fixtures.teardown()


# INTEGRATION TESTS


@pytest.mark.integration
def test_country_schema_dump(app):
    app_key = AppKey.query.get(1)
    result = AppKeySchema().dump(app_key)
    assert result['application'] == 'Application 1'
    assert 'created_at' in result
    assert result['id'] == 1
    assert result['key'] == '7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW'
    assert result['status'] == AppKey.STATUS_ENABLED
    assert result['status_changed_at'] == '2018-01-03T00:00:00+0000'
    assert 'updated_at' in result
