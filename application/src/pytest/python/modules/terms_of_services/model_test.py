from copy import copy

import pytest

from app import create_app
from config import Config
from modules.terms_of_services.model import TermsOfService
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
def test_terms_of_service_get_1(app):
    tos = TermsOfService.query.get(1)
    assert tos.id == 1
    assert tos.text == 'This is TOS 1'
    assert tos.version == '1.0'
    assert tos.publish_date.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-06-18T00:00:00+0000"
    assert tos.status == TermsOfService.STATUS_ENABLED
    assert tos.status_changed_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-06-17T00:00:00+0000"
    assert tos.created_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-06-15T00:00:00+0000"
    assert tos.updated_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-06-17T00:00:00+0000"
