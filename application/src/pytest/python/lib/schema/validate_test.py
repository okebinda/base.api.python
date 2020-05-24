import pytest

from app import create_app
from config import Config
from init_dep import db
from lib.schema.validate import unique, unique_email, exists


@pytest.fixture
def app():
    Config.TESTING = True
    app = create_app(Config)
    return app


class TestModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    email_digest = db.Column(db.String(100))


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

    errors = unique({}, TestModel, TestModel.name, 'foo', update=test_model)

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

    errors = unique({}, TestModel, TestModel.name, 'foo', update=test_model)

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

    errors = unique({}, TestModel, TestModel.name, 'foo', update=test_model)

    assert errors == {'name': ['Value must be unique.']}


@pytest.mark.unit
def test_unique_email_pass(app, mocker):

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None

    errors = unique_email({}, TestModel, TestModel.email, 'foo')

    assert errors == {}


@pytest.mark.unit
def test_unique_email_fail(app, mocker):

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = TestModel()

    errors = unique_email({}, TestModel, TestModel.email, 'foo')

    assert errors == {'email': ['Value must be unique.']}


@pytest.mark.unit
def test_unique_email_update_no_diff_pass(app, mocker):
    test_model = TestModel()
    test_model.email = 'foo'

    errors = unique_email({}, TestModel, TestModel.email, 'foo',
                          update=test_model)

    assert errors == {}


@pytest.mark.unit
def test_unique_unique_email_diff_pass(app, mocker):

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = None
    test_model = TestModel()
    test_model.email = 'bar'

    errors = unique_email({}, TestModel, TestModel.email, 'foo',
                          update=test_model)

    assert errors == {}


@pytest.mark.unit
def test_unique_update_diff_fail(app, mocker):

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .filter.return_value \
        .first.return_value = TestModel()
    test_model = TestModel()
    test_model.email = 'bar'

    errors = unique_email({}, TestModel, TestModel.email, 'foo',
                          update=test_model)

    assert errors == {'email': ['Value must be unique.']}


@pytest.mark.unit
def test_exists_single_pass(app, mocker):
    test_model = TestModel()
    test_model.id = 1

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = test_model

    errors, models = exists({}, TestModel, 'field', 1)

    assert errors == {}
    assert models == test_model


@pytest.mark.unit
def test_exists_multiple_pass(app, mocker):
    test_model = TestModel()
    test_model.id = 1

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = test_model

    errors, models = exists({}, TestModel, 'field', [1, 2])

    assert errors == {}
    assert models == [test_model, test_model]


@pytest.mark.unit
def test_exists_single_fail(app, mocker):

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = None

    errors, models = exists({}, TestModel, 'field', 1)

    assert errors == {'field': ["Invalid value."]}
    assert models is None


@pytest.mark.unit
def test_exists_multiple_fail(app, mocker):

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = None

    errors, models = exists({}, TestModel, 'field', [1, 2])

    assert errors == {'field': ["Invalid value."]}
    assert models == []


@pytest.mark.unit
def test_exists_no_pkey_fail(app, mocker):

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = None

    errors, models = exists({}, TestModel, 'field', None)

    assert errors == {'field': ["Missing data for required field."]}
    assert models is None


@pytest.mark.unit
def test_exists_single_custom_message_fail(app, mocker):

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = None

    errors, models = exists({}, TestModel, 'field', 1, invalid_error="foo")

    assert errors == {'field': ["foo"]}
    assert models is None


@pytest.mark.unit
def test_exists_no_pkey_custom_message_fail(app, mocker):

    # mock db query
    query_mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    query_mock.return_value \
        .get.return_value = None

    errors, models = exists({}, TestModel, 'field', None, missing_error="bar")

    assert errors == {'field': ["bar"]}
    assert models is None
