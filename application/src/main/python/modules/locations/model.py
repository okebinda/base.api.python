"""
SQLAlchemy database record definitions for Locations module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member,too-few-public-methods

from init_dep import db
from lib.sqlalchemy.base_model import BaseModel


class Country(db.Model, BaseModel):
    """Model for Country"""

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


class Region(db.Model, BaseModel):
    """Model for Region"""

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
