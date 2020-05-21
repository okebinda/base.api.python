import pytest

from lib.sqlalchemy.pgp_string import PGPString


# UNIT TESTS


@pytest.mark.unit
def test_pgp_string_bind_expression():
    # @todo: test actual functionality of PGPString.bind_expression()
    assert hasattr(PGPString, 'bind_expression')


@pytest.mark.unit
def test_pgp_string_column_expression():
    # @todo: test actual functionality of PGPString.column_expression()
    assert hasattr(PGPString, 'column_expression')
