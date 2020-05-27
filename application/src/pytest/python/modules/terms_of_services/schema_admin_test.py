from copy import copy

import pytest

from app import create_app
from config import Config
from modules.terms_of_services.schema_admin import TermsOfServiceSchema
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
@pytest.mark.admin_api
def test_app_key_schema_dump(app):
    tos = TermsOfService.query.get(1)
    result = TermsOfServiceSchema().dump(tos)
    assert len(result) == 8
    assert result['id'] == 1
    assert result['text'] == "This is TOS 1"
    assert result['version'] == "1.0"
    assert result['publish_date'] == '2018-06-18T00:00:00+0000'
    assert result['status'] == TermsOfService.STATUS_ENABLED
    assert result['status_changed_at'] == '2018-06-17T00:00:00+0000'
    assert result['created_at'] == '2018-06-15T00:00:00+0000'
    assert result['updated_at'] == '2018-06-17T00:00:00+0000'
