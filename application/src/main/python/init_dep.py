"""
Initializes application dependencies.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from lib.logger import JSONLogger


db = SQLAlchemy()
ma = Marshmallow()
logger = JSONLogger()
