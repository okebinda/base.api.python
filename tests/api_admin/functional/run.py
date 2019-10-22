import unittest
import os
import sys
import getopt

# set environmental variables for testing
os.environ["DATABASE_URL"] = 'postgresql://api_admin:passpass@localhost:5432/api_db_test'
os.environ["SECRET_KEY"] = 'SECRET_KEY'
os.environ["AUTH_SECRET_KEY"] = 'AUTH_SECRET_KEY'
os.environ["AUTH_TOKEN_EXPIRATION"] = '14400'
os.environ["AUTH_HASH_ROUNDS"] = '4'
os.environ["CRYPT_SYM_SECRET_KEY"] = 'CRYPT_SYM_SECRET_KEY'
os.environ["CRYPT_DIGEST_SALT"] = 'CRYPT_DIGEST_SALT'

# include application directory in import path
PACKAGE_PARENT = '../../../application/src'

# get command line args
try:
    opts, args = getopt.getopt(sys.argv[1:], "d:")
except getopt.GetoptError as err:
    print(err)
    usage()
    sys.exit(2)
for o, a in opts:
    if o == "-d":
        PACKAGE_PARENT = a
    else:
        assert False, "unhandled option"

# prep args for unittest
args.insert(0, sys.argv[0])

SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

# include data directory in import path
DATA_PARENT = '../../../data'
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, DATA_PARENT)))

# import unit tests
from tests.routes import AppKeysTest
from tests.routes import AuthTokenTest
from tests.routes import UserAccountTest
from tests.routes import PasswordTest
from tests.routes import RolesTest
from tests.routes import TermsOfServiceTest
from tests.routes import AdministratorsTest
from tests.routes import UsersTest
from tests.routes import UserProfilesTest
from tests.routes import LoginsTest
from tests.routes import CountriesTest
from tests.routes import RegionsTest
from tests.routes import PasswordResetsTest
from tests.routes import NotificationsTest


# run tests
if __name__ == '__main__':
    unittest.main(argv=args)
