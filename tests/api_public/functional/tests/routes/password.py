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
                    + get_http_basic_auth_credentials(UserData.id2_user2)})

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
            data='{"previous_password":"BADPASS","password1":"user2Pass2","password2":"user2Pass2"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(UserData.id2_user2)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("previous_password", response.json['error'])
        self.assertEqual("Incorrect password.", response.json['error']['previous_password'][0])
    
    def test_put_password_no_match(self):

        response = self.client.put(
            '/user_account/password?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"previous_password":"user2pass","password1":"user2Pass2","password2":"user2Pass3"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(UserData.id2_user2)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("password2", response.json['error'])
        self.assertEqual("New passwords must match.", response.json['error']['password2'][0])
    
    def test_put_password_complexity(self):

        response = self.client.put(
            '/user_account/password?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"previous_password":"user2pass","password1":"password","password2":"password"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(UserData.id2_user2)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("password1", response.json['error'])
        self.assertEqual("Please choose a more complex password.", response.json['error']['password1'][0])

    def test_put_password_user2(self):

        response = self.client.put(
            '/user_account/password?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"previous_password":"user2pass","password1":"user2Pass2","password2":"user2Pass2"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(UserData.id2_user2)})

        self.assertEqual(200, response.status_code)
        self.assertEqual('true', response.json['success'])
    
    def test_put_password_no_app_key(self):

        response = self.client.put(
            '/user_account/password',
            data='{"previous_password":"user2pass","password1":"user2Pass2","password2":"user2Pass2"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(UserData.id2_user2)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_put_password_bad_app_key(self):

        response = self.client.put(
            '/user_account/password?app_key=BADD_KEY',
            data='{"previous_password":"user2pass","password1":"user2Pass2","password2":"user2Pass2"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(UserData.id2_user2)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_put_password_unauthorized(self):

        response = self.client.put(
            '/user_account/password?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"previous_password":"user2pass","password1":"user2Pass2","password2":"user2Pass2"}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_put_password_no_permission(self):

        response = self.client.put(
            '/user_account/password?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"previous_password":"user2pass","password1":"user2Pass2","password2":"user2Pass2"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(UserData.id1_user1)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])

    def test_post_password_request_reset_code_error(self):

        response = self.client.post(
            '/password/request-reset-code?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"foo":"bar"}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("email", response.json['error'])
        self.assertEqual("Missing data for required field.", response.json['error']['email'][0])
    
    def test_post_password_request_reset_code_empty_email(self):

        response = self.client.post(
            '/password/request-reset-code?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"email":""}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("email", response.json['error'])
        self.assertEqual("Missing data for required field.", response.json['error']['email'][0])
    
    def test_post_password_request_reset_code_email_not_found(self):

        response = self.client.post(
            '/password/request-reset-code?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"email":"bademail@test.com"}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("email", response.json['error'])
        self.assertEqual("Email address not found.", response.json['error']['email'][0])

    def test_post_password_request_reset_code_success(self):

        response = self.client.post(
            '/password/request-reset-code?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"email":"user2@test.com"}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(201, response.status_code)
        self.assertIn("success", response.json)
        self.assertTrue(response.json['success'])
        self.assertIn("sent", response.json)
        self.assertFalse(response.json['sent'])

    def test_put_password_reset_error(self):

        response = self.client.put(
            '/password/reset?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"foo":"bar"}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("code", response.json['error'])
        self.assertEqual("Missing data for required field.", response.json['error']['code'][0])
        self.assertIn("email", response.json['error'])
        self.assertEqual("Missing data for required field.", response.json['error']['email'][0])
        self.assertIn("password1", response.json['error'])
        self.assertEqual("Missing data for required field.", response.json['error']['password1'][0])
        self.assertIn("password2", response.json['error'])
        self.assertEqual("Missing data for required field.", response.json['error']['password2'][0])
    
    def test_put_password_reset_bad_email(self):

        response = self.client.put(
            '/password/reset?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"code":"J91NP0","email":"bademail@test.com","password1":"user3PASS","password2":"user3PASS"}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("email", response.json['error'])
        self.assertEqual("Email address not found.", response.json['error']['email'][0])

    def test_put_password_reset_bad_code(self):

        response = self.client.put(
            '/password/reset?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"code":"badcode","email":"user2@test.com","password1":"user3PASS","password2":"user3PASS"}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("code", response.json['error'])
        self.assertEqual("Invalid reset code.", response.json['error']['code'][0])

    def test_put_password_reset_password_complexity(self):

        response = self.client.put(
            '/password/reset?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"code":"J91NP0","email":"user2@test.com","password1":"password","password2":"password"}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("password1", response.json['error'])
        self.assertEqual("Please choose a more complex password.", response.json['error']['password1'][0])

    def test_put_password_reset_password_mismatch(self):

        response = self.client.put(
            '/password/reset?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"code":"J91NP0","email":"user2@test.com","password1":"user3PASS","password2":"user3PASS2"}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("password2", response.json['error'])
        self.assertEqual("New passwords must match.", response.json['error']['password2'][0])
    
    def test_put_password_reset_password_expired_code(self):

        response = self.client.put(
            '/password/reset?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"code":"AM8A4N","email":"user2@test.com","password1":"user3PASS","password2":"user3PASS"}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("code", response.json['error'])
        self.assertEqual("Invalid reset code.", response.json['error']['code'][0])
    
    def test_put_password_reset_password_used_code(self):

        response = self.client.put(
            '/password/reset?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"code":"PRQ7M2","email":"user2@test.com","password1":"user3PASS","password2":"user3PASS"}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("code", response.json['error'])
        self.assertEqual("Invalid reset code.", response.json['error']['code'][0])
    
    def test_put_password_reset_password_success(self):

        response = self.client.put(
            '/password/reset?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"code":"J91NP0","email":"user2@test.com","password1":"user3PASS","password2":"user3PASS"}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(200, response.status_code)
        self.assertIn("success", response.json)
        self.assertTrue(response.json['success'])
    
    def test_put_password_reset_no_app_key(self):

        response = self.client.put(
            '/password/reset',
            data='{"code":"J91NP0","email":"user2@test.com","password1":"user3PASS","password2":"user3PASS"}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_put_password_reset_bad_app_key(self):

        response = self.client.put(
            '/password/reset?app_key=BAD_KEY',
            data='{"code":"J91NP0","email":"user2@test.com","password1":"user3PASS","password2":"user3PASS"}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
