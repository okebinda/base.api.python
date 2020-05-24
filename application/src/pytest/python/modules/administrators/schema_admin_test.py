import pytest

from app import create_app
from config import Config
from modules.administrators.schema_admin import AdministratorSchema
from modules.administrators.model import Administrator
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
def test_administrator_schema_dump(app):
    administrator = Administrator.query.get(1)
    result = AdministratorSchema().dump(administrator)
    assert len(result) == 13
    assert result['id'] == 1
    assert result['username'] == 'admin1'
    assert result['email'] == 'admin1@test.com'
    assert result['first_name'] == 'Tommy'
    assert result['last_name'] == 'Lund'
    assert result['joined_at'] == '2018-11-01T00:00:00+0000'
    assert len(result['roles']) == 1
    assert result['roles'][0]['id'] == 2
    assert result['roles'][0]['name'] == 'SUPER_ADMIN'
    assert result['uri'] == 'http://localhost/administrator/1'
    assert result['password_changed_at'] == '2018-11-04T00:00:00+0000'
    assert result['status'] == Administrator.STATUS_ENABLED
    assert result['status_changed_at'] == '2018-11-03T00:00:00+0000'
    assert result['created_at'] == '2018-11-01T00:00:00+0000'
    assert result['updated_at'] == '2018-11-02T00:00:00+0000'
