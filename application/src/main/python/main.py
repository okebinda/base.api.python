"""
Application front controller.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from app import create_app
from config import Config


app = create_app(Config)

if __name__ == "__main__":
    app.run(host='127.0.0.1')
