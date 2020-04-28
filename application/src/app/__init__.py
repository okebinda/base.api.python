"""Initializes database services for global use"""

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from app.lib.logger import JSONLogger


db = SQLAlchemy()
ma = Marshmallow()
logger = JSONLogger()
