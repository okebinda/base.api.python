from copy import copy

import pytest

from app import create_app
from config import Config
from modules.locations.schema_public import CountrySchema, RegionSchema
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
def test_country_schema_dump(app):
    country = Country.query.get(1)
    result = CountrySchema().dump(country)
    assert result['code_2'] == 'US'
    assert result['code_3'] == 'USA'
    assert result['id'] == 1
    assert result['name'] == 'United States'
    assert result['regions_uri'] == 'http://localhost/regions/US'


@pytest.mark.integration
def test_region_schema_dump(app):
    region = Region.query.get(1)
    result = RegionSchema().dump(region)
    assert result['code_2'] == 'CA'
    assert result['id'] == 1
    assert result['name'] == 'California'
