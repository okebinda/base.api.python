from app import db
from app.lib.sqlalchemy.BaseModel import BaseModel


class TermsOfService(db.Model, BaseModel):

    __tablename__ = 'terms_of_services'

    # columns
    text = db.Column(
        'text',
        db.Text(),
        nullable=False)
    version = db.Column(
        'version',
        db.String(10),
        unique=True,
        nullable=False)
    publish_date = db.Column(
        'publish_date',
        db.TIMESTAMP(timezone=True),
        server_default=db.func.current_timestamp(),
        nullable=False)
