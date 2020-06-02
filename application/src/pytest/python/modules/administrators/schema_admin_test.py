from copy import copy
import re

import pytest

from app import create_app
from config import Config
from modules.administrators.schema_admin import AdministratorAdminSchema
from modules.administrators.model import Administrator
from fixtures import Fixtures


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


# INTEGRATION TESTS


@pytest.mark.integration
@pytest.mark.admin_api
def test_administrator_schema_dump(app):
    re_datetime = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}$")

    administrator = Administrator.query.get(1)
    result = AdministratorAdminSchema().dump(administrator)
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
    assert bool(re_datetime.match(result['password_changed_at']))
    assert result['status'] == Administrator.STATUS_ENABLED
    assert result['status_changed_at'] == '2018-11-03T00:00:00+0000'
    assert result['created_at'] == '2018-11-01T00:00:00+0000'
    assert result['updated_at'] == '2018-11-02T00:00:00+0000'
