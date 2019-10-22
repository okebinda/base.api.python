from tests.BaseTest import BaseTest
from test_fixtures import *
from tests.utils import get_http_basic_auth_credentials


class UserAccountTest(BaseTest):

    def test_get_user_account(self):

        response = self.client.get(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.json['user_account']['id'])
        self.assertEqual("admin1", response.json['user_account']['username'])
        self.assertEqual("admin1@test.com", response.json['user_account']['email'])
        self.assertEqual("Tommy", response.json['user_account']['first_name'])
        self.assertEqual("Lund", response.json['user_account']['last_name'])
        self.assertIn("password_changed_at", response.json['user_account'])
        self.assertEqual("2018-11-01T00:00:00+0000", response.json['user_account']['joined_at'])
        self.assertTrue(response.json['user_account']['uri'].endswith('/administrator/1'))
        self.assertNotIn("password", response.json['user_account'])
        self.assertNotIn("terms_of_services", response.json['user_account'])
        self.assertNotIn("status", response.json['user_account'])
        self.assertNotIn("status_changed_at", response.json['user_account'])
        self.assertNotIn("created_at", response.json['user_account'])
        self.assertNotIn("updated_at", response.json['user_account'])
    
    def test_get_user_account_no_app_key(self):

        response = self.client.get('/user_account',
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_get_user_account_bad_app_key(self):

        response = self.client.get('/user_account?app_key=BAD_APP_KEY',
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_ger_user_account_unauthorized(self):

        response = self.client.get(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_get_user_account_no_permission(self):

        response = self.client.get(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            headers={
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])

    def test_put_user_account_user1(self):

        response = self.client.put(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"admin1a","email":"admin1a@test.com","first_name":"Tomy","last_name":"Lunnd"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.json['user_account']['id'])
        self.assertEqual("admin1a", response.json['user_account']['username'])
        self.assertEqual("admin1a@test.com", response.json['user_account']['email'])
        self.assertEqual("Tomy", response.json['user_account']['first_name'])
        self.assertEqual("Lunnd", response.json['user_account']['last_name'])
        self.assertIn("password_changed_at", response.json['user_account'])
        self.assertEqual("2018-11-01T00:00:00+0000", response.json['user_account']['joined_at'])
        self.assertTrue(response.json['user_account']['uri'].endswith('/administrator/1'))
        self.assertNotIn("password", response.json['user_account'])
        self.assertNotIn("terms_of_services", response.json['user_account'])
        self.assertNotIn("status", response.json['user_account'])
        self.assertNotIn("status_changed_at", response.json['user_account'])
        self.assertNotIn("created_at", response.json['user_account'])
        self.assertNotIn("updated_at", response.json['user_account'])

    def test_put_user_account_user1_whitespace(self):

        response = self.client.put(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"admin1a","email":"admin1a@test.com","first_name":"Tomy ","last_name":" Lunnd"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.json['user_account']['id'])
        self.assertEqual("admin1a", response.json['user_account']['username'])
        self.assertEqual("admin1a@test.com", response.json['user_account']['email'])
        self.assertEqual("Tomy", response.json['user_account']['first_name'])
        self.assertEqual("Lunnd", response.json['user_account']['last_name'])
        self.assertIn("password_changed_at", response.json['user_account'])
        self.assertEqual("2018-11-01T00:00:00+0000", response.json['user_account']['joined_at'])
        self.assertTrue(response.json['user_account']['uri'].endswith('/administrator/1'))
        self.assertNotIn("password", response.json['user_account'])
        self.assertNotIn("terms_of_services", response.json['user_account'])
        self.assertNotIn("status", response.json['user_account'])
        self.assertNotIn("status_changed_at", response.json['user_account'])
        self.assertNotIn("created_at", response.json['user_account'])
        self.assertNotIn("updated_at", response.json['user_account'])
    
    def test_put_user_account_error(self):

        response = self.client.put(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"foo":"bar"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertIn("email", response.json['error'])
        self.assertIn("first_name", response.json['error'])
        self.assertIn("last_name", response.json['error'])
        self.assertNotIn("password", response.json['error'])
        self.assertNotIn("terms_of_services", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("status_changed_at", response.json['error'])
        self.assertNotIn("created_at", response.json['error'])
        self.assertNotIn("updated_at", response.json['error'])
    
    def test_put_user_account_unique_username_error(self):

        response = self.client.put(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"admin2","email":"admin1@test.com","first_name":"Tommy","last_name":"Lund"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must be unique."], response.json['error']['username'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("password", response.json['error'])
    
    def test_put_user_account_unique_email_error(self):

        response = self.client.put(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"admin1","email":"admin2@test.com","first_name":"Tommy","last_name":"Lund"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("email", response.json['error'])
        self.assertEqual(["Value must be unique."], response.json['error']['email'])
        self.assertNotIn("username", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("password", response.json['error'])
    
    def test_put_user_account_unique_username_and_no_first_name_error(self):

        response = self.client.put(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"admin2","email":"admin1@test.com","first_name":"","last_name":"Lund"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must be unique."], response.json['error']['username'])
        self.assertIn("first_name", response.json['error'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("password", response.json['error'])

    def test_put_user_account_username_length_error(self):

        response = self.client.put(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"a","email":"admin1@test.com","first_name":"Tommy","last_name":"Lund"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must be between 2 and 40 characters long."], response.json['error']['username'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("password", response.json['error'])

    def test_put_user_account_username_numeric_error(self):

        response = self.client.put(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"10","email":"admin1@test.com","first_name":"Tommy","last_name":"Lund"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must not be a number."], response.json['error']['username'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("password", response.json['error'])
    
    def test_put_user_account_username_whitespace_error(self):

        response = self.client.put(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"admin 1","email":"admin1@test.com","first_name":"Tommy","last_name":"Lund"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must contain only alphanumeric characters and the underscore."], response.json['error']['username'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("password", response.json['error'])
    
    def test_put_user_account_no_app_key(self):

        response = self.client.put(
            '/user_account',
            data='{"username":"admin1a","email":"admin1a@test.com","first_name":"Tommy","last_name":"Lund"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_put_user_account_bad_app_key(self):

        response = self.client.put(
            '/user_account?app_key=BAD_APP_KEY',
            data='{"username":"admin1a","email":"admin1a@test.com","first_name":"Tommy","last_name":"Lund"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_put_user_account_unauthorized(self):

        response = self.client.put(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"admin1a","email":"admin1a@test.com","first_name":"Tommy","last_name":"Lund"}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])

    def test_put_user_account_no_permission(self):

        response = self.client.put(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"admin1a","email":"admin1a@test.com","first_name":"Tommy","last_name":"Lund"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})
        
        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
