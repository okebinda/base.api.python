from app import db
from app.lib.sqlalchemy.BaseModel import BaseModel


class AppKey(db.Model, BaseModel):

    __tablename__ = 'app_keys'
    
    # columns
    application = db.Column(db.String(200), unique=True, nullable=False)
    key = db.Column(db.String(32), index=True, unique=True, nullable=False)
