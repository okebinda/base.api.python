import pytest

from app import create_app
from config import Config
from modules.user_profiles.model import UserProfile
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
def test_user_profile_get_1(app):
    user_profile = UserProfile.query.get(2)
    assert user_profile.id == 2
    assert user_profile.first_name == 'Lynne'
    assert user_profile.last_name == 'Harford'
    assert user_profile.joined_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-12-07T00:00:00+0000"
    assert user_profile.user.id == 2
    assert user_profile.status == UserProfile.STATUS_ENABLED
    assert user_profile.status_changed_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-12-08T00:00:00+0000"
    assert user_profile.created_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-12-05T00:00:00+0000"
    assert user_profile.updated_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-12-06T00:00:00+0000"
