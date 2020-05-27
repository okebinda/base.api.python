import pytest

from app import create_app
from config import Config
from modules.users.model import User, UserPasswordHistory, UserTermsOfService
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


# UNIT TESTS


@pytest.mark.unit
def test_user_check_password_pass(app):
    user = User()
    user.password = 'testPass1'

    assert user.check_password('testPass1')


@pytest.mark.unit
def test_user_check_password_fail(app):
    user = User()
    user.password = 'testPass1'

    assert not user.check_password('testPass2')


@pytest.mark.unit
def test_user_auth_token_pass(app, mocker):
    user1 = User()
    user1.id = 1
    token = user1.generate_auth_token()

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = user1

    assert User.verify_auth_token(token)


@pytest.mark.unit
def test_user_auth_token_fail(app):
    assert not User.verify_auth_token('badtoken')


# INTEGRATION TESTS


@pytest.mark.integration
def test_user_get_1(app):
    user = User.query.get(2)
    assert user.id == 2
    assert user.username == 'user2'
    assert user.email == 'user2@test.com'
    assert user.email_digest == \
        '8b1d84bfb7b4b49bbb52a5ec4a523eda3e659c48753655589cf679e6980291f5'
    assert user.password != 'user2pass'
    assert len(user.roles) == 1
    assert len(user.password_history) == 2
    assert len(user.terms_of_services) == 2
    assert len(user.password_resets) == 5
    assert user.password_changed_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-12-08T00:00:00+0000"
    assert user.is_verified is True
    assert user.status == User.STATUS_ENABLED
    assert user.status_changed_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-12-07T00:00:00+0000"
    assert user.created_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-12-05T00:00:00+0000"
    assert user.updated_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-12-06T00:00:00+0000"


@pytest.mark.integration
def test_user_password_history_get_1(app):
    uph = UserPasswordHistory.query.get(1)
    assert uph.id == 1
    assert uph.user.id == 2
    assert uph.password == \
        '$2b$04$90i2qNzbpfpdgeI9RiYi4eXkGKeieO4CIT0jF0vXyuQENr2bjREya'
    assert uph.set_date.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-12-07T00:00:00+0000"
    assert uph.created_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-12-05T00:00:00+0000"
    assert uph.updated_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-12-06T00:00:00+0000"


@pytest.mark.integration
def test_user_terms_of_service_get_1(app):
    utos = UserTermsOfService.query.get((1, 1))
    assert utos.user.id == 1
    assert utos.terms_of_service.id == 1
    assert utos.ip_address == '1.1.1.1'
    assert utos.accept_date.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-12-03T08:00:00+0000"
    assert utos.created_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-12-01T08:00:00+0000"
    assert utos.updated_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-12-02T08:00:00+0000"
