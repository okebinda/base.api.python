from app import db


class Role(db.Model):

    __tablename__ = 'roles'

    # columns
    id = db.Column(
        'id',
        db.Integer,
        primary_key=True)
    name = db.Column(
        'name',
        db.String(32),
        unique=True,
        nullable=False)
    is_admin_role = db.Column(
        'is_admin_role',
        db.Boolean,
        nullable=False)
    priority = db.Column(
        'priority',
        db.SmallInteger,
        nullable=False)
    login_lockout_policy = db.Column(
        'login_lockout_policy',
        db.Boolean,
        nullable=False)
    login_max_attempts = db.Column(
        'login_max_attempts',
        db.SmallInteger,
        nullable=False)
    login_timeframe = db.Column(
        'login_timeframe',
        db.SmallInteger,
        nullable=False)
    login_ban_time = db.Column(
        'login_ban_time',
        db.SmallInteger,
        nullable=False)
    login_ban_by_ip = db.Column(
        'login_ban_by_ip',
        db.Boolean,
        nullable=False)
    password_policy = db.Column(
        'password_policy',
        db.Boolean,
        nullable=False)
    password_reuse_history = db.Column(
        'password_reuse_history',
        db.SmallInteger,
        nullable=False)
    password_reset_days = db.Column(
        'password_reset_days',
        db.SmallInteger,
        nullable=False)

    # timestamps
    created_at = db.Column(
        'created_at',
        db.TIMESTAMP(timezone=True),
        server_default=db.func.current_timestamp(),
        nullable=False)
    updated_at = db.Column(
        'updated_at',
        db.TIMESTAMP(timezone=True),
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
        nullable=False)
