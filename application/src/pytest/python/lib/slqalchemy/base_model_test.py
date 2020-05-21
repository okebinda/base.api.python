import pytest

from lib.sqlalchemy.base_model import BaseModel


# UNIT TESTS


@pytest.mark.unit
def test_base_model_statuses():
    assert hasattr(BaseModel, 'STATUS_ENABLED')
    assert hasattr(BaseModel, 'STATUS_DISABLED')
    assert hasattr(BaseModel, 'STATUS_ARCHIVED')
    assert hasattr(BaseModel, 'STATUS_DELETED')
    assert hasattr(BaseModel, 'STATUS_PENDING')
    assert BaseModel.STATUS_ENABLED == 1
    assert BaseModel.STATUS_DISABLED == 2
    assert BaseModel.STATUS_ARCHIVED == 3
    assert BaseModel.STATUS_DELETED == 4
    assert BaseModel.STATUS_PENDING == 5

@pytest.mark.unit
def test_base_model_columns():
    assert hasattr(BaseModel, 'id')
    assert hasattr(BaseModel, 'status')
    assert hasattr(BaseModel, 'status_changed_at')
    assert hasattr(BaseModel, 'created_at')
    assert hasattr(BaseModel, 'updated_at')
