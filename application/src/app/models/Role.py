from app import db

class Role(db.Model):

    __tablename__ = 'roles'

    # columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    is_admin_role = db.Column(db.Boolean, nullable=False)
    priority = db.Column(db.SmallInteger, nullable=False)
    login_lockout_policy = db.Column(db.Boolean, nullable=False)
    login_max_attempts = db.Column(db.SmallInteger, nullable=False)
    login_timeframe = db.Column(db.SmallInteger, nullable=False)
    login_ban_time = db.Column(db.SmallInteger, nullable=False)
    login_ban_by_ip = db.Column(db.Boolean, nullable=False)
    password_policy = db.Column(db.Boolean, nullable=False)
    password_reuse_history = db.Column(db.SmallInteger, nullable=False)
    password_reset_days = db.Column(db.SmallInteger, nullable=False)

    # timestamps
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp(),
        nullable=False)
    updated_at = db.Column(
        db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(), nullable=False)
