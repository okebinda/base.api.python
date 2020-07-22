"""
Logger module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=unused-variable,too-few-public-methods


import logging
from logging.config import dictConfig
import uuid

from flask import g
from datetime import datetime, timezone

from .json_access_log_formatter import JSONAccessLogFormatter
from .json_default_log_formatter import JSONDefaultLogFormatter


class JSONLogger:
    """JSON logger for Flask application."""

    def __init__(self):
        """Initialize JSONLogger with default values."""

        # switches
        self.default_enabled = True
        self.access_enabled = True

        # level
        self.level = logging.ERROR

        # formatters
        self.default_formatter = JSONDefaultLogFormatter
        self.access_formatter = JSONAccessLogFormatter

        # handlers
        self.default_handler = {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
            'formatter': 'default',
        }
        self.access_handler = {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'access',
        }

        # rotation
        self.rotation_when_map = {
            'M': 'M',
            'H': 'H',
            'D': 'D',
            'W': 'W0',
        }
        self.rotation_backup_count_map = {
            'M': 60,
            'H': 24,
            'D': 7,
            'W': 4,
        }

    def init_app(self, app, *, default_formatter=None, access_formatter=None,
                 default_handler=None, access_handler=None):
        """Initialize Flask application for logging.

        :param app: The Flask application instance
        :type app: Flask
        :param default_formatter: An optional log formatter for default logger
        :type default_formatter: logging.Formatter
        :param access_formatter: An optional log formatter for access logger
        :type access_formatter: logging.Formatter
        :param default_handler: An optional configuration for default handler
        :type default_handler: dict
        :param access_handler: An optional configuration for access handler
        :type access_handler: dict
        """

        # we only really want to run this module in production mode
        if app.config.get('DEBUG') or app.config.get('TESTING'):
            app.logger.setLevel(self.level)

        else:

            # configure the logger
            self.config(app, default_formatter, access_formatter,
                        default_handler, access_handler)

            # set python's dictConfig() function
            self.set_dict_config()

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

    def config(self, app, default_formatter, access_formatter, default_handler,
               access_handler):
        """Configure the logger's local properties.

        :param app: The Flask application instance
        :type app: Flask
        :param default_formatter: An optional log formatter for default logger
        :type default_formatter: logging.Formatter
        :param access_formatter: An optional log formatter for access logger
        :type access_formatter: logging.Formatter
        :param default_handler: An optional configuration for default handler
        :type default_handler: dict
        :param access_handler: An optional configuration for access handler
        :type access_handler: dict
        """

        # set switches
        self.default_enabled = bool(app.config.get(
            'LOGGING_DEFAULT_ENABLED', self.default_enabled))
        self.access_enabled = bool(app.config.get(
            'LOGGING_ACCESS_ENABLED', self.access_enabled))

        # config default logger
        if self.default_enabled:

            # set level
            self.level = app.config.get('LOGGING_DEFAULT_LEVEL', self.level)

            # set formatter
            if default_formatter is not None:
                self.default_formatter = default_formatter

            # set handler
            if default_handler is not None:
                self.default_handler = default_handler

            # log to file
            if app.config.get('LOGGING_DEFAULT_FILE', False):
                del self.default_handler['stream']
                self.default_handler['class'] = 'logging.FileHandler'
                self.default_handler['mode'] = 'a'
                self.default_handler['filename'] = app.config.get(
                    'LOGGING_DEFAULT_FILE')

            # log to rotating file
            if (app.config.get('LOGGING_DEFAULT_FILE_ROTATION', False)
                    and app.config.get('LOGGING_DEFAULT_FILE', False)):

                when = self.rotation_when_map[
                    app.config.get('LOGGING_DEFAULT_FILE_ROTATION')]

                interval = 1
                if app.config.get(
                        'LOGGING_DEFAULT_FILE_ROTATION_INTERVAL'):
                    interval = app.config.get(
                        'LOGGING_DEFAULT_FILE_ROTATION_INTERVAL')

                retention = self.rotation_backup_count_map[app.config.get(
                    'LOGGING_DEFAULT_FILE_ROTATION')]
                if app.config.get(
                        'LOGGING_DEFAULT_FILE_ROTATION_RETENTION'):
                    retention = app.config.get(
                        'LOGGING_DEFAULT_FILE_ROTATION_RETENTION')

                del self.default_handler['mode']
                self.default_handler['class'] = \
                    'logging.handlers.TimedRotatingFileHandler'
                self.default_handler['when'] = when
                self.default_handler['interval'] = interval
                self.default_handler['backupCount'] = retention

        else:
            logging.getLogger().disabled = True

        # config access logger
        if self.access_enabled:

            # set level
            if access_formatter is not None:
                self.access_formatter = access_formatter

            # set formatter
            if access_handler is not None:
                self.access_handler = access_handler

            # set handler
            if app.config.get('LOGGING_ACCESS_FILE', False):
                del self.access_handler['stream']
                self.access_handler['class'] = 'logging.FileHandler'
                self.access_handler['mode'] = 'a'
                self.access_handler['filename'] = app.config.get(
                    'LOGGING_ACCESS_FILE')

            # log to rotating file
            if (app.config.get('LOGGING_ACCESS_FILE_ROTATION', False)
                    and app.config.get('LOGGING_ACCESS_FILE', False)):

                when = self.rotation_when_map[
                    app.config.get('LOGGING_ACCESS_FILE_ROTATION')]

                interval = 1
                if app.config.get('LOGGING_ACCESS_FILE_ROTATION_INTERVAL'):
                    interval = app.config.get(
                        'LOGGING_ACCESS_FILE_ROTATION_INTERVAL')

                retention = self.rotation_backup_count_map[app.config.get(
                    'LOGGING_ACCESS_FILE_ROTATION')]
                if app.config.get('LOGGING_ACCESS_FILE_ROTATION_RETENTION'):
                    retention = app.config.get(
                        'LOGGING_ACCESS_FILE_ROTATION_RETENTION')

                del self.access_handler['mode']
                self.access_handler['class'] = \
                    'logging.handlers.TimedRotatingFileHandler'
                self.access_handler['when'] = when
                self.access_handler['interval'] = interval
                self.access_handler['backupCount'] = retention

        else:
            logging.getLogger('access_log').disabled = True

    def set_dict_config(self):
        """Calls Python's dictConfig() to configure logging."""

        dictConfig({
            'version': 1,
            'loggers': {
                "": {
                    "level": self.level,
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
                'default': self.default_handler,
                'access': self.access_handler,
            }
        })
