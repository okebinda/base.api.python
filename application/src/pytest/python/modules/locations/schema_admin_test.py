from copy import copy

import pytest

from app import create_app
from config import Config
from modules.locations.schema_admin import CountryAdminSchema, \
    RegionAdminSchema
from modules.locations.model import Country, Region
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
def test_country_admin_schema_dump(app):
    country = Country.query.get(1)
    result = CountryAdminSchema().dump(country)
    assert len(result) == 8
    assert result['id'] == 1
    assert result['name'] == 'United States'
    assert result['code_2'] == 'US'
    assert result['code_3'] == 'USA'
    assert result['status'] == Country.STATUS_ENABLED
    assert result['status_changed_at'] == '2018-01-03T00:00:00+0000'
    assert result['created_at'] == '2018-01-01T00:00:00+0000'
    assert result['updated_at'] == '2018-01-02T00:00:00+0000'


@pytest.mark.integration
@pytest.mark.admin_api
def test_region_admin_schema_dump(app):
    region = Region.query.get(1)
    result = RegionAdminSchema().dump(region)
    assert len(result) == 8
    assert result['id'] == 1
    assert result['name'] == 'California'
    assert result['code_2'] == 'CA'
    assert result['country']['id'] == 1
    assert result['country']['name'] == 'United States'
    assert result['country']['code_2'] == 'US'
    assert result['country']['code_3'] == 'USA'
    assert result['status'] == Region.STATUS_ENABLED
    assert result['status_changed_at'] == '2018-01-03T00:00:00+0000'
    assert result['created_at'] == '2018-01-01T00:00:00+0000'
    assert result['updated_at'] == '2018-01-02T00:00:00+0000'
