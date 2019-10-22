from app import db
from app.lib.sqlalchemy.BaseModel import BaseModel


class Region(db.Model, BaseModel):

    __tablename__ = 'regions'

    # columns
    name = db.Column(
        'name',
        db.String(60),
        nullable=False)
    code_2 = db.Column(
        'code_2',
        db.String(2))
    country_id = db.Column(
        'country_id',
        db.Integer,
        db.ForeignKey('countries.id'),
        nullable=False)

    # relationships
    country = db.relationship(
        'Country',
        back_populates="regions")
