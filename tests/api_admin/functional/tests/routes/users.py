from tests.BaseTest import BaseTest
from test_fixtures import *
from tests.utils import get_http_basic_auth_credentials


class UsersTest(BaseTest):

    def test_get_users(self):

        response = self.client.get(
            '/users?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(7, response.json['total'])
        self.assertIn("users", response.json)

        self.assertEqual(1, response.json['users'][0]['id'])
        self.assertEqual("user1", response.json['users'][0]['username'])
        self.assertEqual("user1@test.com", response.json['users'][0]['email'])
        self.assertEqual("Fiona", response.json['users'][0]['profile']['first_name'])
        self.assertEqual("Farnham", response.json['users'][0]['profile']['last_name'])
        self.assertEqual("2019-01-01T00:00:00+0000", response.json['users'][0]['terms_of_services'][0]['accept_date'])
        self.assertEqual("1.1.1.1", response.json['users'][0]['terms_of_services'][0]['ip_address'])
        self.assertEqual(2, response.json['users'][0]['terms_of_services'][0]['terms_of_service']['id'])
        self.assertEqual("1.1", response.json['users'][0]['terms_of_services'][0]['terms_of_service']['version'])
        self.assertEqual("2018-06-16T00:00:00+0000", response.json['users'][0]['terms_of_services'][1]['accept_date'])
        self.assertEqual("1.1.1.1", response.json['users'][0]['terms_of_services'][1]['ip_address'])
        self.assertEqual(1, response.json['users'][0]['terms_of_services'][1]['terms_of_service']['id'])
        self.assertEqual("1.0", response.json['users'][0]['terms_of_services'][1]['terms_of_service']['version'])
        self.assertIn("password_changed_at", response.json['users'][0])
        self.assertEqual(False, response.json['users'][0]['is_verified'])
        self.assertEqual(1, response.json['users'][0]['status'])
        self.assertIn("status_changed_at", response.json['users'][0])
        self.assertEqual([], response.json['users'][0]['roles'])
        self.assertTrue(response.json['users'][0]['uri'].endswith('/user/1'))
        self.assertIn("created_at", response.json['users'][0])
        self.assertIn("updated_at", response.json['users'][0])
        self.assertNotIn("password", response.json['users'][0])

        self.assertEqual(2, response.json['users'][1]['id'])
        self.assertEqual("user2", response.json['users'][1]['username'])
        self.assertEqual("user2@test.com", response.json['users'][1]['email'])
        self.assertEqual("Lynne", response.json['users'][1]['profile']['first_name'])
        self.assertEqual("Harford", response.json['users'][1]['profile']['last_name'])
        self.assertEqual("2019-01-06T00:00:00+0000", response.json['users'][1]['terms_of_services'][0]['accept_date'])
        self.assertEqual("1.1.1.2", response.json['users'][1]['terms_of_services'][0]['ip_address'])
        self.assertEqual(2, response.json['users'][1]['terms_of_services'][0]['terms_of_service']['id'])
        self.assertEqual("1.1", response.json['users'][1]['terms_of_services'][0]['terms_of_service']['version'])
        self.assertEqual("2018-12-10T00:00:00+0000", response.json['users'][1]['terms_of_services'][1]['accept_date'])
        self.assertEqual("1.1.1.2", response.json['users'][1]['terms_of_services'][1]['ip_address'])
        self.assertEqual(1, response.json['users'][1]['terms_of_services'][1]['terms_of_service']['id'])
        self.assertEqual("1.0", response.json['users'][1]['terms_of_services'][1]['terms_of_service']['version'])
        self.assertIn("password_changed_at", response.json['users'][1])
        self.assertEqual(True, response.json['users'][1]['is_verified'])
        self.assertEqual(1, response.json['users'][1]['status'])
        self.assertIn("status_changed_at", response.json['users'][1])
        self.assertEqual(1, response.json['users'][1]['roles'][0]['id'])
        self.assertEqual("USER", response.json['users'][1]['roles'][0]['name'])
        self.assertTrue(response.json['users'][1]['uri'].endswith('/user/2'))
        self.assertIn("created_at", response.json['users'][1])
        self.assertIn("updated_at", response.json['users'][1])
        self.assertNotIn("password", response.json['users'][1])

        self.assertEqual(3, response.json['users'][2]['id'])
        self.assertEqual("user3", response.json['users'][2]['username'])
        self.assertEqual("user3@test.com", response.json['users'][2]['email'])
        self.assertEqual("Duane", response.json['users'][2]['profile']['first_name'])
        self.assertEqual("Hargrave", response.json['users'][2]['profile']['last_name'])
        self.assertEqual("2019-01-02T00:00:00+0000", response.json['users'][2]['terms_of_services'][0]['accept_date'])
        self.assertEqual("1.1.1.3", response.json['users'][2]['terms_of_services'][0]['ip_address'])
        self.assertEqual(2, response.json['users'][2]['terms_of_services'][0]['terms_of_service']['id'])
        self.assertEqual("1.1", response.json['users'][2]['terms_of_services'][0]['terms_of_service']['version'])
        self.assertIn("password_changed_at", response.json['users'][2])
        self.assertEqual(True, response.json['users'][2]['is_verified'])
        self.assertEqual(1, response.json['users'][2]['status'])
        self.assertIn("status_changed_at", response.json['users'][2])
        self.assertEqual(1, response.json['users'][2]['roles'][0]['id'])
        self.assertEqual("USER", response.json['users'][2]['roles'][0]['name'])
        self.assertTrue(response.json['users'][2]['uri'].endswith('/user/3'))
        self.assertIn("created_at", response.json['users'][2])
        self.assertIn("updated_at", response.json['users'][2])
        self.assertNotIn("password", response.json['users'][2])

        self.assertEqual(5, response.json['users'][3]['id'])
        self.assertEqual("user5", response.json['users'][3]['username'])
        self.assertEqual("user5@test.com", response.json['users'][3]['email'])
        self.assertEqual("Elroy", response.json['users'][3]['profile']['first_name'])
        self.assertEqual("Hunnicutt", response.json['users'][3]['profile']['last_name'])
        self.assertEqual([], response.json['users'][3]['terms_of_services'])
        self.assertIn("password_changed_at", response.json['users'][3])
        self.assertEqual(False, response.json['users'][3]['is_verified'])
        self.assertEqual(2, response.json['users'][3]['status'])
        self.assertIn("status_changed_at", response.json['users'][3])
        self.assertEqual(1, response.json['users'][3]['roles'][0]['id'])
        self.assertEqual("USER", response.json['users'][3]['roles'][0]['name'])
        self.assertTrue(response.json['users'][3]['uri'].endswith('/user/5'))
        self.assertIn("created_at", response.json['users'][3])
        self.assertIn("updated_at", response.json['users'][3])
        self.assertNotIn("password", response.json['users'][3])

        self.assertEqual(6, response.json['users'][4]['id'])
        self.assertEqual("user6", response.json['users'][4]['username'])
        self.assertEqual("user6@test.com", response.json['users'][4]['email'])
        self.assertEqual("Alease", response.json['users'][4]['profile']['first_name'])
        self.assertEqual("Richards", response.json['users'][4]['profile']['last_name'])
        self.assertIn("password_changed_at", response.json['users'][4])
        self.assertEqual(True, response.json['users'][4]['is_verified'])
        self.assertEqual(5, response.json['users'][4]['status'])
        self.assertIn("status_changed_at", response.json['users'][4])
        self.assertEqual(1, response.json['users'][4]['roles'][0]['id'])
        self.assertEqual("USER", response.json['users'][4]['roles'][0]['name'])
        self.assertTrue(response.json['users'][4]['uri'].endswith('/user/6'))
        self.assertIn("created_at", response.json['users'][4])
        self.assertIn("updated_at", response.json['users'][4])
        self.assertNotIn("password", response.json['users'][4])

        self.assertEqual(8, response.json['users'][5]['id'])
        self.assertEqual("user8", response.json['users'][5]['username'])
        self.assertEqual("user8@test.com", response.json['users'][5]['email'])
        self.assertEqual("Luke", response.json['users'][5]['profile']['first_name'])
        self.assertEqual("Tennyson", response.json['users'][5]['profile']['last_name'])
        self.assertIn("password_changed_at", response.json['users'][5])
        self.assertEqual(False, response.json['users'][5]['is_verified'])
        self.assertEqual(1, response.json['users'][5]['status'])
        self.assertIn("status_changed_at", response.json['users'][5])
        self.assertEqual(1, response.json['users'][5]['roles'][0]['id'])
        self.assertEqual("USER", response.json['users'][5]['roles'][0]['name'])
        self.assertTrue(response.json['users'][5]['uri'].endswith('/user/8'))
        self.assertIn("created_at", response.json['users'][5])
        self.assertIn("updated_at", response.json['users'][5])
        self.assertNotIn("password", response.json['users'][5])

        self.assertEqual(9, response.json['users'][6]['id'])
        self.assertEqual("service1", response.json['users'][6]['username'])
        self.assertEqual("service1@test.com", response.json['users'][6]['email'])
        self.assertIn("password_changed_at", response.json['users'][6])
        self.assertEqual(False, response.json['users'][6]['is_verified'])
        self.assertEqual(1, response.json['users'][6]['status'])
        self.assertIn("status_changed_at", response.json['users'][6])
        self.assertEqual(3, response.json['users'][6]['roles'][0]['id'])
        self.assertEqual("SERVICE", response.json['users'][6]['roles'][0]['name'])
        self.assertTrue(response.json['users'][6]['uri'].endswith('/user/9'))
        self.assertIn("created_at", response.json['users'][6])
        self.assertIn("updated_at", response.json['users'][6])
        self.assertNotIn("password", response.json['users'][6])
    
    def test_get_users_id_asc(self):

        response = self.client.get(
            '/users?order_by=id.asc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(7, response.json['total'])
        self.assertIn("users", response.json)

        self.assertEqual(1, response.json['users'][0]['id'])
        self.assertEqual(2, response.json['users'][1]['id'])
        self.assertEqual(3, response.json['users'][2]['id'])
        self.assertEqual(5, response.json['users'][3]['id'])
        self.assertEqual(6, response.json['users'][4]['id'])
        self.assertEqual(8, response.json['users'][5]['id'])
        self.assertEqual(9, response.json['users'][6]['id'])

    def test_get_users_id_desc(self):

        response = self.client.get(
            '/users?order_by=id.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(7, response.json['total'])
        self.assertIn("users", response.json)

        self.assertEqual(9, response.json['users'][0]['id'])
        self.assertEqual(8, response.json['users'][1]['id'])
        self.assertEqual(6, response.json['users'][2]['id'])
        self.assertEqual(5, response.json['users'][3]['id'])
        self.assertEqual(3, response.json['users'][4]['id'])
        self.assertEqual(2, response.json['users'][5]['id'])
        self.assertEqual(1, response.json['users'][6]['id'])

    def test_get_users_username_asc(self):

        response = self.client.get(
            '/users?order_by=username.asc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(7, response.json['total'])
        self.assertIn("users", response.json)

        self.assertEqual(9, response.json['users'][0]['id'])
        self.assertEqual(1, response.json['users'][1]['id'])
        self.assertEqual(2, response.json['users'][2]['id'])
        self.assertEqual(3, response.json['users'][3]['id'])
        self.assertEqual(5, response.json['users'][4]['id'])
        self.assertEqual(6, response.json['users'][5]['id'])
        self.assertEqual(8, response.json['users'][6]['id'])
    
    def test_get_users_username_desc(self):

        response = self.client.get(
            '/users?order_by=username.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(7, response.json['total'])
        self.assertIn("users", response.json)

        self.assertEqual(8, response.json['users'][0]['id'])
        self.assertEqual(6, response.json['users'][1]['id'])
        self.assertEqual(5, response.json['users'][2]['id'])
        self.assertEqual(3, response.json['users'][3]['id'])
        self.assertEqual(2, response.json['users'][4]['id'])
        self.assertEqual(1, response.json['users'][5]['id'])
        self.assertEqual(9, response.json['users'][6]['id'])

    def test_get_users_page_2(self):

        response = self.client.get(
            '/users/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(204, response.status_code)
        self.assertTrue(None == response.json)

    def test_get_users_page_1_limit_2(self):

        response = self.client.get(
            '/users/1/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(2, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(7, response.json['total'])
        self.assertIn("users", response.json)
        self.assertTrue(response.json['next_uri'].endswith('/users/2/2'))

        self.assertEqual(1, response.json['users'][0]['id'])
        self.assertEqual(2, response.json['users'][1]['id'])

    def test_get_users_page_2_limit_2(self):

        response = self.client.get(
            '/users/2/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(2, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(2, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(7, response.json['total'])
        self.assertIn("users", response.json)
        self.assertTrue(response.json['previous_uri'].endswith('/users/1/2'))
        self.assertTrue(response.json['next_uri'].endswith('/users/3/2'))

        self.assertEqual(3, response.json['users'][0]['id'])
        self.assertEqual(5, response.json['users'][1]['id'])
    
    def test_get_users_status_enabled(self):

        response = self.client.get(
            '/users?status=1&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("users", response.json)

        self.assertEqual(1, response.json['users'][0]['id'])
        self.assertEqual(2, response.json['users'][1]['id'])
        self.assertEqual(3, response.json['users'][2]['id'])
        self.assertEqual(8, response.json['users'][3]['id'])
        self.assertEqual(9, response.json['users'][4]['id'])
    
    def test_get_users_status_disabled(self):

        response = self.client.get(
            '/users?status=2&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("users", response.json)

        self.assertEqual(5, response.json['users'][0]['id'])
    
    def test_get_users_status_archived(self):

        response = self.client.get(
            '/users?status=3&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("users", response.json)

        self.assertEqual(4, response.json['users'][0]['id'])

    def test_get_users_status_deleted(self):

        response = self.client.get(
            '/users?status=4&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("users", response.json)

        self.assertEqual(7, response.json['users'][0]['id'])
    
    def test_get_users_status_pending(self):

        response = self.client.get(
            '/users?status=5&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("users", response.json)

        self.assertEqual(6, response.json['users'][0]['id'])
    
    def test_get_users_role_user(self):

        response = self.client.get(
            '/users?role=1&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("users", response.json)

        self.assertEqual(2, response.json['users'][0]['id'])
        self.assertEqual(3, response.json['users'][1]['id'])
        self.assertEqual(5, response.json['users'][2]['id'])
        self.assertEqual(6, response.json['users'][3]['id'])
        self.assertEqual(8, response.json['users'][4]['id'])
    
    def test_get_users_role_user_status_pending(self):

        response = self.client.get(
            '/users?role=1&status=5&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("users", response.json)

        self.assertEqual(6, response.json['users'][0]['id'])

    def test_get_users_no_app_key(self):

        response = self.client.get(
            '/users',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_get_users_bad_app_key(self):

        response = self.client.get(
            '/users?app_key=BAD_APP_KEY',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])

    def test_get_users_unauthorized(self):

        response = self.client.get('/users?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_get_users_no_permission(self):

        response = self.client.get(
            '/users?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])

    def test_get_user_1(self):

        response = self.client.get(
            '/user/1?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.json['user']['id'])
        self.assertEqual("user1", response.json['user']['username'])
        self.assertEqual("user1@test.com", response.json['user']['email'])
        self.assertEqual("Fiona", response.json['user']['profile']['first_name'])
        self.assertEqual("Farnham", response.json['user']['profile']['last_name'])
        self.assertEqual("2019-01-01T00:00:00+0000", response.json['user']['terms_of_services'][0]['accept_date'])
        self.assertEqual("1.1.1.1", response.json['user']['terms_of_services'][0]['ip_address'])
        self.assertEqual(2, response.json['user']['terms_of_services'][0]['terms_of_service']['id'])
        self.assertEqual("1.1", response.json['user']['terms_of_services'][0]['terms_of_service']['version'])
        self.assertEqual("2018-06-16T00:00:00+0000", response.json['user']['terms_of_services'][1]['accept_date'])
        self.assertEqual("1.1.1.1", response.json['user']['terms_of_services'][1]['ip_address'])
        self.assertEqual(1, response.json['user']['terms_of_services'][1]['terms_of_service']['id'])
        self.assertEqual("1.0", response.json['user']['terms_of_services'][1]['terms_of_service']['version'])
        self.assertIn("password_changed_at", response.json['user'])
        self.assertEqual(False, response.json['user']['is_verified'])
        self.assertEqual(1, response.json['user']['status'])
        self.assertIn("status_changed_at", response.json['user'])
        self.assertEqual([], response.json['user']['roles'])
        self.assertTrue(response.json['user']['uri'].endswith('/user/1'))
        self.assertIn("created_at", response.json['user'])
        self.assertIn("updated_at", response.json['user'])
        self.assertNotIn("password", response.json['user'])
    
    def test_get_user_user2(self):

        response = self.client.get(
            '/user/user2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, response.json['user']['id'])
        self.assertEqual("user2", response.json['user']['username'])
        self.assertEqual("user2@test.com", response.json['user']['email'])
        self.assertEqual("Lynne", response.json['user']['profile']['first_name'])
        self.assertEqual("Harford", response.json['user']['profile']['last_name'])
        self.assertEqual("2019-01-06T00:00:00+0000", response.json['user']['terms_of_services'][0]['accept_date'])
        self.assertEqual("1.1.1.2", response.json['user']['terms_of_services'][0]['ip_address'])
        self.assertEqual(2, response.json['user']['terms_of_services'][0]['terms_of_service']['id'])
        self.assertEqual("1.1", response.json['user']['terms_of_services'][0]['terms_of_service']['version'])
        self.assertEqual("2018-12-10T00:00:00+0000", response.json['user']['terms_of_services'][1]['accept_date'])
        self.assertEqual("1.1.1.2", response.json['user']['terms_of_services'][1]['ip_address'])
        self.assertEqual(1, response.json['user']['terms_of_services'][1]['terms_of_service']['id'])
        self.assertEqual("1.0", response.json['user']['terms_of_services'][1]['terms_of_service']['version'])
        self.assertIn("password_changed_at", response.json['user'])
        self.assertEqual(True, response.json['user']['is_verified'])
        self.assertEqual(1, response.json['user']['status'])
        self.assertIn("status_changed_at", response.json['user'])
        self.assertEqual(1, response.json['user']['roles'][0]['id'])
        self.assertEqual("USER", response.json['user']['roles'][0]['name'])
        self.assertTrue(response.json['user']['uri'].endswith('/user/2'))
        self.assertIn("created_at", response.json['user'])
        self.assertIn("updated_at", response.json['user'])
        self.assertNotIn("password", response.json['user'])
    
    def test_get_user_250(self):

        response = self.client.get(
            '/user/250?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(404, response.status_code)
        self.assertEqual("Not found", response.json['error'])
    
    def test_get_user_empty(self):

        response = self.client.get(
            '/user/EMPTY?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(404, response.status_code)
        self.assertEqual("Not found", response.json['error'])

    def test_get_user_no_app_key(self):

        response = self.client.get(
            '/user/1',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_get_user_bad_app_key(self):

        response = self.client.get(
            '/user/1?app_key=BAD_APP_KEY',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])

    def test_get_user_unauthorized(self):

        response = self.client.get('/user/1?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_get_user_no_permission(self):

        response = self.client.get(
            '/user/1?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
    
    def test_post_user_error(self):

        response = self.client.post(
            '/users?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"foo":"bar"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertIn("email", response.json['error'])
        self.assertIn("is_verified", response.json['error'])
        self.assertIn("status", response.json['error'])
        self.assertIn("password", response.json['error'])
        self.assertNotIn("password_changed_at", response.json['error'])
    
    def test_post_user_password_comlexity(self):

        response = self.client.post(
            '/users?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user9","email":"user9@test.com","is_verified":false,"password":"password","roles":[1],"status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("password", response.json['error'])
        self.assertEqual("Please choose a more complex password.", response.json['error']['password'][0])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("is_verified", response.json['error'])
        self.assertNotIn("status", response.json['error'])
    
    def test_post_user_unique_username_error(self):

        response = self.client.post(
            '/users?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user1","email":"user9@test.com","is_verified":false,"password":"user9Pass","roles":[1],"status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must be unique."], response.json['error']['username'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("is_verified", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("password", response.json['error'])
    
    def test_post_user_unique_email_error(self):

        response = self.client.post(
            '/users?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user9","email":"user1@test.com","is_verified":false,"password":"user9Pass","roles":[1],"status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("email", response.json['error'])
        self.assertEqual(["Value must be unique."], response.json['error']['email'])
        self.assertNotIn("username", response.json['error'])
        self.assertNotIn("is_verified", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("password", response.json['error'])
    
    def test_post_user_unique_username_and_is_verified_at_error(self):

        response = self.client.post(
            '/users?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user1","email":"user9@test.com","password":"user9Pass","roles":[1],"status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must be unique."], response.json['error']['username'])
        self.assertIn("is_verified", response.json['error'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("password", response.json['error'])

    def test_post_user_username_length_error(self):

        response = self.client.post(
            '/users?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"u","email":"user9@test.com","is_verified":false,"password":"user9Pass","roles":[1],"status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must be between 2 and 40 characters long."], response.json['error']['username'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("is_verified", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("password", response.json['error'])
    
    def test_post_user_username_numeric_error(self):

        response = self.client.post(
            '/users?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"90","email":"user9@test.com","is_verified":false,"password":"user9Pass","roles":[1],"status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must not be a number."], response.json['error']['username'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("is_verified", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("password", response.json['error'])
    
    def test_post_user_username_whitespace_error(self):

        response = self.client.post(
            '/users?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user 9","email":"user9@test.com","is_verified":false,"password":"user9Pass","roles":[1],"status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must contain only alphanumeric characters and the underscore."], response.json['error']['username'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("is_verified", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("password", response.json['error'])
    
    # @todo: test 500 error for bad role

    def test_post_user_success(self):

        response = self.client.post(
            '/users?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user9","email":"user9@test.com","is_verified":false,"password":"user9Pass","roles":[1],"status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(201, response.status_code)
        self.assertEqual(10, response.json['user']['id'])
        self.assertEqual("user9", response.json['user']['username'])
        self.assertEqual("user9@test.com", response.json['user']['email'])
        self.assertEqual(None, response.json['user']['profile'])
        self.assertEqual([], response.json['user']['terms_of_services'])
        self.assertIn("password_changed_at", response.json['user'])
        self.assertEqual(False, response.json['user']['is_verified'])
        self.assertEqual(1, response.json['user']['status'])
        self.assertIn("status_changed_at", response.json['user'])
        self.assertEqual(1, response.json['user']['roles'][0]['id'])
        self.assertEqual("USER", response.json['user']['roles'][0]['name'])
        self.assertTrue(response.json['user']['uri'].endswith('/user/10'))
        self.assertIn("created_at", response.json['user'])
        self.assertIn("updated_at", response.json['user'])
        self.assertNotIn("password", response.json['user'])

    def test_post_user_success_whitespace(self):

        response = self.client.post(
            '/users?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user9","email":"user9@test.com","is_verified":false,"password":"user9Pass","roles":[1],"status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(201, response.status_code)
        self.assertEqual(10, response.json['user']['id'])
        self.assertEqual("user9", response.json['user']['username'])
        self.assertEqual("user9@test.com", response.json['user']['email'])
        self.assertEqual(None, response.json['user']['profile'])
        self.assertEqual([], response.json['user']['terms_of_services'])
        self.assertIn("password_changed_at", response.json['user'])
        self.assertEqual(False, response.json['user']['is_verified'])
        self.assertEqual(1, response.json['user']['status'])
        self.assertIn("status_changed_at", response.json['user'])
        self.assertEqual(1, response.json['user']['roles'][0]['id'])
        self.assertEqual("USER", response.json['user']['roles'][0]['name'])
        self.assertTrue(response.json['user']['uri'].endswith('/user/10'))
        self.assertIn("created_at", response.json['user'])
        self.assertIn("updated_at", response.json['user'])
        self.assertNotIn("password", response.json['user'])
    
    def test_post_user_no_app_key(self):

        response = self.client.post(
            '/users',
            data='{"username":"user9","email":"user9@test.com","is_verified":false,"password":"user9Pass","roles":[1],"status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_post_user_bad_app_key(self):

        response = self.client.post(
            '/users?app_key=BAD_APP_KEY',
            data='{"username":"user9","email":"user9@test.com","is_verified":false,"password":"user9Pass","roles":[1],"status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_post_user_unauthorized(self):

        response = self.client.post(
            '/users?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user9","email":"user9@test.com","is_verified":false,"password":"user9Pass","roles":[1],"status":1}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_post_user_no_permission(self):

        response = self.client.post(
            '/users?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user9","email":"user9@test.com","is_verified":false,"password":"user9Pass","roles":[1],"status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
    
    def test_put_user_error(self):

        response = self.client.put(
            '/user/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"foo":"bar"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertIn("email", response.json['error'])
        self.assertIn("is_verified", response.json['error'])
        self.assertIn("status", response.json['error'])
        self.assertNotIn("password", response.json['error'])
        self.assertNotIn("password_changed_at", response.json['error'])
    
    def test_put_user_password_complexity(self):

        response = self.client.put(
            '/user/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user2a","email":"user2a@test.com","password":"password","is_verified":false,"roles":[1],"status":2}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("password", response.json['error'])
        self.assertEqual("Please choose a more complex password.", response.json['error']['password'][0])
    
    def test_put_user_empty(self):

        response = self.client.put(
            '/user/250?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user7","email":"user7@test.com","password":"user7Pass","is_verified":true,"roles":[1],"status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(404, response.status_code)
        self.assertEqual("Not found", response.json['error'])
    
    def test_put_user_unique_username_error(self):

        response = self.client.put(
            '/user/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user1","email":"user2@test.com","is_verified":false,"roles":[1],"status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must be unique."], response.json['error']['username'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("is_verified", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("password", response.json['error'])
    
    def test_put_user_unique_email_error(self):

        response = self.client.put(
            '/user/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user2","email":"user1@test.com","is_verified":false,"roles":[1],"status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("email", response.json['error'])
        self.assertEqual(["Value must be unique."], response.json['error']['email'])
        self.assertNotIn("username", response.json['error'])
        self.assertNotIn("is_verified", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("password", response.json['error'])
    
    def test_put_user_unique_username_and_no_is_verified_error(self):

        response = self.client.put(
            '/user/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user1","email":"user2@test.com","roles":[1],"status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must be unique."], response.json['error']['username'])
        self.assertIn("is_verified", response.json['error'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("password", response.json['error'])
    
    def test_put_user_username_length_error(self):

        response = self.client.put(
            '/user/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"u","email":"user2@test.com","is_verified":false,"roles":[1],"status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must be between 2 and 40 characters long."], response.json['error']['username'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("is_verified", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("password", response.json['error'])
    
    def test_put_user_username_numeric_error(self):

        response = self.client.put(
            '/user/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"20","email":"user2@test.com","is_verified":false,"roles":[1],"status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must not be a number."], response.json['error']['username'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("is_verified", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("password", response.json['error'])
    
    def test_put_user_username_whitespace_error(self):

        response = self.client.put(
            '/user/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user 2","email":"user2@test.com","is_verified":false,"roles":[1],"status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must contain only alphanumeric characters and the underscore."], response.json['error']['username'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("is_verified", response.json['error'])
        self.assertNotIn("status", response.json['error'])
        self.assertNotIn("password", response.json['error'])

    def test_put_user_user_2(self):

        response = self.client.put(
            '/user/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user2a","email":"user2a@test.com","is_verified":false,"password":"user2Pass","roles":[1],"status":2}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, response.json['user']['id'])
        self.assertEqual("user2a", response.json['user']['username'])
        self.assertEqual("user2a@test.com", response.json['user']['email'])
        self.assertEqual("Lynne", response.json['user']['profile']['first_name'])
        self.assertEqual("Harford", response.json['user']['profile']['last_name'])
        self.assertEqual("2019-01-06T00:00:00+0000", response.json['user']['terms_of_services'][0]['accept_date'])
        self.assertEqual("1.1.1.2", response.json['user']['terms_of_services'][0]['ip_address'])
        self.assertEqual(2, response.json['user']['terms_of_services'][0]['terms_of_service']['id'])
        self.assertEqual("1.1", response.json['user']['terms_of_services'][0]['terms_of_service']['version'])
        self.assertEqual("2018-12-10T00:00:00+0000", response.json['user']['terms_of_services'][1]['accept_date'])
        self.assertEqual("1.1.1.2", response.json['user']['terms_of_services'][1]['ip_address'])
        self.assertEqual(1, response.json['user']['terms_of_services'][1]['terms_of_service']['id'])
        self.assertEqual("1.0", response.json['user']['terms_of_services'][1]['terms_of_service']['version'])
        self.assertIn("password_changed_at", response.json['user'])
        self.assertEqual(False, response.json['user']['is_verified'])
        self.assertEqual(2, response.json['user']['status'])
        self.assertIn("status_changed_at", response.json['user'])
        self.assertEqual(1, response.json['user']['roles'][0]['id'])
        self.assertEqual("USER", response.json['user']['roles'][0]['name'])
        self.assertTrue(response.json['user']['uri'].endswith('/user/2'))
        self.assertIn("created_at", response.json['user'])
        self.assertIn("updated_at", response.json['user'])
        self.assertNotIn("password", response.json['user'])

    def test_put_user_user_2_no_password(self):

        response = self.client.put(
            '/user/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user2a","email":"user2a@test.com","is_verified":false,"roles":[1],"status":2}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, response.json['user']['id'])
        self.assertEqual("user2a", response.json['user']['username'])
        self.assertEqual("user2a@test.com", response.json['user']['email'])
        self.assertEqual("Lynne", response.json['user']['profile']['first_name'])
        self.assertEqual("Harford", response.json['user']['profile']['last_name'])
        self.assertEqual("2019-01-06T00:00:00+0000", response.json['user']['terms_of_services'][0]['accept_date'])
        self.assertEqual("1.1.1.2", response.json['user']['terms_of_services'][0]['ip_address'])
        self.assertEqual(2, response.json['user']['terms_of_services'][0]['terms_of_service']['id'])
        self.assertEqual("1.1", response.json['user']['terms_of_services'][0]['terms_of_service']['version'])
        self.assertEqual("2018-12-10T00:00:00+0000", response.json['user']['terms_of_services'][1]['accept_date'])
        self.assertEqual("1.1.1.2", response.json['user']['terms_of_services'][1]['ip_address'])
        self.assertEqual(1, response.json['user']['terms_of_services'][1]['terms_of_service']['id'])
        self.assertEqual("1.0", response.json['user']['terms_of_services'][1]['terms_of_service']['version'])
        self.assertIn("password_changed_at", response.json['user'])
        self.assertEqual(False, response.json['user']['is_verified'])
        self.assertEqual(2, response.json['user']['status'])
        self.assertIn("status_changed_at", response.json['user'])
        self.assertEqual(1, response.json['user']['roles'][0]['id'])
        self.assertEqual("USER", response.json['user']['roles'][0]['name'])
        self.assertTrue(response.json['user']['uri'].endswith('/user/2'))
        self.assertIn("created_at", response.json['user'])
        self.assertIn("updated_at", response.json['user'])
        self.assertNotIn("password", response.json['user'])
    
    def test_put_user_no_app_key(self):

        response = self.client.put(
            '/user/2',
            data='{"username":"user2a","email":"user2a@test.com","is_verified":false,"password":"user2Pass","roles":[1],"status":2}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_put_user_bad_app_key(self):

        response = self.client.put(
            '/user/2?app_key=BAD_APP_KEY',
            data='{"username":"user2a","email":"user2a@test.com","is_verified":false,"password":"user2Pass","roles":[1],"status":2}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])

    def test_put_user_unauthorized(self):

        response = self.client.put(
            '/user/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user2a","email":"user2a@test.com","is_verified":false,"password":"user2Pass","roles":[1],"status":2}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])

    def test_put_user_no_permission(self):

        response = self.client.put(
            '/user/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"user2a","email":"user2a@test.com","is_verified":false,"password":"user2Pass","roles":[1],"status":2}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])

    def test_delete_user_empty(self):

        response = self.client.delete(
            '/user/250?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(404, response.status_code)
        self.assertEqual("Not found", response.json['error'])
    
    def test_delete_user_id2(self):

        response = self.client.delete(
            '/user/2?app_key=' + AppKeyData.id1_appkey1.key, 
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(204, response.status_code)
        self.assertEqual(None, response.json)
    
    def test_delete_user_no_app_key(self):

        response = self.client.delete(
            '/user/2', 
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_delete_user_bad_app_key(self):

        response = self.client.delete(
            '/user/2?app_key=BAD_APP_KEY', 
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])

    def test_delete_user_unauthorized(self):

        response = self.client.delete('/user/2?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_delete_user_no_permission(self):

        response = self.client.delete('/user/2?app_key=' + AppKeyData.id1_appkey1.key, headers={
            "Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
