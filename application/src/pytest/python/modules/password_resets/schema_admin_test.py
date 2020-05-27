import pytest

from app import create_app
from config import Config
from modules.password_resets.schema_admin import PasswordResetSchema
from modules.password_resets.model import PasswordReset
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
def test_login_schema_dump(app):
    pr = PasswordReset.query.get(1)
    result = PasswordResetSchema().dump(pr)
    assert len(result) == 10
    assert result['id'] == 1
    assert result['user']['id'] == 1
    assert result['user']['username'] == 'user1'
    assert result['user']['uri'] == 'http://localhost/user/1'
    assert result['code'] == 'HD7SF2'
    assert result['is_used'] is True
    assert result['requested_at'] == '2019-01-10T07:13:49+0000'
    assert result['ip_address'] == '1.1.1.1'
    assert result['status'] == 1
    assert result['status_changed_at'] == '2019-01-12T00:00:00+0000'
    assert result['created_at'] == '2019-01-10T00:00:00+0000'
    assert result['updated_at'] == '2019-01-11T00:00:00+0000'
