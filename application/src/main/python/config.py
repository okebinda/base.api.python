"""
Main application configuration.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=too-few-public-methods

import os


class Config:
    """Abstract data type containing configuration settings, data only"""

    # application properties
    SECRET_KEY = os.environ.get('SECRET_KEY')
    APP_TYPE = os.environ.get('APP_TYPE')

    # database properties
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # authentication properties
    AUTH_SECRET_KEY = os.environ.get('AUTH_SECRET_KEY')
    AUTH_TOKEN_EXPIRATION = int(os.getenv('AUTH_TOKEN_EXPIRATION', '1800'))
    AUTH_HASH_ROUNDS = int(os.getenv('AUTH_HASH_ROUNDS', '15'))

    # encryption properties
    CRYPT_SYM_SECRET_KEY = os.environ.get('CRYPT_SYM_SECRET_KEY')
    CRYPT_DIGEST_SALT = os.environ.get('CRYPT_DIGEST_SALT')

    # CORS properties
    CORS_ORIGIN = os.environ.get('CORS_ORIGIN', '')

    # logging properties
    LOGGING_DEFAULT_ENABLED = bool(int(os.environ.get(
        'LOGGING_DEFAULT_ENABLED', 1)))
    LOGGING_DEFAULT_LEVEL = os.environ.get(
        'LOGGING_DEFAULT_LEVEL', 'ERROR')
    LOGGING_DEFAULT_FILE = os.environ.get(
        'LOGGING_DEFAULT_FILE', None)
    LOGGING_DEFAULT_FILE_ROTATION = os.environ.get(
        'LOGGING_DEFAULT_FILE_ROTATION', None)
    LOGGING_DEFAULT_FILE_ROTATION_INTERVAL = int(os.environ.get(
        'LOGGING_DEFAULT_FILE_ROTATION_INTERVAL', 1))
    LOGGING_DEFAULT_FILE_ROTATION_RETENTION = int(os.environ.get(
        'LOGGING_DEFAULT_FILE_ROTATION_RETENTION', 10))

    LOGGING_ACCESS_ENABLED = bool(int(os.environ.get(
        'LOGGING_ACCESS_ENABLED', 1)))
    LOGGING_ACCESS_FILE = os.environ.get(
        'LOGGING_ACCESS_FILE', None)
    LOGGING_ACCESS_FILE_ROTATION = os.environ.get(
        'LOGGING_ACCESS_FILE_ROTATION', None)
    LOGGING_ACCESS_FILE_ROTATION_INTERVAL = int(os.environ.get(
        'LOGGING_ACCESS_FILE_ROTATION_INTERVAL', 1))
    LOGGING_ACCESS_FILE_ROTATION_RETENTION = int(os.environ.get(
        'LOGGING_ACCESS_FILE_ROTATION_RETENTION', 10))
