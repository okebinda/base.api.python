import types

from tests.BaseTest import BaseTest
from test_fixtures import *
from tests.utils import get_http_basic_auth_credentials
    
class UserAccountTest(BaseTest):

    def test_get_user_account(self):

        response = self.client.get(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(UserData.id2_user2)})

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, response.json['user_account']['id'])
        self.assertEqual("user2", response.json['user_account']['username'])
        self.assertEqual("user2@test.com", response.json['user_account']['email'])
        self.assertEqual("Lynne", response.json['user_account']['first_name'])
        self.assertEqual("Harford", response.json['user_account']['last_name'])
        self.assertEqual(True, response.json['user_account']['is_verified'])
        self.assertIn("password_changed_at", response.json['user_account'])
        self.assertEqual("2018-12-10T00:00:00+0000", response.json['user_account']['joined_at'])
        self.assertNotIn("password", response.json['user_account'])
        self.assertNotIn("terms_of_services", response.json['user_account'])
        self.assertNotIn("status", response.json['user_account'])
        self.assertNotIn("status_changed_at", response.json['user_account'])
        self.assertNotIn("password", response.json['user_account'])
        self.assertNotIn("created_at", response.json['user_account'])
        self.assertNotIn("updated_at", response.json['user_account'])

    def test_get_user_account_no_app_key(self):

        response = self.client.get('/user_account',
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(UserData.id2_user2)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_get_user_account_bad_app_key(self):

        response = self.client.get('/user_account?app_key=BAD_APP_KEY',
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(UserData.id2_user2)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_get_user_account_unauthorized(self):

        response = self.client.get(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_get_user_account_no_permission(self):

        response = self.client.get(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            headers={
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(UserData.id1_user1)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])

    def test_post_user_account_step1_success(self):

        response = self.client.post(
            '/user_account/step1?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user9","email":"user9@test.com","password":"user9Pass","password2":"user9Pass","tos_id":2}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(201, response.status_code)
        self.assertEqual(10, response.json['user_account']['id'])
        self.assertEqual("user9", response.json['user_account']['username'])
        self.assertEqual("user9@test.com", response.json['user_account']['email'])
        self.assertEqual(None, response.json['user_account']['first_name'])
        self.assertEqual(None, response.json['user_account']['last_name'])
        self.assertEqual(False, response.json['user_account']['is_verified'])
        self.assertIn("password_changed_at", response.json['user_account'])
        self.assertIn("joined_at", response.json['user_account'])
        self.assertNotIn("password", response.json['user_account'])
        self.assertNotIn("terms_of_services", response.json['user_account'])
        self.assertNotIn("status", response.json['user_account'])
        self.assertNotIn("status_changed_at", response.json['user_account'])
        self.assertNotIn("password", response.json['user_account'])
        self.assertNotIn("created_at", response.json['user_account'])
        self.assertNotIn("updated_at", response.json['user_account'])

    def test_post_user_account_step1_no_tos_error(self):

        response = self.client.post(
            '/user_account/step1?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user9","email":"user9@test.com","password":"user9Pass","password2":"user9Pass"}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("tos_id", response.json['error'])
        self.assertEqual(["Missing data for required field."], response.json['error']['tos_id'])
        self.assertNotIn("username", response.json['error'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("password", response.json['error'])
        self.assertNotIn("password2", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("terms_of_services", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("status_changed_at", response.json['error'])
        self.assertNotIn("created_at", response.json['error'])
        self.assertNotIn("updated_at", response.json['error'])

    def test_post_user_account_step1_bad_tos_error(self):

        response = self.client.post(
            '/user_account/step1?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user9","email":"user9@test.com","password":"user9Pass","password2":"user9Pass","tos_id":250}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("tos_id", response.json['error'])
        self.assertEqual(["Invalid value."], response.json['error']['tos_id'])
        self.assertNotIn("username", response.json['error'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("password", response.json['error'])
        self.assertNotIn("password2", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("terms_of_services", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("status_changed_at", response.json['error'])
        self.assertNotIn("created_at", response.json['error'])
        self.assertNotIn("updated_at", response.json['error'])

    def test_post_user_account_step1_error(self):

        response = self.client.post(
            '/user_account/step1?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"foo":"bar"}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertIn("email", response.json['error'])
        self.assertIn("password", response.json['error'])
        self.assertIn("password2", response.json['error'])
        self.assertIn("tos_id", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("terms_of_services", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("status_changed_at", response.json['error'])
        self.assertNotIn("created_at", response.json['error'])
        self.assertNotIn("updated_at", response.json['error'])

    def test_post_user_account_step1_password_comlexity(self):

        response = self.client.post(
            '/user_account/step1?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user9","email":"user9@test.com","password":"password","password2":"password","tos_id":2}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("password", response.json['error'])
        self.assertEqual("Please choose a more complex password.", response.json['error']['password'][0])
        self.assertNotIn("username", response.json['error'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("tos_id", response.json['error'])
        self.assertNotIn("password2", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("terms_of_services", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("status_changed_at", response.json['error'])
        self.assertNotIn("created_at", response.json['error'])
        self.assertNotIn("updated_at", response.json['error'])

    def test_post_user_account_step1_password_not_matching(self):

        response = self.client.post(
            '/user_account/step1?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user9","email":"user9@test.com","password":"user9Pass","password2":"user9PassA","tos_id":2}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("password2", response.json['error'])
        self.assertEqual(["Passwords must match."], response.json['error']['password2'])
        self.assertNotIn("username", response.json['error'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("password", response.json['error'])
        self.assertNotIn("tos_id", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("terms_of_services", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("status_changed_at", response.json['error'])
        self.assertNotIn("created_at", response.json['error'])
        self.assertNotIn("updated_at", response.json['error'])

    def test_post_user_account_step1_unique_username_error(self):

        response = self.client.post(
            '/user_account/step1?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user1","email":"user9@test.com","password":"user9Pass","password2":"user9Pass","tos_id":2}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must be unique."], response.json['error']['username'])
        self.assertNotIn("password2", response.json['error'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("password", response.json['error'])
        self.assertNotIn("tos_id", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("terms_of_services", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("status_changed_at", response.json['error'])
        self.assertNotIn("created_at", response.json['error'])
        self.assertNotIn("updated_at", response.json['error'])

    def test_post_user_account_step1_unique_email_error(self):

        response = self.client.post(
            '/user_account/step1?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user9","email":"user1@test.com","password":"user9Pass","password2":"user9Pass","tos_id":2}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("email", response.json['error'])
        self.assertEqual(["Value must be unique."], response.json['error']['email'])
        self.assertNotIn("password2", response.json['error'])
        self.assertNotIn("username", response.json['error'])
        self.assertNotIn("password", response.json['error'])
        self.assertNotIn("tos_id", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("terms_of_services", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("status_changed_at", response.json['error'])
        self.assertNotIn("created_at", response.json['error'])
        self.assertNotIn("updated_at", response.json['error'])

    def test_post_user_account_step1_unique_username_and_no_email_error(self):

        response = self.client.post(
            '/user_account/step1?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user1","password":"user9Pass","password2":"user9Pass","tos_id":2}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must be unique."], response.json['error']['username'])
        self.assertIn("email", response.json['error'])
        self.assertNotIn("password", response.json['error'])
        self.assertNotIn("password2", response.json['error'])
        self.assertNotIn("tos_id", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("terms_of_services", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("status_changed_at", response.json['error'])
        self.assertNotIn("created_at", response.json['error'])
        self.assertNotIn("updated_at", response.json['error'])

    def test_post_user_account_step1_username_length_error(self):

        response = self.client.post(
            '/user_account/step1?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"u","email":"user9@test.com","password":"user9Pass","password2":"user9Pass","tos_id":2}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must be between 2 and 40 characters long."], response.json['error']['username'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("password", response.json['error'])
        self.assertNotIn("password2", response.json['error'])
        self.assertNotIn("tos_id", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("terms_of_services", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("status_changed_at", response.json['error'])
        self.assertNotIn("created_at", response.json['error'])
        self.assertNotIn("updated_at", response.json['error'])

    def test_post_user_account_step1_username_numeric_error(self):

        response = self.client.post(
            '/user_account/step1?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"90","email":"user9@test.com","password":"user9Pass","password2":"user9Pass","tos_id":2}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must not be a number."], response.json['error']['username'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("password", response.json['error'])
        self.assertNotIn("password2", response.json['error'])
        self.assertNotIn("tos_id", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("terms_of_services", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("status_changed_at", response.json['error'])
        self.assertNotIn("created_at", response.json['error'])
        self.assertNotIn("updated_at", response.json['error'])

    def test_post_user_account_step1_username_whitespace_error(self):

        response = self.client.post(
            '/user_account/step1?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user 9","email":"user9@test.com","password":"user9Pass","password2":"user9Pass","tos_id":2}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must contain only alphanumeric characters and the underscore."], response.json['error']['username'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("password", response.json['error'])
        self.assertNotIn("password2", response.json['error'])
        self.assertNotIn("tos_id", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("terms_of_services", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("status_changed_at", response.json['error'])
        self.assertNotIn("created_at", response.json['error'])
        self.assertNotIn("updated_at", response.json['error'])

    def test_post_user_account_step1_no_app_key(self):

        response = self.client.post(
            '/user_account/step1',
            data='{"username":"user9","email":"user9@test.com","password":"user9Pass","password2":"user9Pass","tos_id":2}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_post_user_account_step1_bad_app_key(self):

        response = self.client.post(
            '/user_account/step1?app_key=BAD_APP_KEY',
            data='{"username":"user9","email":"user9@test.com","password":"user9Pass","password2":"user9Pass","tos_id":2}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])

    def test_post_user_account_step2_success(self):

        response = self.client.post(
            '/user_account/step1?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user9","email":"user9@test.com","password":"user9Pass","password2":"user9Pass","tos_id":2}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(201, response.status_code)

        response = self.client.post(
            '/user_account/step2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"first_name":"Wilmer","last_name":"Munson"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(types.SimpleNamespace(username='user9', password='user9Pass'))})

        self.assertEqual(201, response.status_code)
        self.assertEqual(10, response.json['user_account']['id'])
        self.assertEqual("user9", response.json['user_account']['username'])
        self.assertEqual("user9@test.com", response.json['user_account']['email'])
        self.assertEqual("Wilmer", response.json['user_account']['first_name'])
        self.assertEqual("Munson", response.json['user_account']['last_name'])
        self.assertEqual(False, response.json['user_account']['is_verified'])
        self.assertIn("password_changed_at", response.json['user_account'])
        self.assertIn("joined_at", response.json['user_account'])
        self.assertNotIn("password", response.json['user_account'])
        self.assertNotIn("terms_of_services", response.json['user_account'])
        self.assertNotIn("status", response.json['user_account'])
        self.assertNotIn("status_changed_at", response.json['user_account'])
        self.assertNotIn("password", response.json['user_account'])
        self.assertNotIn("created_at", response.json['user_account'])
        self.assertNotIn("updated_at", response.json['user_account'])

    def test_post_user_account_step2_whitespace_success(self):

        response = self.client.post(
            '/user_account/step1?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user9","email":"user9@test.com","password":"user9Pass","password2":"user9Pass","tos_id":2}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(201, response.status_code)

        response = self.client.post(
            '/user_account/step2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"first_name":" Wilmer","last_name":"Munson  "}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(types.SimpleNamespace(username='user9', password='user9Pass'))})

        self.assertEqual(201, response.status_code)
        self.assertEqual(10, response.json['user_account']['id'])
        self.assertEqual("user9", response.json['user_account']['username'])
        self.assertEqual("user9@test.com", response.json['user_account']['email'])
        self.assertEqual("Wilmer", response.json['user_account']['first_name'])
        self.assertEqual("Munson", response.json['user_account']['last_name'])
        self.assertEqual(False, response.json['user_account']['is_verified'])
        self.assertIn("password_changed_at", response.json['user_account'])
        self.assertIn("joined_at", response.json['user_account'])
        self.assertNotIn("password", response.json['user_account'])
        self.assertNotIn("terms_of_services", response.json['user_account'])
        self.assertNotIn("status", response.json['user_account'])
        self.assertNotIn("status_changed_at", response.json['user_account'])
        self.assertNotIn("password", response.json['user_account'])
        self.assertNotIn("created_at", response.json['user_account'])
        self.assertNotIn("updated_at", response.json['user_account'])

    def test_post_user_account_step2_error(self):

        response = self.client.post(
            '/user_account/step1?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user9","email":"user9@test.com","password":"user9Pass","password2":"user9Pass","tos_id":2}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(201, response.status_code)

        response = self.client.post(
            '/user_account/step2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"foo":"bar"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(types.SimpleNamespace(username='user9', password='user9Pass'))})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)

        self.assertIn("first_name", response.json['error'])
        self.assertIn("last_name", response.json['error'])
        self.assertNotIn("username", response.json['error'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("terms_of_services", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("status_changed_at", response.json['error'])
        self.assertNotIn("created_at", response.json['error'])
        self.assertNotIn("updated_at", response.json['error'])
    
    def test_post_user_account_step2_no_app_key(self):

        response = self.client.post(
            '/user_account/step1?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user9","email":"user9@test.com","password":"user9Pass","password2":"user9Pass","tos_id":2}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(201, response.status_code)

        response = self.client.post(
            '/user_account/step2',
            data='{"first_name":"Wilmer","last_name":"Munson"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(types.SimpleNamespace(username='user9', password='user9Pass'))})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_post_user_account_step2_bad_app_key(self):

        response = self.client.post(
            '/user_account/step1?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user9","email":"user9@test.com","password":"user9Pass","password2":"user9Pass","tos_id":2}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(201, response.status_code)

        response = self.client.post(
            '/user_account/step2?app_key=BAD_APP_KEY',
            data='{"first_name":"Wilmer","last_name":"Munson"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(types.SimpleNamespace(username='user9', password='user9Pass'))})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])

    def test_post_user_account_step2_unauthorized(self):

        response = self.client.post(
            '/user_account/step1?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user9","email":"user9@test.com","password":"user9Pass","password2":"user9Pass","tos_id":2}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(201, response.status_code)

        response = self.client.post(
            '/user_account/step2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"first_name":"Wilmer","last_name":"Munson"}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_post_user_account_step2_no_permission(self):

        response = self.client.post(
            '/user_account/step1?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user9","email":"user9@test.com","password":"user9Pass","password2":"user9Pass","tos_id":2}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(201, response.status_code)

        response = self.client.post(
            '/user_account/step2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"first_name":"Wilmer","last_name":"Munson",}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(UserData.id1_user1)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])

    def test_put_user_account_user2_success(self):

        response = self.client.put(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user2a","email":"user2a@test.com","first_name":"Lynn","last_name":"Harfourd"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(UserData.id2_user2)})

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, response.json['user_account']['id'])
        self.assertEqual("user2a", response.json['user_account']['username'])
        self.assertEqual("user2a@test.com", response.json['user_account']['email'])
        self.assertEqual("Lynn", response.json['user_account']['first_name'])
        self.assertEqual("Harfourd", response.json['user_account']['last_name'])
        self.assertEqual(True, response.json['user_account']['is_verified'])
        self.assertIn("password_changed_at", response.json['user_account'])
        self.assertEqual("2018-12-10T00:00:00+0000", response.json['user_account']['joined_at'])
        self.assertNotIn("password", response.json['user_account'])
        self.assertNotIn("terms_of_services", response.json['user_account'])
        self.assertNotIn("status", response.json['user_account'])
        self.assertNotIn("status_changed_at", response.json['user_account'])
        self.assertNotIn("password", response.json['user_account'])
        self.assertNotIn("created_at", response.json['user_account'])
        self.assertNotIn("updated_at", response.json['user_account'])

    def test_put_user_account_user2_whitespace_success(self):

        response = self.client.put(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user2a","email":"user2a@test.com","first_name":"Lynn  ","last_name":" Harfourd"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(UserData.id2_user2)})

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, response.json['user_account']['id'])
        self.assertEqual("user2a", response.json['user_account']['username'])
        self.assertEqual("user2a@test.com", response.json['user_account']['email'])
        self.assertEqual("Lynn", response.json['user_account']['first_name'])
        self.assertEqual("Harfourd", response.json['user_account']['last_name'])
        self.assertEqual(True, response.json['user_account']['is_verified'])
        self.assertIn("password_changed_at", response.json['user_account'])
        self.assertEqual("2018-12-10T00:00:00+0000", response.json['user_account']['joined_at'])
        self.assertNotIn("password", response.json['user_account'])
        self.assertNotIn("terms_of_services", response.json['user_account'])
        self.assertNotIn("status", response.json['user_account'])
        self.assertNotIn("status_changed_at", response.json['user_account'])
        self.assertNotIn("password", response.json['user_account'])
        self.assertNotIn("created_at", response.json['user_account'])
        self.assertNotIn("updated_at", response.json['user_account'])

    def test_put_user_account_error(self):

        response = self.client.put(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"foo":"bar"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(UserData.id2_user2)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertIn("email", response.json['error'])
        self.assertIn("first_name", response.json['error'])
        self.assertIn("last_name", response.json['error'])
        self.assertNotIn("terms_of_services", response.json['error'])
        self.assertNotIn("password", response.json['error'])
        self.assertNotIn("password2", response.json['error'])
        self.assertNotIn("tos_id", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("status_changed_at", response.json['error'])
        self.assertNotIn("created_at", response.json['error'])
        self.assertNotIn("updated_at", response.json['error'])

    def test_put_user_account_unique_username_error(self):

        response = self.client.put(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user1","email":"user2a@test.com","first_name":"Lynn","last_name":"Harfourd"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(UserData.id2_user2)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must be unique."], response.json['error']['username'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("terms_of_services", response.json['error'])
        self.assertNotIn("password", response.json['error'])
        self.assertNotIn("password2", response.json['error'])
        self.assertNotIn("tos_id", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("status_changed_at", response.json['error'])
        self.assertNotIn("created_at", response.json['error'])
        self.assertNotIn("updated_at", response.json['error'])

    def test_put_user_account_unique_email_error(self):

        response = self.client.put(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user2a","email":"user1@test.com","first_name":"Lynn","last_name":"Harfourd"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(UserData.id2_user2)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("email", response.json['error'])
        self.assertEqual(["Value must be unique."], response.json['error']['email'])
        self.assertNotIn("username", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("terms_of_services", response.json['error'])
        self.assertNotIn("password", response.json['error'])
        self.assertNotIn("password2", response.json['error'])
        self.assertNotIn("tos_id", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("status_changed_at", response.json['error'])
        self.assertNotIn("created_at", response.json['error'])
        self.assertNotIn("updated_at", response.json['error'])

    def test_put_user_account_unique_username_and_no_first_name_error(self):

        response = self.client.put(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user1","email":"user2a@test.com","last_name":"Harfourd"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(UserData.id2_user2)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must be unique."], response.json['error']['username'])
        self.assertIn("first_name", response.json['error'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("terms_of_services", response.json['error'])
        self.assertNotIn("password", response.json['error'])
        self.assertNotIn("password2", response.json['error'])
        self.assertNotIn("tos_id", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("status_changed_at", response.json['error'])
        self.assertNotIn("created_at", response.json['error'])
        self.assertNotIn("updated_at", response.json['error'])

    def test_put_user_account_username_length_error(self):

        response = self.client.put(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"u","email":"user2a@test.com","first_name":"Lynn","last_name":"Harfourd"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(UserData.id2_user2)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must be between 2 and 40 characters long."], response.json['error']['username'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("terms_of_services", response.json['error'])
        self.assertNotIn("password", response.json['error'])
        self.assertNotIn("password2", response.json['error'])
        self.assertNotIn("tos_id", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("status_changed_at", response.json['error'])
        self.assertNotIn("created_at", response.json['error'])
        self.assertNotIn("updated_at", response.json['error'])

    def test_put_user_account_username_numeric_error(self):

        response = self.client.put(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"20","email":"user2a@test.com","first_name":"Lynn","last_name":"Harfourd"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(UserData.id2_user2)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must not be a number."], response.json['error']['username'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("terms_of_services", response.json['error'])
        self.assertNotIn("password", response.json['error'])
        self.assertNotIn("password2", response.json['error'])
        self.assertNotIn("tos_id", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("status_changed_at", response.json['error'])
        self.assertNotIn("created_at", response.json['error'])
        self.assertNotIn("updated_at", response.json['error'])

    def test_put_user_account_username_whitespace_error(self):

        response = self.client.put(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user 2a","email":"user2a@test.com","first_name":"Lynn","last_name":"Harfourd"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(UserData.id2_user2)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must contain only alphanumeric characters and the underscore."], response.json['error']['username'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("terms_of_services", response.json['error'])
        self.assertNotIn("password", response.json['error'])
        self.assertNotIn("password2", response.json['error'])
        self.assertNotIn("tos_id", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("status_changed_at", response.json['error'])
        self.assertNotIn("created_at", response.json['error'])
        self.assertNotIn("updated_at", response.json['error'])

    def test_put_user_account_no_app_key(self):

        response = self.client.put(
            '/user_account',
            data='{"username":"user2a","email":"user2a@test.com","first_name":"Lynn","last_name":"Harfourd"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(UserData.id2_user2)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_put_user_account_bad_app_key(self):

        response = self.client.put(
            '/user_account?app_key=BAD_APP_KEY',
            data='{"username":"user2a","email":"user2a@test.com","first_name":"Lynn","last_name":"Harfourd"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(UserData.id2_user2)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_put_user_account_unauthorized(self):

        response = self.client.put(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user2a","email":"user2a@test.com","first_name":"Lynn","last_name":"Harfourd"}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])

    def test_put_user_account_no_permission(self):

        response = self.client.put(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user2a","email":"user2a@test.com","first_name":"Lynn","last_name":"Harfourd"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(UserData.id1_user1)})
        
        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])

    def test_delete_user_account_user1(self):

        response = self.client.delete(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(UserData.id2_user2)})

        self.assertEqual(204, response.status_code)
        self.assertEqual(None, response.json)
    
    def test_delete_user_account_no_app_key(self):

        response = self.client.delete(
            '/user_account',
            headers={
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(UserData.id2_user2)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_delete_user_account_bad_app_key(self):

        response = self.client.delete(
            '/user_account?app_key=BAD_APP_KEY',
            headers={
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(UserData.id2_user2)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_delete_user_account_unauthorized(self):

        response = self.client.delete(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])

    def test_delete_user_account_no_permission(self):

        response = self.client.delete(
            '/user_account?app_key=' + AppKeyData.id1_appkey1.key,
            headers={
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(UserData.id1_user1)})
        
        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
    