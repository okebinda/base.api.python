from tests.BaseTest import BaseTest
from test_fixtures import *
from tests.utils import get_http_basic_auth_credentials


class RolesTest(BaseTest):

    def test_get_roles(self):

        response = self.client.get('/roles?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("roles", response.json)

        self.assertEqual(1, response.json['roles'][0]['id'])
        self.assertEqual("USER", response.json['roles'][0]['name'])
        self.assertEqual(False, response.json['roles'][0]['is_admin_role'])
        self.assertEqual(100, response.json['roles'][0]['priority'])
        self.assertEqual(False, response.json['roles'][0]['login_lockout_policy'])
        self.assertEqual(10, response.json['roles'][0]['login_max_attempts'])
        self.assertEqual(600, response.json['roles'][0]['login_timeframe'])
        self.assertEqual(1800, response.json['roles'][0]['login_ban_time'])
        self.assertEqual(True, response.json['roles'][0]['login_ban_by_ip'])
        self.assertEqual(False, response.json['roles'][0]['password_policy'])
        self.assertEqual(10, response.json['roles'][0]['password_reuse_history'])
        self.assertEqual(365, response.json['roles'][0]['password_reset_days'])
        self.assertIn("created_at", response.json['roles'][0])
        self.assertIn("updated_at", response.json['roles'][0])

        self.assertEqual(2, response.json['roles'][1]['id'])
        self.assertEqual("SUPER_ADMIN", response.json['roles'][1]['name'])
        self.assertEqual(True, response.json['roles'][1]['is_admin_role'])
        self.assertEqual(10, response.json['roles'][1]['priority'])
        self.assertEqual(True, response.json['roles'][1]['login_lockout_policy'])
        self.assertEqual(5, response.json['roles'][1]['login_max_attempts'])
        self.assertEqual(300, response.json['roles'][1]['login_timeframe'])
        self.assertEqual(1800, response.json['roles'][1]['login_ban_time'])
        self.assertEqual(True, response.json['roles'][1]['login_ban_by_ip'])
        self.assertEqual(True, response.json['roles'][1]['password_policy'])
        self.assertEqual(24, response.json['roles'][1]['password_reuse_history'])
        self.assertEqual(90, response.json['roles'][1]['password_reset_days'])
        self.assertIn("created_at", response.json['roles'][1])
        self.assertIn("updated_at", response.json['roles'][1])

        self.assertEqual(3, response.json['roles'][2]['id'])
        self.assertEqual("SERVICE", response.json['roles'][2]['name'])
        self.assertEqual(False, response.json['roles'][2]['is_admin_role'])
        self.assertEqual(50, response.json['roles'][2]['priority'])
        self.assertEqual(True, response.json['roles'][2]['login_lockout_policy'])
        self.assertEqual(5, response.json['roles'][2]['login_max_attempts'])
        self.assertEqual(300, response.json['roles'][2]['login_timeframe'])
        self.assertEqual(1800, response.json['roles'][2]['login_ban_time'])
        self.assertEqual(True, response.json['roles'][2]['login_ban_by_ip'])
        self.assertEqual(True, response.json['roles'][2]['password_policy'])
        self.assertEqual(24, response.json['roles'][2]['password_reuse_history'])
        self.assertEqual(365, response.json['roles'][2]['password_reset_days'])
        self.assertIn("created_at", response.json['roles'][2])
        self.assertIn("updated_at", response.json['roles'][2])
    
    def test_get_roles_id_asc(self):

        response = self.client.get('/roles?order_by=id.asc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("roles", response.json)

        self.assertEqual(1, response.json['roles'][0]['id'])
        self.assertEqual(2, response.json['roles'][1]['id'])
        self.assertEqual(3, response.json['roles'][2]['id'])

    def test_get_roles_id_desc(self):

        response = self.client.get('/roles?order_by=id.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("roles", response.json)

        self.assertEqual(3, response.json['roles'][0]['id'])
        self.assertEqual(2, response.json['roles'][1]['id'])
        self.assertEqual(1, response.json['roles'][2]['id'])

    def test_get_roles_name_asc(self):

        response = self.client.get('/roles?order_by=name.asc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("roles", response.json)

        self.assertEqual(3, response.json['roles'][0]['id'])
        self.assertEqual(2, response.json['roles'][1]['id'])
        self.assertEqual(1, response.json['roles'][2]['id'])

    def test_get_roles_name_desc(self):

        response = self.client.get('/roles?order_by=name.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("roles", response.json)

        self.assertEqual(1, response.json['roles'][0]['id'])
        self.assertEqual(2, response.json['roles'][1]['id'])
        self.assertEqual(3, response.json['roles'][2]['id'])

    def test_get_roles_page_2(self):

        response = self.client.get('/roles/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(204, response.status_code)
        self.assertTrue(None == response.json)
    
    def test_get_roles_page_1_limit_1(self):

        response = self.client.get('/roles/1/1?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(1, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("next_uri", response.json)
        self.assertTrue(response.json['next_uri'].endswith('/roles/2/1'))
        self.assertIn("roles", response.json)

        self.assertEqual(1, response.json['roles'][0]['id'])

    def test_get_roles_page_2_limit_1(self):

        response = self.client.get('/roles/2/1?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(1, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(2, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("previous_uri", response.json)
        self.assertTrue(response.json['previous_uri'].endswith('/roles/1/1'))
        self.assertIn("next_uri", response.json)
        self.assertTrue(response.json['next_uri'].endswith('/roles/3/1'))
        self.assertIn("roles", response.json)

        self.assertEqual(2, response.json['roles'][0]['id'])
    
    def test_get_roles_admin(self):

        response = self.client.get('/roles/admin?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("roles", response.json)

        self.assertEqual(2, response.json['roles'][0]['id'])
    
    def test_get_roles_user(self):

        response = self.client.get('/roles/user?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(2, response.json['total'])
        self.assertIn("roles", response.json)

        self.assertEqual(1, response.json['roles'][0]['id'])
        self.assertEqual(3, response.json['roles'][1]['id'])

    def test_get_roles_no_app_key(self):

        response = self.client.get('/roles',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_get_roles_bad_app_key(self):

        response = self.client.get('/roles?app_key=BAD_APP_KEY',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])

    def test_get_roles_unauthorized(self):

        response = self.client.get('/roles?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_get_roles_no_permission(self):

        response = self.client.get('/roles?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])

    def test_get_role_1(self):

        response = self.client.get(
            '/role/1?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.json['role']['id'])
        self.assertEqual("USER", response.json['role']['name'])
        self.assertEqual(False, response.json['role']['is_admin_role'])
        self.assertEqual(100, response.json['role']['priority'])
        self.assertEqual(False, response.json['role']['login_lockout_policy'])
        self.assertEqual(10, response.json['role']['login_max_attempts'])
        self.assertEqual(600, response.json['role']['login_timeframe'])
        self.assertEqual(1800, response.json['role']['login_ban_time'])
        self.assertEqual(True, response.json['role']['login_ban_by_ip'])
        self.assertEqual(False, response.json['role']['password_policy'])
        self.assertEqual(10, response.json['role']['password_reuse_history'])
        self.assertEqual(365, response.json['role']['password_reset_days'])
        self.assertIn("created_at", response.json['role'])
        self.assertIn("updated_at", response.json['role'])
    
    def test_get_role_admin(self):

        response = self.client.get(
            '/role/SUPER_ADMIN?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, response.json['role']['id'])
        self.assertEqual("SUPER_ADMIN", response.json['role']['name'])
        self.assertEqual(True, response.json['role']['is_admin_role'])
        self.assertEqual(10, response.json['role']['priority'])
        self.assertEqual(True, response.json['role']['login_lockout_policy'])
        self.assertEqual(5, response.json['role']['login_max_attempts'])
        self.assertEqual(300, response.json['role']['login_timeframe'])
        self.assertEqual(1800, response.json['role']['login_ban_time'])
        self.assertEqual(True, response.json['role']['login_ban_by_ip'])
        self.assertEqual(True, response.json['role']['password_policy'])
        self.assertEqual(24, response.json['role']['password_reuse_history'])
        self.assertEqual(90, response.json['role']['password_reset_days'])
        self.assertIn("created_at", response.json['role'])
        self.assertIn("updated_at", response.json['role'])
    
    def test_get_role_250(self):

        response = self.client.get(
            '/role/250?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(404, response.status_code)
        self.assertEqual("Not found", response.json['error'])

    def test_get_role_empty(self):

        response = self.client.get(
            '/role/EMPTY?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(404, response.status_code)
        self.assertEqual("Not found", response.json['error'])
    
    def test_get_role_no_app_key(self):

        response = self.client.get(
            '/role/1',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_get_role_bad_app_key(self):

        response = self.client.get(
            '/role/1?app_key=BAD_APP_KEY',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])

    def test_get_role_unauthorized(self):

        response = self.client.get('/role/1?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_get_role_no_permission(self):

        response = self.client.get(
            '/role/1?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
    
    def test_post_role_error(self):

        response = self.client.post(
            '/roles?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"foo":"bar"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("name", response.json['error'])

    def test_post_role_unique_name_error(self):

        response = self.client.post(
            '/roles?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"name":"USER","is_admin_role":true,"priority":50,"login_lockout_policy":true,"login_max_attempts":6,"login_timeframe":360,"login_ban_time":3600,"login_ban_by_ip":false,"password_policy":true,"password_reuse_history":5,"password_reset_days":180}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("name", response.json['error'])
        self.assertEqual(["Value must be unique."], response.json['error']['name'])
        self.assertNotIn("is_admin_role", response.json['error'])
        self.assertNotIn("priority", response.json['error'])
        self.assertNotIn("login_lockout_policy", response.json['error'])
        self.assertNotIn("login_max_attempts", response.json['error'])
        self.assertNotIn("login_timeframe", response.json['error'])
        self.assertNotIn("login_ban_time", response.json['error'])
        self.assertNotIn("login_ban_by_ip", response.json['error'])
        self.assertNotIn("password_policy", response.json['error'])
        self.assertNotIn("password_reuse_history", response.json['error'])
        self.assertNotIn("password_reset_days", response.json['error'])

    def test_post_role_success(self):

        response = self.client.post(
            '/roles?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"name":"AUTHOR","is_admin_role":true,"priority":50,"login_lockout_policy":true,"login_max_attempts":6,"login_timeframe":360,"login_ban_time":3600,"login_ban_by_ip":false,"password_policy":true,"password_reuse_history":5,"password_reset_days":180}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(201, response.status_code)
        self.assertIn("role", response.json)
        self.assertIn("id", response.json['role'])
        self.assertEqual(4, response.json['role']['id'])
        self.assertIn("name", response.json['role'])
        self.assertEqual("AUTHOR", response.json['role']['name'])
        self.assertEqual(True, response.json['role']['is_admin_role'])
        self.assertEqual(50, response.json['role']['priority'])
        self.assertEqual(True, response.json['role']['login_lockout_policy'])
        self.assertEqual(6, response.json['role']['login_max_attempts'])
        self.assertEqual(360, response.json['role']['login_timeframe'])
        self.assertEqual(3600, response.json['role']['login_ban_time'])
        self.assertEqual(False, response.json['role']['login_ban_by_ip'])
        self.assertEqual(True, response.json['role']['password_policy'])
        self.assertEqual(5, response.json['role']['password_reuse_history'])
        self.assertEqual(180, response.json['role']['password_reset_days'])
        self.assertIn("created_at", response.json['role'])
        self.assertIn("updated_at", response.json['role'])
    
    def test_post_role_no_app_key(self):

        response = self.client.post(
            '/roles',
            data='{"name":"AUTHOR","is_admin_role":true,"priority":50,"login_lockout_policy":true,"login_max_attempts":6,"login_timeframe":360,"login_ban_time":3600,"login_ban_by_ip":false,"password_policy":true,"password_reuse_history":5,"password_reset_days":180}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_post_role_bad_app_key(self):

        response = self.client.post(
            '/roles?app_key=BAD_APP_KEY',
            data='{"name":"AUTHOR","is_admin_role":true,"priority":50,"login_lockout_policy":true,"login_max_attempts":6,"login_timeframe":360,"login_ban_time":3600,"login_ban_by_ip":false,"password_policy":true,"password_reuse_history":5,"password_reset_days":180}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_post_role_unauthorized(self):

        response = self.client.post(
            '/roles?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"name":"AUTHOR","is_admin_role":true,"priority":50,"login_lockout_policy":true,"login_max_attempts":6,"login_timeframe":360,"login_ban_time":3600,"login_ban_by_ip":false,"password_policy":true,"password_reuse_history":5,"password_reset_days":180}',
            headers={
                "Content-Type": "application/json"})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_post_role_no_permission(self):

        response = self.client.post(
            '/roles?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"name":"AUTHOR","is_admin_role":true,"priority":50,"login_lockout_policy":true,"login_max_attempts":6,"login_timeframe":360,"login_ban_time":3600,"login_ban_by_ip":false,"password_policy":true,"password_reuse_history":5,"password_reset_days":180}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])

    def test_put_role_error(self):

        response = self.client.put(
            '/role/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"foo":"bar"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("name", response.json['error'])
        self.assertIn("is_admin_role", response.json['error'])
        self.assertIn("priority", response.json['error'])
        self.assertIn("login_lockout_policy", response.json['error'])
        self.assertIn("login_max_attempts", response.json['error'])
        self.assertIn("login_timeframe", response.json['error'])
        self.assertIn("login_ban_time", response.json['error'])
        self.assertIn("login_ban_by_ip", response.json['error'])
        self.assertIn("password_policy", response.json['error'])
        self.assertIn("password_reuse_history", response.json['error'])
        self.assertIn("password_reset_days", response.json['error'])
    
    def test_put_role_empty(self):

        response = self.client.put(
            '/role/250?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"name":"EMPTY","is_admin_role":true,"priority":100,"login_lockout_policy":true,"login_max_attempts":6,"login_timeframe":360,"login_ban_time":3600,"login_ban_by_ip":false,"password_policy":true,"password_reuse_history":5,"password_reset_days":180}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(404, response.status_code)
        self.assertEqual("Not found", response.json['error'])

    def test_put_role_unique_role_error(self):

        response = self.client.put(
            '/role/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"name":"USER","is_admin_role":false,"priority":200,"login_lockout_policy":true,"login_max_attempts":6,"login_timeframe":360,"login_ban_time":3600,"login_ban_by_ip":false,"password_policy":false,"password_reuse_history":8,"password_reset_days":45}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("name", response.json['error'])
        self.assertEqual(["Value must be unique."], response.json['error']['name'])
        self.assertNotIn("is_admin_role", response.json['error'])
        self.assertNotIn("priority", response.json['error'])
        self.assertNotIn("login_lockout_policy", response.json['error'])
        self.assertNotIn("login_max_attempts", response.json['error'])
        self.assertNotIn("login_timeframe", response.json['error'])
        self.assertNotIn("login_ban_time", response.json['error'])
        self.assertNotIn("login_ban_by_ip", response.json['error'])
        self.assertNotIn("password_policy", response.json['error'])
        self.assertNotIn("password_reuse_history", response.json['error'])
        self.assertNotIn("password_reset_days", response.json['error'])

    def test_put_role_admin(self):

        response = self.client.put(
            '/role/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"name":"EDITOR","is_admin_role":false,"priority":200,"login_lockout_policy":true,"login_max_attempts":6,"login_timeframe":360,"login_ban_time":3600,"login_ban_by_ip":false,"password_policy":false,"password_reuse_history":8,"password_reset_days":45}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, response.json['role']['id'])
        self.assertEqual("EDITOR", response.json['role']['name'])
        self.assertEqual(False, response.json['role']['is_admin_role'])
        self.assertEqual(200, response.json['role']['priority'])
        self.assertEqual(True, response.json['role']['login_lockout_policy'])
        self.assertEqual(6, response.json['role']['login_max_attempts'])
        self.assertEqual(360, response.json['role']['login_timeframe'])
        self.assertEqual(3600, response.json['role']['login_ban_time'])
        self.assertEqual(False, response.json['role']['login_ban_by_ip'])
        self.assertEqual(False, response.json['role']['password_policy'])
        self.assertEqual(8, response.json['role']['password_reuse_history'])
        self.assertEqual(45, response.json['role']['password_reset_days'])
        self.assertIn("created_at", response.json['role'])
        self.assertIn("updated_at", response.json['role'])
    
    def test_put_role_no_app_key(self):

        response = self.client.put(
            '/role/2',
            data='{"name":"EDITOR","is_admin_role":false,"priority":200,"login_lockout_policy":true,"login_max_attempts":6,"login_timeframe":360,"login_ban_time":3600,"login_ban_by_ip":false,"password_policy":false,"password_reuse_history":8,"password_reset_days":45}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_put_role_bad_app_key(self):

        response = self.client.put(
            '/role/2?app_key=BAD_APP_KEY',
            data='{"name":"EDITOR","is_admin_role":false,"priority":200,"login_lockout_policy":true,"login_max_attempts":6,"login_timeframe":360,"login_ban_time":3600,"login_ban_by_ip":false,"password_policy":false,"password_reuse_history":8,"password_reset_days":45}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_put_role_unauthorized(self):

        response = self.client.put(
            '/role/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"name":"EDITOR","is_admin_role":false,"priority":200,"login_lockout_policy":true,"login_max_attempts":6,"login_timeframe":360,"login_ban_time":3600,"login_ban_by_ip":false,"password_policy":false,"password_reuse_history":8,"password_reset_days":45}',
            headers={
                "Content-Type": "application/json"})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_put_role_no_permission(self):

        response = self.client.put(
            '/role/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"name":"EDITOR","is_admin_role":false,"priority":200,"login_lockout_policy":true,"login_max_attempts":6,"login_timeframe":360,"login_ban_time":3600,"login_ban_by_ip":false,"password_policy":false,"password_reuse_history":8,"password_reset_days":45}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
    
    def test_delete_role_empty(self):

        response = self.client.delete(
            '/role/250?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(404, response.status_code)
        self.assertEqual("Not found", response.json['error'])
    
    def test_delete_role_admin(self):

        response = self.client.delete(
            '/role/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(204, response.status_code)
        self.assertEqual(None, response.json)
    
    def test_delete_role_no_app_key(self):

        response = self.client.delete(
            '/role/2',
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_delete_role_bad_app_key(self):

        response = self.client.delete(
            '/role/2?app_key=BAD_APP_KEY',
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])

    def test_delete_role_unauthorized(self):

        response = self.client.delete('/role/2?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_delete_role_no_permission(self):

        response = self.client.delete(
            '/role/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
