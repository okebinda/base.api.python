from tests.BaseTest import BaseTest
from test_fixtures import *
from tests.utils import get_http_basic_auth_credentials
    
class AdministratorsTest(BaseTest):

    def test_get_administrators(self):

        response = self.client.get(
            '/administrators?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("administrators", response.json)

        self.assertEqual(1, response.json['administrators'][0]['id'])
        self.assertEqual("admin1", response.json['administrators'][0]['username'])
        self.assertEqual("admin1@test.com", response.json['administrators'][0]['email'])
        self.assertEqual("Tommy", response.json['administrators'][0]['first_name'])
        self.assertEqual("Lund", response.json['administrators'][0]['last_name'])
        self.assertIn("password_changed_at", response.json['administrators'][0])
        self.assertEqual("2018-11-01T00:00:00+0000", response.json['administrators'][0]['joined_at'])
        self.assertEqual(1, response.json['administrators'][0]['status'])
        self.assertEqual("2018-11-01T00:00:00+0000", response.json['administrators'][0]['status_changed_at'])
        self.assertEqual(2, response.json['administrators'][0]['roles'][0]['id'])
        self.assertEqual("SUPER_ADMIN", response.json['administrators'][0]['roles'][0]['name'])
        self.assertTrue(response.json['administrators'][0]['uri'].endswith('/administrator/1'))
        self.assertIn("created_at", response.json['administrators'][0])
        self.assertIn("updated_at", response.json['administrators'][0])
        self.assertNotIn("password", response.json['administrators'][0])

        self.assertEqual(2, response.json['administrators'][1]['id'])
        self.assertEqual("admin2", response.json['administrators'][1]['username'])
        self.assertEqual("admin2@test.com", response.json['administrators'][1]['email'])
        self.assertEqual("Selma", response.json['administrators'][1]['first_name'])
        self.assertEqual("Keyes", response.json['administrators'][1]['last_name'])
        self.assertIn("password_changed_at", response.json['administrators'][1])
        self.assertEqual("2018-11-05T00:00:00+0000", response.json['administrators'][1]['joined_at'])
        self.assertEqual(1, response.json['administrators'][1]['status'])
        self.assertEqual("2018-11-05T00:00:00+0000", response.json['administrators'][1]['status_changed_at'])
        self.assertEqual(2, response.json['administrators'][1]['roles'][0]['id'])
        self.assertEqual("SUPER_ADMIN", response.json['administrators'][1]['roles'][0]['name'])
        self.assertTrue(response.json['administrators'][1]['uri'].endswith('/administrator/2'))
        self.assertIn("created_at", response.json['administrators'][1])
        self.assertIn("updated_at", response.json['administrators'][1])
        self.assertNotIn("password", response.json['administrators'][1])
        
        self.assertEqual(3, response.json['administrators'][2]['id'])
        self.assertEqual("admin3", response.json['administrators'][2]['username'])
        self.assertEqual("admin3@test.com", response.json['administrators'][2]['email'])
        self.assertEqual("Victor", response.json['administrators'][2]['first_name'])
        self.assertEqual("Landon", response.json['administrators'][2]['last_name'])
        self.assertIn("password_changed_at", response.json['administrators'][2])
        self.assertEqual("2018-11-15T00:00:00+0000", response.json['administrators'][2]['joined_at'])
        self.assertEqual(1, response.json['administrators'][2]['status'])
        self.assertEqual("2018-11-15T00:00:00+0000", response.json['administrators'][2]['status_changed_at'])
        self.assertEqual([], response.json['administrators'][2]['roles'])
        self.assertTrue(response.json['administrators'][2]['uri'].endswith('/administrator/3'))
        self.assertIn("created_at", response.json['administrators'][2])
        self.assertIn("updated_at", response.json['administrators'][2])
        self.assertNotIn("password", response.json['administrators'][2])

        self.assertEqual(4, response.json['administrators'][3]['id'])
        self.assertEqual("admin4", response.json['administrators'][3]['username'])
        self.assertEqual("admin4@test.com", response.json['administrators'][3]['email'])
        self.assertEqual("Tamela", response.json['administrators'][3]['first_name'])
        self.assertEqual("Coburn", response.json['administrators'][3]['last_name'])
        self.assertIn("password_changed_at", response.json['administrators'][3])
        self.assertEqual("2018-11-20T00:00:00+0000", response.json['administrators'][3]['joined_at'])
        self.assertEqual(2, response.json['administrators'][3]['status'])
        self.assertEqual("2018-11-20T00:00:00+0000", response.json['administrators'][3]['status_changed_at'])
        self.assertEqual(2, response.json['administrators'][3]['roles'][0]['id'])
        self.assertEqual("SUPER_ADMIN", response.json['administrators'][3]['roles'][0]['name'])
        self.assertTrue(response.json['administrators'][3]['uri'].endswith('/administrator/4'))
        self.assertIn("created_at", response.json['administrators'][3])
        self.assertIn("updated_at", response.json['administrators'][3])
        self.assertNotIn("password", response.json['administrators'][3])

        self.assertEqual(7, response.json['administrators'][4]['id'])
        self.assertEqual("admin7", response.json['administrators'][4]['username'])
        self.assertEqual("admin7@test.com", response.json['administrators'][4]['email'])
        self.assertEqual("Nigel", response.json['administrators'][4]['first_name'])
        self.assertEqual("Sams", response.json['administrators'][4]['last_name'])
        self.assertIn("password_changed_at", response.json['administrators'][4])
        self.assertEqual("2018-11-10T00:00:00+0000", response.json['administrators'][4]['joined_at'])
        self.assertEqual(5, response.json['administrators'][4]['status'])
        self.assertEqual("2018-11-10T00:00:00+0000", response.json['administrators'][4]['status_changed_at'])
        self.assertEqual(2, response.json['administrators'][4]['roles'][0]['id'])
        self.assertEqual("SUPER_ADMIN", response.json['administrators'][4]['roles'][0]['name'])
        self.assertTrue(response.json['administrators'][4]['uri'].endswith('/administrator/7'))
        self.assertIn("created_at", response.json['administrators'][4])
        self.assertIn("updated_at", response.json['administrators'][4])
        self.assertNotIn("password", response.json['administrators'][4])

    def test_get_administrators_id_asc(self):

        response = self.client.get(
            '/administrators?order_by=id.asc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("administrators", response.json)

        self.assertEqual(1, response.json['administrators'][0]['id'])
        self.assertEqual(2, response.json['administrators'][1]['id'])
        self.assertEqual(3, response.json['administrators'][2]['id'])
        self.assertEqual(4, response.json['administrators'][3]['id'])
        self.assertEqual(7, response.json['administrators'][4]['id'])
    
    def test_get_administrators_id_desc(self):

        response = self.client.get(
            '/administrators?order_by=id.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("administrators", response.json)

        self.assertEqual(7, response.json['administrators'][0]['id'])
        self.assertEqual(4, response.json['administrators'][1]['id'])
        self.assertEqual(3, response.json['administrators'][2]['id'])
        self.assertEqual(2, response.json['administrators'][3]['id'])
        self.assertEqual(1, response.json['administrators'][4]['id'])
    
    def test_get_administrators_username_asc(self):

        response = self.client.get(
            '/administrators?order_by=username.asc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("administrators", response.json)

        self.assertEqual(1, response.json['administrators'][0]['id'])
        self.assertEqual(2, response.json['administrators'][1]['id'])
        self.assertEqual(3, response.json['administrators'][2]['id'])
        self.assertEqual(4, response.json['administrators'][3]['id'])
        self.assertEqual(7, response.json['administrators'][4]['id'])
    
    def test_get_administrators_username_desc(self):

        response = self.client.get(
            '/administrators?order_by=username.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("administrators", response.json)

        self.assertEqual(7, response.json['administrators'][0]['id'])
        self.assertEqual(4, response.json['administrators'][1]['id'])
        self.assertEqual(3, response.json['administrators'][2]['id'])
        self.assertEqual(2, response.json['administrators'][3]['id'])
        self.assertEqual(1, response.json['administrators'][4]['id'])
    
    def test_get_administrators_joined_at_asc(self):

        response = self.client.get(
            '/administrators?order_by=joined_at.asc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("administrators", response.json)

        self.assertEqual(1, response.json['administrators'][0]['id'])
        self.assertEqual(2, response.json['administrators'][1]['id'])
        self.assertEqual(7, response.json['administrators'][2]['id'])
        self.assertEqual(3, response.json['administrators'][3]['id'])
        self.assertEqual(4, response.json['administrators'][4]['id'])
    
    def test_get_administrators_joined_at_desc(self):

        response = self.client.get(
            '/administrators?order_by=joined_at.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("administrators", response.json)

        self.assertEqual(4, response.json['administrators'][0]['id'])
        self.assertEqual(3, response.json['administrators'][1]['id'])
        self.assertEqual(7, response.json['administrators'][2]['id'])
        self.assertEqual(2, response.json['administrators'][3]['id'])
        self.assertEqual(1, response.json['administrators'][4]['id'])
    
    def test_get_administrators_page_2(self):

        response = self.client.get(
            '/administrators/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(204, response.status_code)
        self.assertTrue(None == response.json)
    
    def test_get_administrators_page_1_limit_2(self):

        response = self.client.get(
            '/administrators/1/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(2, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("administrators", response.json)
        self.assertTrue(response.json['next_uri'].endswith('/administrators/2/2'))

        self.assertEqual(1, response.json['administrators'][0]['id'])
        self.assertEqual(2, response.json['administrators'][1]['id'])
    
    def test_get_administrators_page_2_limit_1(self):

        response = self.client.get(
            '/administrators/2/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(2, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(2, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("administrators", response.json)
        self.assertTrue(response.json['previous_uri'].endswith('/administrators/1/2'))
        self.assertTrue(response.json['next_uri'].endswith('/administrators/3/2'))

        self.assertEqual(3, response.json['administrators'][0]['id'])
        self.assertEqual(4, response.json['administrators'][1]['id'])
    
    def test_get_administrators_status_enabled(self):

        response = self.client.get(
            '/administrators?status=1&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("administrators", response.json)

        self.assertEqual(1, response.json['administrators'][0]['id'])
        self.assertEqual(2, response.json['administrators'][1]['id'])
        self.assertEqual(3, response.json['administrators'][2]['id'])

    def test_get_administrators_status_disabled(self):

        response = self.client.get(
            '/administrators?status=2&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("administrators", response.json)

        self.assertEqual(4, response.json['administrators'][0]['id'])

    def test_get_administrators_status_archived(self):

        response = self.client.get(
            '/administrators?status=3&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("administrators", response.json)

        self.assertEqual(5, response.json['administrators'][0]['id'])

    def test_get_administrators_status_deleted(self):

        response = self.client.get(
            '/administrators?status=4&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("administrators", response.json)

        self.assertEqual(6, response.json['administrators'][0]['id'])
    
    def test_get_administrators_status_pending(self):

        response = self.client.get(
            '/administrators?status=5&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("administrators", response.json)

        self.assertEqual(7, response.json['administrators'][0]['id'])

    def test_get_administrators_role_admin(self):

        response = self.client.get(
            '/administrators?role=2&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(4, response.json['total'])
        self.assertIn("administrators", response.json)

        self.assertEqual(1, response.json['administrators'][0]['id'])
        self.assertEqual(2, response.json['administrators'][1]['id'])
        self.assertEqual(4, response.json['administrators'][2]['id'])
        self.assertEqual(7, response.json['administrators'][3]['id'])
    
    def test_get_administrators_role_admin_status_pending(self):

        response = self.client.get(
            '/administrators?role=2&status=5&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("administrators", response.json)

        self.assertEqual(7, response.json['administrators'][0]['id'])
    
    def test_get_administrators_no_app_key(self):

        response = self.client.get(
            '/administrators',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_get_administrators_bad_app_key(self):

        response = self.client.get(
            '/administrators?app_key=BAD_APP_KEY',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_get_administrators_unauthorized(self):

        response = self.client.get('/administrators?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_get_administrators_no_permission(self):

        response = self.client.get(
            '/administrators?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])

    def test_get_administrator_1(self):

        response = self.client.get(
            '/administrator/1?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.json['administrator']['id'])
        self.assertEqual("admin1", response.json['administrator']['username'])
        self.assertEqual("admin1@test.com", response.json['administrator']['email'])
        self.assertEqual("Tommy", response.json['administrator']['first_name'])
        self.assertEqual("Lund", response.json['administrator']['last_name'])
        self.assertIn("password_changed_at", response.json['administrator'])
        self.assertEqual("2018-11-01T00:00:00+0000", response.json['administrator']['joined_at'])
        self.assertEqual(1, response.json['administrator']['status'])
        self.assertEqual("2018-11-01T00:00:00+0000", response.json['administrator']['status_changed_at'])
        self.assertEqual(2, response.json['administrator']['roles'][0]['id'])
        self.assertEqual("SUPER_ADMIN", response.json['administrator']['roles'][0]['name'])
        self.assertTrue(response.json['administrator']['uri'].endswith('/administrator/1'))
        self.assertIn("created_at", response.json['administrator'])
        self.assertIn("updated_at", response.json['administrator'])
        self.assertNotIn("password", response.json['administrator'])
    
    def test_get_administrator_250(self):

        response = self.client.get(
            '/administrator/250?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(404, response.status_code)
        self.assertEqual("Not found", response.json['error'])
    
    def test_get_administrator_no_app_key(self):

        response = self.client.get(
            '/administrator/1',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_get_administrator_bad_app_key(self):

        response = self.client.get(
            '/administrator/1?app_key=BAD_APP_KEY',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_get_administrator_unauthorized(self):

        response = self.client.get('/administrator/1?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_get_administrator_no_permission(self):

        response = self.client.get(
            '/administrator/1?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
    
    def test_post_administrator_error(self):

        response = self.client.post(
            '/administrators?app_key=' + AppKeyData.id1_appkey1.key,
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
        self.assertIn("joined_at", response.json['error'])
        self.assertIn("status", response.json['error'])
        self.assertIn("password", response.json['error'])
        self.assertNotIn("password_changed_at", response.json['error'])
    
    def test_post_administrator_password_comlexity(self):

        response = self.client.post(
            '/administrators?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"admin8","email":"admin8@test.com","first_name":"Blanch","last_name":"Causer","joined_at":"2019-02-10T00:00:00+0000","password":"password","roles":[2],"status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("password", response.json['error'])
        self.assertEqual("Please choose a more complex password.", response.json['error']['password'][0])
        self.assertNotIn("username", response.json['error'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("joined_at", response.json['error'])
        self.assertNotIn("status", response.json['error'])

    def test_post_administrator_unique_username_error(self):

        response = self.client.post(
            '/administrators?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"admin2","email":"admin8@test.com","first_name":"Blanch","last_name":"Causer","joined_at":"2019-02-10T00:00:00+0000","password":"user8Pass","roles":[2],"status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must be unique."], response.json['error']['username'])
        self.assertNotIn("password", response.json['error'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("joined_at", response.json['error'])
        self.assertNotIn("status", response.json['error'])

    def test_post_administrator_unique_email_error(self):

        response = self.client.post(
            '/administrators?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"admin8","email":"admin2@test.com","first_name":"Blanch","last_name":"Causer","joined_at":"2019-02-10T00:00:00+0000","password":"user8Pass","roles":[2],"status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("email", response.json['error'])
        self.assertEqual(["Value must be unique."], response.json['error']['email'])
        self.assertNotIn("password", response.json['error'])
        self.assertNotIn("username", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("joined_at", response.json['error'])
        self.assertNotIn("status", response.json['error'])
    
    def test_post_administrator_unique_username_and_no_first_name_error(self):

        response = self.client.post(
            '/administrators?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"admin2","email":"admin8@test.com","first_name":"","last_name":"Causer","joined_at":"2019-02-10T00:00:00+0000","password":"user8Pass","roles":[2],"status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must be unique."], response.json['error']['username'])
        self.assertIn("first_name", response.json['error'])
        self.assertNotIn("password", response.json['error'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("joined_at", response.json['error'])
        self.assertNotIn("status", response.json['error'])

    # @todo: test 500 error for bad role

    def test_post_administrator_success(self):

        response = self.client.post(
            '/administrators?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"admin8","email":"admin8@test.com","first_name":"Blanch","last_name":"Causer","joined_at":"2019-02-10T00:00:00+0000","password":"user8Pass","roles":[2],"status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(201, response.status_code)
        self.assertEqual(8, response.json['administrator']['id'])
        self.assertEqual("admin8", response.json['administrator']['username'])
        self.assertEqual("admin8@test.com", response.json['administrator']['email'])
        self.assertEqual("Blanch", response.json['administrator']['first_name'])
        self.assertEqual("Causer", response.json['administrator']['last_name'])
        self.assertIn("password_changed_at", response.json['administrator'])
        self.assertEqual("2019-02-10T00:00:00+0000", response.json['administrator']['joined_at'])
        self.assertEqual(1, response.json['administrator']['status'])
        self.assertIn("status_changed_at", response.json['administrator'])
        self.assertEqual(2, response.json['administrator']['roles'][0]['id'])
        self.assertEqual("SUPER_ADMIN", response.json['administrator']['roles'][0]['name'])
        self.assertTrue(response.json['administrator']['uri'].endswith('/administrator/8'))
        self.assertIn("created_at", response.json['administrator'])
        self.assertIn("updated_at", response.json['administrator'])
        self.assertNotIn("password", response.json['administrator'])
    
    def test_post_administrator_no_app_key(self):

        response = self.client.post(
            '/administrators',
            data='{"username":"admin8","email":"admin8@test.com","first_name":"Blanch","last_name":"Causer","joined_at":"2019-02-10T00:00:00+0000","password":"user8Pass","roles":[2],"status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_post_administrator_bad_app_key(self):

        response = self.client.post(
            '/administrators?app_key=BAD_APP_KEY',
            data='{"username":"admin8","email":"admin8@test.com","first_name":"Blanch","last_name":"Causer","joined_at":"2019-02-10T00:00:00+0000","password":"user8Pass","roles":[2],"status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_post_administrator_unauthorized(self):

        response = self.client.post(
            '/administrators?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"admin8","email":"admin8@test.com","first_name":"Blanch","last_name":"Causer","joined_at":"2019-02-10T00:00:00+0000","password":"user8Pass","roles":[2],"status":1}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_post_administrator_no_permission(self):

        response = self.client.post(
            '/administrators?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"admin8","email":"admin8@test.com","first_name":"Blanch","last_name":"Causer","joined_at":"2019-02-10T00:00:00+0000","password":"user8Pass","roles":[2],"status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
    
    def test_put_administrator_error(self):

        response = self.client.put(
            '/administrator/2?app_key=' + AppKeyData.id1_appkey1.key,
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
        self.assertIn("joined_at", response.json['error'])
        self.assertIn("status", response.json['error'])
        self.assertNotIn("password", response.json['error'])
        self.assertNotIn("password_changed_at", response.json['error'])
    
    def test_put_administrator_empty(self):

        response = self.client.put(
            '/administrator/250?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"admin2a","email":"admin2a@test.com","first_name":"Selmma","last_name":"Keyyes","joined_at":"2018-11-06T00:00:00+0000","password":"user8Pass","roles":[2],"status":2}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(404, response.status_code)
        self.assertEqual("Not found", response.json['error'])

    def test_put_administrator_password_complexity(self):

        response = self.client.put(
            '/administrator/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"admin2a","email":"admin2a@test.com","first_name":"Selmma","last_name":"Keyyes","joined_at":"2018-11-06T00:00:00+0000","password":"password","roles":[2],"status":2}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("password", response.json['error'])
        self.assertEqual("Please choose a more complex password.", response.json['error']['password'][0])
        self.assertNotIn("username", response.json['error'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("joined_at", response.json['error'])
        self.assertNotIn("status", response.json['error'])
    
    def test_put_administrator_unique_username_error(self):

        response = self.client.put(
            '/administrator/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"admin3","email":"admin2a@test.com","first_name":"Selmma","last_name":"Keyyes","joined_at":"2018-11-06T00:00:00+0000","password":"user8Pass","roles":[2],"status":2}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("username", response.json['error'])
        self.assertEqual(["Value must be unique."], response.json['error']['username'])
        self.assertNotIn("password", response.json['error'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("joined_at", response.json['error'])
        self.assertNotIn("status", response.json['error'])

    def test_put_administrator_unique_email_error(self):

        response = self.client.put(
            '/administrator/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"admin2a","email":"admin3@test.com","first_name":"Selmma","last_name":"Keyyes","joined_at":"2018-11-06T00:00:00+0000","password":"user8Pass","roles":[2],"status":2}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("email", response.json['error'])
        self.assertEqual(["Value must be unique."], response.json['error']['email'])
        self.assertNotIn("username", response.json['error'])
        self.assertNotIn("password", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("joined_at", response.json['error'])
        self.assertNotIn("status", response.json['error'])
    
    def test_put_administrator_unique_username_and_no_first_name_error(self):

        response = self.client.put(
            '/administrator/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"admin3","email":"admin2a@test.com","first_name":"","last_name":"Keyyes","joined_at":"2018-11-06T00:00:00+0000","password":"user8Pass","roles":[2],"status":2}',
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
        self.assertNotIn("password", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("joined_at", response.json['error'])
        self.assertNotIn("status", response.json['error'])

    def test_put_administrator_admin_2(self):

        response = self.client.put(
            '/administrator/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"admin2a","email":"admin2a@test.com","first_name":"Selmma","last_name":"Keyyes","joined_at":"2018-11-06T00:00:00+0000","password":"user8Pass","roles":[2],"status":2}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, response.json['administrator']['id'])
        self.assertEqual("admin2a", response.json['administrator']['username'])
        self.assertEqual("admin2a@test.com", response.json['administrator']['email'])
        self.assertEqual("Selmma", response.json['administrator']['first_name'])
        self.assertEqual("Keyyes", response.json['administrator']['last_name'])
        self.assertIn("password_changed_at", response.json['administrator'])
        self.assertEqual("2018-11-06T00:00:00+0000", response.json['administrator']['joined_at'])
        self.assertEqual(2, response.json['administrator']['status'])
        self.assertIn("status_changed_at", response.json['administrator'])
        self.assertEqual(2, response.json['administrator']['roles'][0]['id'])
        self.assertEqual("SUPER_ADMIN", response.json['administrator']['roles'][0]['name'])
        self.assertTrue(response.json['administrator']['uri'].endswith('/administrator/2'))
        self.assertIn("created_at", response.json['administrator'])
        self.assertIn("updated_at", response.json['administrator'])
        self.assertNotIn("password", response.json['administrator'])
    
    def test_put_administrator_admin_2_no_password(self):

        response = self.client.put(
            '/administrator/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"admin2a","email":"admin2a@test.com","first_name":"Selmma","last_name":"Keyyes","joined_at":"2018-11-06T00:00:00+0000","roles":[2],"status":2}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, response.json['administrator']['id'])
        self.assertEqual("admin2a", response.json['administrator']['username'])
        self.assertEqual("admin2a@test.com", response.json['administrator']['email'])
        self.assertEqual("Selmma", response.json['administrator']['first_name'])
        self.assertEqual("Keyyes", response.json['administrator']['last_name'])
        self.assertIn("password_changed_at", response.json['administrator'])
        self.assertEqual("2018-11-06T00:00:00+0000", response.json['administrator']['joined_at'])
        self.assertEqual(2, response.json['administrator']['status'])
        self.assertIn("status_changed_at", response.json['administrator'])
        self.assertEqual(2, response.json['administrator']['roles'][0]['id'])
        self.assertEqual("SUPER_ADMIN", response.json['administrator']['roles'][0]['name'])
        self.assertTrue(response.json['administrator']['uri'].endswith('/administrator/2'))
        self.assertIn("created_at", response.json['administrator'])
        self.assertIn("updated_at", response.json['administrator'])
        self.assertNotIn("password", response.json['administrator'])

    def test_put_administrator_admin_2_no_joined_at_error(self):

        response = self.client.put(
            '/administrator/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"admin2a","email":"admin2a@test.com","first_name":"Selmma","last_name":"Keyyes","password":"user8Pass","roles":[2],"status":2}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("joined_at", response.json['error'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("username", response.json['error'])
        self.assertNotIn("email", response.json['error'])
        self.assertNotIn("password", response.json['error'])
        self.assertNotIn("status", response.json['error'])
    
    def test_put_administrator_no_app_key(self):

        response = self.client.put(
            '/administrator/2',
            data='{"username":"admin2a","email":"admin2a@test.com","first_name":"Selmma","last_name":"Keyyes","joined_at":"2018-11-06T00:00:00+0000","password":"user8Pass","roles":[2],"status":2}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_put_administrator_bad_app_key(self):

        response = self.client.put(
            '/administrator/2?app_key=BAD_APP_KEY',
            data='{"username":"admin2a","email":"admin2a@test.com","first_name":"Selmma","last_name":"Keyyes","joined_at":"2018-11-06T00:00:00+0000","password":"user8Pass","roles":[2],"status":2}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_put_administrator_unauthorized(self):

        response = self.client.put(
            '/administrator/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"admin2a","email":"admin2a@test.com","first_name":"Selmma","last_name":"Keyyes","joined_at":"2018-11-06T00:00:00+0000","password":"user8Pass","roles":[2],"status":2}',
            headers={"Content-Type": "application/json"})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])

    def test_put_administrator_no_permission(self):

        response = self.client.put(
            '/administrator/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"username":"admin2a","email":"admin2a@test.com","first_name":"Selmma","last_name":"Keyyes","joined_at":"2018-11-06T00:00:00+0000","password":"user8Pass","roles":[2],"status":2}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
    
    def test_delete_administrator_id2(self):

        response = self.client.delete(
            '/administrator/2?app_key=' + AppKeyData.id1_appkey1.key, 
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(204, response.status_code)
        self.assertEqual(None, response.json)
    
    def test_delete_administrator_empty(self):

        response = self.client.delete(
            '/administrator/250?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(404, response.status_code)
        self.assertEqual("Not found", response.json['error'])
    
    def test_delete_administrator_no_app_key(self):

        response = self.client.delete(
            '/administrator/2', 
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_delete_administrator_bad_app_key(self):

        response = self.client.delete(
            '/administrator/2?app_key=BAD_APP_KEY', 
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])

    def test_delete_administrator_unauthorized(self):

        response = self.client.delete(
            '/administrator/2?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_delete_administrator_no_permission(self):

        response = self.client.delete(
            '/administrator/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
