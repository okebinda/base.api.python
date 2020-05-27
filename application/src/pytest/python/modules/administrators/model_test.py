from copy import copy

import pytest

from app import create_app
from config import Config
from modules.administrators.model import Administrator, \
    AdministratorPasswordHistory
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


# UNIT TESTS


@pytest.mark.unit
def test_administrator_check_password_pass(app):
    administrator = Administrator()
    administrator.password = 'testPass1'

    assert administrator.check_password('testPass1')


@pytest.mark.unit
def test_administrator_check_password_fail(app):
    administrator = Administrator()
    administrator.password = 'testPass1'

    assert not administrator.check_password('testPass2')


@pytest.mark.unit
def test_administrator_auth_token_pass(app, mocker):
    administrator1 = Administrator()
    administrator1.id = 1
    token = administrator1.generate_auth_token()

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = administrator1

    assert Administrator.verify_auth_token(token)


@pytest.mark.unit
def test_administrator_auth_token_fail(app):
    assert not Administrator.verify_auth_token('badtoken')


# INTEGRATION TESTS


@pytest.mark.integration
def test_administrator_get_1(app):
    administrator = Administrator.query.get(1)
    assert administrator.id == 1
    assert administrator.username == 'admin1'
    assert administrator.email == 'admin1@test.com'
    assert administrator.email_digest == \
        '112bf106b616ea341317d0a07337241b85a9f0d6dd715fe227cbeebf334b492e'
    assert administrator.password != 'admin1pass'
    assert administrator.first_name == 'Tommy'
    assert administrator.last_name == 'Lund'
    assert len(administrator.roles) == 1
    assert len(administrator.password_history) == 2
    assert administrator.joined_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-11-01T00:00:00+0000"
    assert administrator.password_changed_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-11-04T00:00:00+0000"
    assert administrator.status == Administrator.STATUS_ENABLED
    assert administrator.status_changed_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-11-03T00:00:00+0000"
    assert administrator.created_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-11-01T00:00:00+0000"
    assert administrator.updated_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-11-02T00:00:00+0000"


@pytest.mark.integration
def test_administrator_password_history_get_1(app):
    aph = AdministratorPasswordHistory.query.get(1)
    assert aph.id == 1
    assert aph.administrator.id == 1
    assert aph.password == '$2b$04$./bm2r6LxacOsvm.kZvxPOE6NPTjF06qZck9AdhrhV2YHo3ort8qq'
    assert aph.set_date.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-12-03T00:00:00+0000"
    assert aph.created_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-12-01T00:00:00+0000"
    assert aph.updated_at.strftime(
        "%Y-%m-%dT%H:%M:%S%z") == "2018-12-02T00:00:00+0000"
