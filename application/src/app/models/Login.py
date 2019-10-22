from app import db


class Login(db.Model):

    __tablename__ = 'logins'

    # columns
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.Integer, index=True, nullable=True)
    username = db.Column(db.String(40), index=True, nullable=False)
    ip_address = db.Column(db.String(50), index=True)
    success = db.Column(db.Boolean, nullable=False)
    attempt_date = db.Column(
        db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp(),
        nullable=False)

    # timestamps
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp(),
        nullable=False)
    updated_at = db.Column(
        db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(), nullable=False)
