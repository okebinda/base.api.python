from app import db

class BaseModel(object):

    STATUS_ENABLED = 1
    STATUS_DISABLED = 2
    STATUS_ARCHIVED = 3
    STATUS_DELETED = 4
    STATUS_PENDING = 5

    # properties
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.SmallInteger, nullable=False)

    # timestamps
    status_changed_at = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp(),
        nullable=False)
    updated_at = db.Column(
        db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(), nullable=False)
