from app import db
from app.lib.sqlalchemy.BaseModel import BaseModel


class Country(db.Model, BaseModel):

    __tablename__ = 'countries'

    # columns
    name = db.Column(
        'name',
        db.String(60),
        unique=True,
        nullable=False)
    code_2 = db.Column(
        'code_2',
        db.String(2),
        unique=True,
        nullable=False)
    code_3 = db.Column(
        'code_3',
        db.String(3),
        unique=True,
        nullable=False)

    # relationships
    regions = db.relationship(
        "Region",
        back_populates="country")
