from app import db
from app.lib.sqlalchemy.BaseModel import BaseModel


class Region(db.Model, BaseModel):

    __tablename__ = 'regions'
    
    # columns
    name = db.Column(db.String(60), nullable=False)
    code_2 = db.Column(db.String(2))
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)

    # relationships
    country = db.relationship('Country', back_populates="regions")
