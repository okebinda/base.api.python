import os
import sys

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# include application directory in import path
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, '../python')))

# include data directory in import path
DATA_PARENT = '../../../../data'
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, DATA_PARENT)))

# application imports
from app import db
from app.Config import Config
from app.api_admin import create_app

# init app
app = create_app(Config)
app.app_context().push()

# clear database
db.engine.execute("DELETE FROM alembic_version")
db.drop_all()

# init flask migration manager
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
