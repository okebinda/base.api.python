import pytest

from app import create_app
from config import Config
from modules.locations.model import Country, Region
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
def test_country_get_1(app):
    country = Country.query.get(1)
    assert country.id == 1
    assert country.name == "United States"
    assert country.code_2 == "US"
    assert country.code_3 == "USA"
    assert len(country.regions) == 7
    assert country.status == Country.STATUS_ENABLED
    assert country.status_changed_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-01-01T00:00:00+0000"
    assert type(country.created_at).__name__ == "datetime"
    assert type(country.updated_at).__name__ == "datetime"


@pytest.mark.integration
def test_region_get_1(app):
    region = Region.query.get(1)
    assert region.id == 1
    assert region.name == "California"
    assert region.code_2 == "CA"
    assert region.country.id == 1
    assert region.status == Region.STATUS_ENABLED
    assert region.status_changed_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-01-01T00:00:00+0000"
    assert type(region.created_at).__name__ == "datetime"
    assert type(region.updated_at).__name__ == "datetime"
