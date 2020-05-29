from copy import copy

import pytest

from app import create_app
from config import Config
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
def test_country_get_1(app):
    country = Country.query.get(1)
    assert country.id == 1
    assert country.name == "United States"
    assert country.code_2 == "US"
    assert country.code_3 == "USA"
    assert len(country.regions) == 7
    assert country.status == Country.STATUS_ENABLED
    assert country.status_changed_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-01-03T00:00:00+0000"
    assert country.created_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-01-01T00:00:00+0000"
    assert country.updated_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-01-02T00:00:00+0000"


@pytest.mark.integration
def test_region_get_1(app):
    region = Region.query.get(1)
    assert region.id == 1
    assert region.name == "California"
    assert region.code_2 == "CA"
    assert region.country.id == 1
    assert region.status == Region.STATUS_ENABLED
    assert region.status_changed_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-01-03T00:00:00+0000"
    assert region.created_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-01-01T00:00:00+0000"
    assert region.updated_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-01-02T00:00:00+0000"
