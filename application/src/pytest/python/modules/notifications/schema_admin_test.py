import pytest

from app import create_app
from config import Config
from modules.notifications.schema_admin import NotificationSchema
from modules.notifications.model import Notification
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
    notification = Notification.query.get(1)
    result = NotificationSchema().dump(notification)
    assert len(result) == 13
    assert result['id'] == 1
    assert result['user']['id'] == 1
    assert result['user']['username'] == 'user1'
    assert result['user']['uri'] == 'http://localhost/user/1'
    assert result['channel'] == 1
    assert result['template'] == 'template-1'
    assert result['service'] == 'Service 1'
    assert result['notification_id'] == '123456'
    assert result['accepted'] == 1
    assert result['rejected'] == 0
    assert result['sent_at'] == '2019-02-01T10:45:00+0000'
    assert result['status'] == 1
    assert result['status_changed_at'] == '2019-02-03T00:00:00+0000'
    assert result['created_at'] == '2019-02-01T00:00:00+0000'
    assert result['updated_at'] == '2019-02-02T00:00:00+0000'
