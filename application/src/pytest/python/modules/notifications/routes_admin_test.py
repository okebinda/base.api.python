from copy import copy
import base64

import pytest
from werkzeug.exceptions import Unauthorized
from sqlalchemy.orm.exc import NoResultFound

from fixtures import Fixtures
from app import create_app
from config import Config
from modules.notifications.routes_admin import get_notifications
from modules.notifications.model import Notification
from modules.app_keys.model import AppKey
from modules.administrators.model import Administrator
from modules.roles.model import Role


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


# UNIT TESTS


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_notifications(app, mocker):
    expected_status = 200
    expected_length = 2
    expected_json = {
        'accepted': None,
        'channel': None,
        'created_at': None,
        'id': None,
        'notification_id': None,
        'rejected': None,
        'sent_at': None,
        'service': None,
        'status': None,
        'status_changed_at': None,
        'template': None,
        'updated_at': None,
        'user': None,
    }
    expected_limit = 10
    expected_page = 1
    expected_total = 2

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [Notification()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    result = get_notifications()

    assert result[1] == expected_status
    assert len(result[0].json['notifications']) == expected_length
    assert result[0].json['notifications'][0] == expected_json
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_notifications_limit_10_page_2_of_3(app, mocker):
    expected_status = 200
    expected_length = 10
    expected_json = {
        'accepted': None,
        'channel': None,
        'created_at': None,
        'id': None,
        'notification_id': None,
        'rejected': None,
        'sent_at': None,
        'service': None,
        'status': None,
        'status_changed_at': None,
        'template': None,
        'updated_at': None,
        'user': None,
    }
    expected_limit = 10
    expected_page = 2
    expected_total = 25
    expected_previous_uri = 'http://localhost/notifications/1/10'
    expected_next_uri = 'http://localhost/notifications/3/10'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [Notification()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    result = get_notifications(expected_page, expected_limit)

    assert result[1] == expected_status
    assert len(result[0].json['notifications']) == expected_length
    assert result[0].json['notifications'][0] == expected_json
    assert result[0].json['previous_uri'] == expected_previous_uri
    assert result[0].json['next_uri'] == expected_next_uri
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_notifications_empty(app, mocker):
    expected_status = 204
    expected_content = ''

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = []
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = 15

    result = get_notifications(5, 10)

    assert result[1] == expected_status
    assert result[0] == expected_content


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_notifications_filter(app, mocker):
    expected_status = 200
    expected_length = 2
    expected_json = {
        'accepted': None,
        'channel': None,
        'created_at': None,
        'id': None,
        'notification_id': None,
        'rejected': None,
        'sent_at': None,
        'service': None,
        'status': None,
        'status_changed_at': None,
        'template': None,
        'updated_at': None,
        'user': None,
    }
    expected_limit = 10
    expected_page = 1
    expected_total = 2

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .filter.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [Notification()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .filter.return_value \
        .count.return_value = expected_total

    request_mock = mocker.patch('modules.notifications.routes_admin.request')
    request_mock.args = {'user_id': 1}  # could by any other filter criteria

    result = get_notifications()

    assert result[1] == expected_status
    assert len(result[0].json['notifications']) == expected_length
    assert result[0].json['notifications'][0] == expected_json
    assert result[0].json['limit'] == expected_limit
    assert result[0].json['page'] == expected_page
    assert result[0].json['total'] == expected_total


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_notifications_route(app, mocker, client):
    expected_status = 200
    expected_length = 10
    expected_limit = 10
    expected_page = 1
    expected_total = 15
    expected_next_uri = 'http://localhost/notifications/2/10'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login db query
    role2 = Role()
    role2.id = 2
    role2.name = 'SUPER_ADMIN'
    role2.password_reset_days = 365

    admin1 = Administrator()
    admin1.id = 1
    admin1.password = 'admin1pass'
    admin1.roles = [role2]

    query_mock.return_value \
        .filter.return_value \
        .first.return_value = admin1

    auth_db_mock = mocker.patch('modules.administrators.authentication.db')
    auth_db_mock.add.return_value = None
    auth_db_mock.commit.return_value = None

    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [Notification()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    # mock user login
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get("/notifications?app_key=123",
                          headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert len(response.json['notifications']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_notifications_limit_5_page_2_of_3_route(app, mocker, client):
    expected_status = 200
    expected_length = 5
    expected_limit = 5
    expected_page = 2
    expected_total = 12
    expected_next_uri = 'http://localhost/notifications/3/5'
    expected_previous_uri = 'http://localhost/notifications/1/5'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login db query
    role2 = Role()
    role2.id = 2
    role2.name = 'SUPER_ADMIN'
    role2.password_reset_days = 365

    admin1 = Administrator()
    admin1.id = 1
    admin1.password = 'admin1pass'
    admin1.roles = [role2]

    query_mock.return_value \
        .filter.return_value \
        .first.return_value = admin1

    auth_db_mock = mocker.patch('modules.administrators.authentication.db')
    auth_db_mock.add.return_value = None
    auth_db_mock.commit.return_value = None

    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [Notification()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = expected_total

    # mock user login
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get(
        "/notifications/{}/{}?app_key=123".format(expected_page,
                                                  expected_limit),
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert len(response.json['notifications']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri
    assert response.json['previous_uri'] == expected_previous_uri


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_notifications_empty_route(app, mocker, client):
    expected_status = 204
    expected_json = None

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login db query
    role2 = Role()
    role2.id = 2
    role2.name = 'SUPER_ADMIN'
    role2.password_reset_days = 365

    admin1 = Administrator()
    admin1.id = 1
    admin1.password = 'admin1pass'
    admin1.roles = [role2]

    query_mock.return_value \
        .filter.return_value \
        .first.return_value = admin1

    auth_db_mock = mocker.patch('modules.administrators.authentication.db')
    auth_db_mock.add.return_value = None
    auth_db_mock.commit.return_value = None

    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = []
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .count.return_value = 15

    # mock user login
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get("/notifications/3?app_key=123",
                          headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_notifications_filter_route(app, mocker, client):
    expected_status = 200
    expected_length = 10
    expected_limit = 10
    expected_page = 1
    expected_total = 15
    expected_next_uri = 'http://localhost/notifications/2/10?user_id=1'

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login db query
    role2 = Role()
    role2.id = 2
    role2.name = 'SUPER_ADMIN'
    role2.password_reset_days = 365

    admin1 = Administrator()
    admin1.id = 1
    admin1.password = 'admin1pass'
    admin1.roles = [role2]

    query_mock.return_value \
        .filter.return_value \
        .first.return_value = admin1

    auth_db_mock = mocker.patch('modules.administrators.authentication.db')
    auth_db_mock.add.return_value = None
    auth_db_mock.commit.return_value = None

    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .filter.return_value \
        .limit.return_value \
        .offset.return_value \
        .__iter__.return_value = [Notification()] * expected_length
    query_mock.return_value \
        .filter.return_value \
        .order_by.return_value \
        .filter.return_value \
        .count.return_value = expected_total

    # mock user login
    auth_mock = mocker.patch(
        'modules.administrators.Authentication.is_account_locked')
    auth_mock.return_value = False

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get("/notifications?user_id=1&app_key=123",
                          headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert len(response.json['notifications']) == expected_length
    assert response.json['limit'] == expected_limit
    assert response.json['page'] == expected_page
    assert response.json['total'] == expected_total
    assert response.json['next_uri'] == expected_next_uri


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_notifications_route_no_app_key(app, client):
    expected_status = 401

    response = client.get("/notifications")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_notifications_route_bad_app_key(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    response = client.get("/notifications?app_key=BAD_KEY")

    assert response.status_code == expected_status
    assert 'error' in response.json


@pytest.mark.unit
@pytest.mark.admin_api
def test_get_notifications_route_unauthorized(app, mocker, client):
    expected_status = 401

    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')

    # mock app key authorization db query
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # mock user login
    auth_mock = mocker.patch('modules.administrators.Authentication')
    auth_mock.verify_password.side_effect = Unauthorized()

    response = client.get("/notifications?app_key=123")

    assert response.status_code == expected_status
    assert 'error' in response.json


# INTEGRATION TESTS


@pytest.mark.integration
@pytest.mark.admin_api
def test_get_notifications_route_with_data(client):
    expected_status = 200
    expected_json = {
        "limit": 10,
        "notifications": [
            {
                "accepted": 1,
                "channel": 1,
                "created_at": "2019-02-01T00:00:00+0000",
                "id": 1,
                "notification_id": "123456",
                "rejected": 0,
                "sent_at": "2019-02-01T10:45:00+0000",
                "service": "Service 1",
                "status": 1,
                "status_changed_at": "2019-02-03T00:00:00+0000",
                "template": "template-1",
                "updated_at": "2019-02-02T00:00:00+0000",
                "user": {
                    "id": 1,
                    "uri": "http://localhost/user/1",
                    "username": "user1"
                }
            },
            {
                "accepted": 1,
                "channel": 1,
                "created_at": "2019-02-03T00:00:00+0000",
                "id": 2,
                "notification_id": "123457",
                "rejected": 0,
                "sent_at": "2019-02-03T12:10:07+0000",
                "service": "Service 1",
                "status": 1,
                "status_changed_at": "2019-02-05T00:00:00+0000",
                "template": "template-1",
                "updated_at": "2019-02-04T00:00:00+0000",
                "user": {
                    "id": 2,
                    "uri": "http://localhost/user/2",
                    "username": "user2"
                }
            },
            {
                "accepted": 0,
                "channel": 1,
                "created_at": "2019-02-04T00:00:00+0000",
                "id": 3,
                "notification_id": "123458",
                "rejected": 1,
                "sent_at": "2019-02-04T18:51:36+0000",
                "service": "Service 1",
                "status": 2,
                "status_changed_at": "2019-02-06T00:00:00+0000",
                "template": "template-2",
                "updated_at": "2019-02-05T00:00:00+0000",
                "user": {
                    "id": 1,
                    "uri": "http://localhost/user/1",
                    "username": "user1"
                }
            },
            {
                "accepted": 2,
                "channel": 1,
                "created_at": "2019-02-10T00:00:00+0000",
                "id": 6,
                "notification_id": "AB123461",
                "rejected": 1,
                "sent_at": "2019-02-10T06:21:39+0000",
                "service": "Service 2",
                "status": 5,
                "status_changed_at": "2019-02-12T00:00:00+0000",
                "template": "template-3",
                "updated_at": "2019-02-11T00:00:00+0000",
                "user": {
                    "id": 3,
                    "uri": "http://localhost/user/3",
                    "username": "user3"
                }
            },
            {
                "accepted": 0,
                "channel": 2,
                "created_at": "2019-02-13T00:00:00+0000",
                "id": 7,
                "notification_id": "123462",
                "rejected": 1,
                "sent_at": "2019-02-13T17:03:46+0000",
                "service": "Service 1",
                "status": 1,
                "status_changed_at": "2019-02-15T00:00:00+0000",
                "template": "template-3",
                "updated_at": "2019-02-14T00:00:00+0000",
                "user": {
                    "id": 1,
                    "uri": "http://localhost/user/1",
                    "username": "user1"
                }
            }
        ],
        "page": 1,
        "total": 5
    }

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get(
        "/notifications?app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json


@pytest.mark.integration
@pytest.mark.admin_api
def test_get_notifications_filter_route_with_data(client):
    expected_status = 200
    expected_json = {
        "limit": 10,
        "notifications": [
            {
                "accepted": 1,
                "channel": 1,
                "created_at": "2019-02-01T00:00:00+0000",
                "id": 1,
                "notification_id": "123456",
                "rejected": 0,
                "sent_at": "2019-02-01T10:45:00+0000",
                "service": "Service 1",
                "status": 1,
                "status_changed_at": "2019-02-03T00:00:00+0000",
                "template": "template-1",
                "updated_at": "2019-02-02T00:00:00+0000",
                "user": {
                    "id": 1,
                    "uri": "http://localhost/user/1",
                    "username": "user1"
                }
            },
            {
                "accepted": 0,
                "channel": 1,
                "created_at": "2019-02-04T00:00:00+0000",
                "id": 3,
                "notification_id": "123458",
                "rejected": 1,
                "sent_at": "2019-02-04T18:51:36+0000",
                "service": "Service 1",
                "status": 2,
                "status_changed_at": "2019-02-06T00:00:00+0000",
                "template": "template-2",
                "updated_at": "2019-02-05T00:00:00+0000",
                "user": {
                    "id": 1,
                    "uri": "http://localhost/user/1",
                    "username": "user1"
                }
            },
            {
                "accepted": 0,
                "channel": 2,
                "created_at": "2019-02-13T00:00:00+0000",
                "id": 7,
                "notification_id": "123462",
                "rejected": 1,
                "sent_at": "2019-02-13T17:03:46+0000",
                "service": "Service 1",
                "status": 1,
                "status_changed_at": "2019-02-15T00:00:00+0000",
                "template": "template-3",
                "updated_at": "2019-02-14T00:00:00+0000",
                "user": {
                    "id": 1,
                    "uri": "http://localhost/user/1",
                    "username": "user1"
                }
            }
        ],
        "page": 1,
        "total": 3
    }

    credentials = base64.b64encode(
        'admin1:admin1pass'.encode('ascii')).decode('utf-8')

    response = client.get(
        "/notifications?user_id=1&app_key=7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW",
        headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == expected_status
    assert response.json == expected_json
