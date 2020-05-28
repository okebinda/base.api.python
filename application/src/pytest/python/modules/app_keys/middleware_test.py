from copy import copy

import pytest
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import Unauthorized

from app import create_app
from config import Config
from modules.app_keys.middleware import require_appkey
from modules.app_keys.model import AppKey
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
def test_require_appkey_pass(app, mocker):

    # mock request
    request_mock = mocker.patch('modules.app_keys.middleware.request')
    request_mock.args = {'app_key': '123'}

    # mock app key db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .one.return_value = AppKey()

    # some function to wrap
    def test_func():
        return True

    # wrap the function
    wrapped_func = require_appkey(test_func)

    try:
        assert wrapped_func() is True
    except Unauthorized:
        assert False


@pytest.mark.unit
def test_require_appkey_bad_key(app, mocker):

    # mock request
    request_mock = mocker.patch('modules.app_keys.middleware.request')
    request_mock.args = {'app_key': 'BAD_KEY'}

    # mock app key db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .one.side_effect = NoResultFound()

    # some function to wrap
    def test_func():
        return True

    # wrap the function
    wrapped_func = require_appkey(test_func)

    try:
        wrapped_func()
        assert False
    except Unauthorized:
        assert True


@pytest.mark.unit
def test_require_appkey_missing_key(app, mocker):

    # some function to wrap
    def test_func():
        return True

    # wrap the function
    wrapped_func = require_appkey(test_func)

    try:
        wrapped_func()
        assert False
    except Unauthorized:
        assert True
