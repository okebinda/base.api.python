from tests.BaseTest import BaseTest
from test_fixtures import *
from tests.utils import get_http_basic_auth_credentials


class AuthTokenTest(BaseTest):

    def test_get_auth_token(self):

        response = self.client.get('/token?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("token", response.json)
        self.assertIn("user_id", response.json)
        self.assertEqual(1, response.json['user_id'])
        self.assertEqual('admin1', response.json['username'])
        self.assertIn("expiration", response.json)
    
    def test_get_auth_token_no_app_key(self):

        response = self.client.get('/token')

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_get_auth_token_bad_app_key(self):

        response = self.client.get('/token?app_key=BAD_APP_KEY')

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])

    def test_get_auth_token_unauthorized(self):

        response = self.client.get('/token?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_get_auth_token_check(self):

        response = self.client.get('/token/check?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("token_check", response.json)
        self.assertEqual(True, response.json['token_check'])

    def test_get_auth_token_check_no_app_key(self):

        response = self.client.get('/token/check')

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_get_auth_token_check_bad_app_key(self):

        response = self.client.get('/token/check?app_key=BAD_APP_KEY')

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])

    def test_get_auth_token_check_unauthorized(self):

        response = self.client.get('/token/check?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
