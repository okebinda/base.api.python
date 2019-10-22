import os


class Config:

    # application properties
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # database properties
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # authentication properties
    AUTH_SECRET_KEY = os.environ.get('AUTH_SECRET_KEY')
    AUTH_TOKEN_EXPIRATION = int(os.getenv('AUTH_TOKEN_EXPIRATION', 1800))
    AUTH_HASH_ROUNDS = int(os.getenv('AUTH_HASH_ROUNDS', 15))

    # encryption properties
    CRYPT_SYM_SECRET_KEY = os.environ.get('CRYPT_SYM_SECRET_KEY')
    CRYPT_DIGEST_SALT = os.environ.get('CRYPT_DIGEST_SALT')

    # CORS properties
    CORS_ORIGIN = os.environ.get('CORS_ORIGIN')
