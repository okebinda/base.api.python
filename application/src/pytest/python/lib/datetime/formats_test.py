import pytest

from lib.datetime import Formats


# UNIT TESTS


@pytest.mark.unit
def test_format_iso_8601_datetime():
    assert hasattr(Formats, 'ISO_8601_DATETIME')
    assert Formats.ISO_8601_DATETIME == '%Y-%m-%dT%H:%M:%S%z'


@pytest.mark.unit
def test_format_iso_8601_date():
    assert hasattr(Formats, 'ISO_8601_DATE')
    assert Formats.ISO_8601_DATE == '%Y-%m-%d'
