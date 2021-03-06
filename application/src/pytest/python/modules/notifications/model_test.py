from copy import copy

import pytest

from app import create_app
from config import Config
from modules.notifications.model import Notification
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
def test_login_get_1(app):
    notification = Notification.query.get(1)
    assert notification.id == 1
    assert notification.channel == 1
    assert notification.template == "template-1"
    assert notification.service == "Service 1"
    assert notification.notification_id == "123456"
    assert notification.accepted == 1
    assert notification.rejected == 0
    assert notification.sent_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2019-02-01T10:45:00+0000"
    assert notification.status == 1
    assert notification.status_changed_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2019-02-03T00:00:00+0000"
    assert notification.created_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2019-02-01T00:00:00+0000"
    assert notification.updated_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2019-02-02T00:00:00+0000"
