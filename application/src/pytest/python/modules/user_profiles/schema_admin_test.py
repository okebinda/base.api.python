from copy import copy

import pytest

from app import create_app
from config import Config
from modules.user_profiles.schema_admin import UserProfileSchema
from modules.user_profiles.model import UserProfile
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
def test_user_schema_dump(app):
    user_profile = UserProfile.query.get(2)
    result = UserProfileSchema().dump(user_profile)
    assert len(result) == 9
    assert result['id'] == 2
    assert result['user_id'] == 2
    assert result['first_name'] == 'Lynne'
    assert result['last_name'] == 'Harford'
    assert result['joined_at'] == '2018-12-07T00:00:00+0000'
    assert result['status'] == UserProfile.STATUS_ENABLED
    assert result['status_changed_at'] == '2018-12-08T00:00:00+0000'
    assert result['created_at'] == '2018-12-05T00:00:00+0000'
    assert result['updated_at'] == '2018-12-06T00:00:00+0000'
