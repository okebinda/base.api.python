
import logging
from logging.config import dictConfig
import uuid

from flask import g
from datetime import datetime, timezone

from .JSONAccessLogFormatter import JSONAccessLogFormatter
from .JSONDefaultLogFormatter import JSONDefaultLogFormatter


class JSONLogger:

    def __init__(self):

        self.default_formatter = JSONDefaultLogFormatter
        self.access_formatter = JSONAccessLogFormatter

    def init_app(self, app, logging_level='ERROR', *, default_handler=None,
                 access_handler=None, default_formatter=None,
                 access_formatter=None):

        if app.config.get('DEBUG') or app.config.get('TESTING'):
            app.logger.setLevel(logging_level)

        else:
            if default_formatter is not None:
                self.default_formatter = default_formatter
            if access_formatter is not None:
                self.access_formatter = access_formatter

            if default_handler is None:
                default_handler = {
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://sys.stderr',
                    'formatter': 'default',
                }

            if access_handler is None:
                access_handler = {
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://sys.stdout',
                    'formatter': 'access',
                }

            log_config = {
                'version': 1,
                'loggers': {
                    "": {
                        "level": logging_level,
                        "handlers": ["default"],
                        "propagate": True,
                    },
                    "access_log": {
                        "level": 'INFO',
                        "handlers": ["access"],
                        "propagate": False,
                    },
                },
                'formatters': {
                    'default': {
                        'format': '%(message)s',
                    },
                    'access': {
                        'format': '%(message)s',
                    },
                },
                'handlers': {
                    'default': default_handler,
                    'access': access_handler,
                }
            }
            dictConfig(log_config)

            # disable default Flask logger
            logging.getLogger('werkzeug').disabled = True

            # apply custom log formatters
            logging.getLogger().handlers[0].formatter = \
                self.default_formatter()
            logging.getLogger('access_log').handlers[0].formatter = \
                self.access_formatter()

            @app.before_request
            def before_request():
                g.request_time = datetime.now(timezone.utc)
                g.request_uuid = uuid.uuid4()

            @app.after_request
            def after_request(response):
                """ Logging after every request. """
                logging.getLogger("access_log").info(
                    "", extra={'response': response})
                return response
