"""SQLAlchemy property type for encrypting values at rest"""

from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy import func, type_coerce, String


class PGPString(BYTEA):
    """Defines an encrypted database field"""

    def __init__(self, passphrase, length=None):
        super(PGPString, self).__init__(length)
        self.passphrase = passphrase

    def bind_expression(self, bindvalue):
        # convert the bind's type from PGPString to
        # String, so that it's passed to psycopg2 as is without
        # a dbapi.Binary wrapper
        bindvalue = type_coerce(bindvalue, String)
        return func.pgp_sym_encrypt(bindvalue, self.passphrase,
                                    'compress-algo=1, cipher-algo=aes256')

    def column_expression(self, colexpr):
        return func.pgp_sym_decrypt(colexpr, self.passphrase)
