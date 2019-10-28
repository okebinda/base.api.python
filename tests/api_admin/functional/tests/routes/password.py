from tests.BaseTest import BaseTest
from test_fixtures import *
from tests.utils import get_http_basic_auth_credentials


class PasswordTest(BaseTest):

    def test_put_password_error(self):

        response = self.client.put(
            '/user_account/password?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"foo":"bar"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("previous_password", response.json['error'])
        self.assertEqual("Missing data for required field.", response.json['error']['previous_password'][0])
        self.assertIn("password1", response.json['error'])
        self.assertEqual("Missing data for required field.", response.json['error']['password1'][0])
        self.assertIn("password2", response.json['error'])
        self.assertEqual("Missing data for required field.", response.json['error']['password2'][0])
    
    def test_put_password_incorrect_password(self):

        response = self.client.put(
            '/user_account/password?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"previous_password":"BADPASS","password1":"admin1Pass2","password2":"admin1Pass2"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("previous_password", response.json['error'])
        self.assertEqual("Incorrect password.", response.json['error']['previous_password'][0])
    
    def test_put_password_no_match(self):

        response = self.client.put(
            '/user_account/password?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"previous_password":"admin1pass","password1":"admin1Pass2","password2":"admin1Pass3"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("password2", response.json['error'])
        self.assertEqual("New passwords must match.", response.json['error']['password2'][0])
    
    def test_put_password_complexity(self):

        response = self.client.put(
            '/user_account/password?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"previous_password":"admin1pass","password1":"password","password2":"password"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("password1", response.json['error'])
        self.assertEqual("Please choose a more complex password.", response.json['error']['password1'][0])

    def test_put_password_admin1(self):

        response = self.client.put(
            '/user_account/password?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"previous_password":"admin1pass","password1":"admin1Pass2","password2":"admin1Pass2"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertEqual('true', response.json['success'])
    
    def test_put_password_no_app_key(self):

        response = self.client.put(
            '/user_account/password',
            data='{"previous_password":"admin1pass","password1":"admin1Pass2","password2":"admin1Pass2"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_put_password_bad_app_key(self):

        response = self.client.put(
            '/user_account/password?app_key=BADD_KEY',
            data='{"previous_password":"admin1pass","password1":"admin1Pass2","password2":"admin1Pass2"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_put_password_unauthorized(self):

        response = self.client.put(
            '/user_account/password?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"previous_password":"admin1pass","password1":"admin1Pass2","password2":"admin1Pass2"}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_put_password_no_permission(self):

        response = self.client.put(
            '/user_account/password?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"previous_password":"admin1pass","password1":"admin1Pass2","password2":"admin1Pass2"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
