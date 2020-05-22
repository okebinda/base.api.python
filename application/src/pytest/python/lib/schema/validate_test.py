import pytest

from app import create_app
from config import Config
from init_dep import db
from lib.schema.validate import unique


@pytest.fixture
def app():
    Config.TESTING = True
    app = create_app(Config)
    return app


class TestModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


# UNIT TESTS


@pytest.mark.unit
def test_unique_pass(app, mocker):

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    errors = unique({}, TestModel, TestModel.name, 'foo')

    assert errors == {}


@pytest.mark.unit
def test_unique_fail(app, mocker):

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = TestModel()

    errors = unique({}, TestModel, TestModel.name, 'foo')

    assert errors == {'name': ['Value must be unique.']}


@pytest.mark.unit
def test_unique_update_no_diff_pass(app, mocker):
    test_model = TestModel()
    test_model.name = 'foo'

    errors = unique({}, test_model, TestModel.name, 'foo', update=test_model)

    assert errors == {}


@pytest.mark.unit
def test_unique_update_diff_pass(app, mocker):

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None
    test_model = TestModel()
    test_model.name = 'bar'

    errors = unique({}, test_model, TestModel.name, 'foo', update=test_model)

    assert errors == {}


@pytest.mark.unit
def test_unique_update_diff_fail(app, mocker):

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = TestModel()
    test_model = TestModel()
    test_model.name = 'bar'

    errors = unique({}, test_model, TestModel.name, 'foo', update=test_model)

    assert errors == {'name': ['Value must be unique.']}
