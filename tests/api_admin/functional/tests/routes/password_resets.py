from tests.BaseTest import BaseTest
from test_fixtures import *
from tests.utils import get_http_basic_auth_credentials
    
class PasswordResetsTest(BaseTest):

    def test_get_password_resets(self):

        response = self.client.get('/password_resets?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(7, response.json['total'])
        self.assertIn("password_resets", response.json)

        self.assertEqual(1, response.json['password_resets'][0]['id'])
        self.assertIn('user', response.json['password_resets'][0])
        self.assertEqual(1, response.json['password_resets'][0]['user']['id'])
        self.assertTrue(response.json['password_resets'][0]['user']['uri'].endswith('/user/1'))
        self.assertEqual("user1", response.json['password_resets'][0]['user']['username'])
        self.assertEqual("HD7SF2", response.json['password_resets'][0]['code'])
        self.assertEqual(True, response.json['password_resets'][0]['is_used'])
        self.assertEqual("2019-01-10T07:13:49+0000", response.json['password_resets'][0]['requested_at'])
        self.assertEqual("1.1.1.1", response.json['password_resets'][0]['ip_address'])
        self.assertEqual(1, response.json['password_resets'][0]['status'])
        self.assertEqual("2019-01-10T00:00:00+0000", response.json['password_resets'][0]['status_changed_at'])
        self.assertIn("created_at", response.json['password_resets'][0])
        self.assertIn("updated_at", response.json['password_resets'][0])

        self.assertEqual(2, response.json['password_resets'][1]['id'])
        self.assertIn('user', response.json['password_resets'][1])
        self.assertEqual(2, response.json['password_resets'][1]['user']['id'])
        self.assertTrue(response.json['password_resets'][1]['user']['uri'].endswith('/user/2'))
        self.assertEqual("user2", response.json['password_resets'][1]['user']['username'])
        self.assertEqual("M5AF8G", response.json['password_resets'][1]['code'])
        self.assertEqual(True, response.json['password_resets'][1]['is_used'])
        self.assertEqual("2019-01-12T14:02:51+0000", response.json['password_resets'][1]['requested_at'])
        self.assertEqual("1.1.1.2", response.json['password_resets'][1]['ip_address'])
        self.assertEqual(1, response.json['password_resets'][1]['status'])
        self.assertEqual("2019-01-12T00:00:00+0000", response.json['password_resets'][1]['status_changed_at'])
        self.assertIn("created_at", response.json['password_resets'][1])
        self.assertIn("updated_at", response.json['password_resets'][1])

        self.assertEqual(3, response.json['password_resets'][2]['id'])
        self.assertIn('user', response.json['password_resets'][2])
        self.assertEqual(1, response.json['password_resets'][2]['user']['id'])
        self.assertTrue(response.json['password_resets'][2]['user']['uri'].endswith('/user/1'))
        self.assertEqual("user1", response.json['password_resets'][2]['user']['username'])
        self.assertEqual("QQ94ND", response.json['password_resets'][2]['code'])
        self.assertEqual(True, response.json['password_resets'][2]['is_used'])
        self.assertEqual("2019-01-15T20:46:15+0000", response.json['password_resets'][2]['requested_at'])
        self.assertEqual("1.1.1.1", response.json['password_resets'][2]['ip_address'])
        self.assertEqual(2, response.json['password_resets'][2]['status'])
        self.assertEqual("2019-01-15T00:00:00+0000", response.json['password_resets'][2]['status_changed_at'])
        self.assertIn("created_at", response.json['password_resets'][2])
        self.assertIn("updated_at", response.json['password_resets'][2])

        self.assertEqual(5, response.json['password_resets'][3]['id'])
        self.assertIn('user', response.json['password_resets'][3])
        self.assertEqual(3, response.json['password_resets'][3]['user']['id'])
        self.assertTrue(response.json['password_resets'][3]['user']['uri'].endswith('/user/3'))
        self.assertEqual("user3", response.json['password_resets'][3]['user']['username'])
        self.assertEqual("XAY87R", response.json['password_resets'][3]['code'])
        self.assertEqual(True, response.json['password_resets'][3]['is_used'])
        self.assertEqual("2019-01-20T03:37:10+0000", response.json['password_resets'][3]['requested_at'])
        self.assertEqual("1.1.1.3", response.json['password_resets'][3]['ip_address'])
        self.assertEqual(5, response.json['password_resets'][3]['status'])
        self.assertEqual("2019-01-20T00:00:00+0000", response.json['password_resets'][3]['status_changed_at'])
        self.assertIn("created_at", response.json['password_resets'][3])
        self.assertIn("updated_at", response.json['password_resets'][3])

        self.assertEqual(7, response.json['password_resets'][4]['id'])
        self.assertIn('user', response.json['password_resets'][4])
        self.assertEqual(2, response.json['password_resets'][4]['user']['id'])
        self.assertTrue(response.json['password_resets'][4]['user']['uri'].endswith('/user/2'))
        self.assertEqual("user2", response.json['password_resets'][4]['user']['username'])
        self.assertEqual("AM8A4N", response.json['password_resets'][4]['code'])
        self.assertEqual(False, response.json['password_resets'][4]['is_used'])
        self.assertEqual("2019-01-28T09:38:58+0000", response.json['password_resets'][4]['requested_at'])
        self.assertEqual("1.2.3.4", response.json['password_resets'][4]['ip_address'])
        self.assertEqual(1, response.json['password_resets'][4]['status'])
        self.assertEqual("2019-01-28T00:00:00+0000", response.json['password_resets'][4]['status_changed_at'])
        self.assertIn("created_at", response.json['password_resets'][4])
        self.assertIn("updated_at", response.json['password_resets'][4])

        self.assertEqual(8, response.json['password_resets'][5]['id'])
        self.assertIn('user', response.json['password_resets'][5])
        self.assertEqual(2, response.json['password_resets'][5]['user']['id'])
        self.assertTrue(response.json['password_resets'][5]['user']['uri'].endswith('/user/2'))
        self.assertEqual("user2", response.json['password_resets'][5]['user']['username'])
        self.assertEqual("PRQ7M2", response.json['password_resets'][5]['code'])
        self.assertEqual(True, response.json['password_resets'][5]['is_used'])
        self.assertIn('requested_at', response.json['password_resets'][5])
        self.assertEqual("1.2.3.4", response.json['password_resets'][5]['ip_address'])
        self.assertEqual(1, response.json['password_resets'][5]['status'])
        self.assertIn('status_changed_at', response.json['password_resets'][5])
        self.assertIn("created_at", response.json['password_resets'][5])
        self.assertIn("updated_at", response.json['password_resets'][5])

        self.assertEqual(9, response.json['password_resets'][6]['id'])
        self.assertIn('user', response.json['password_resets'][6])
        self.assertEqual(2, response.json['password_resets'][6]['user']['id'])
        self.assertTrue(response.json['password_resets'][6]['user']['uri'].endswith('/user/2'))
        self.assertEqual("user2", response.json['password_resets'][6]['user']['username'])
        self.assertEqual("J91NP0", response.json['password_resets'][6]['code'])
        self.assertEqual(False, response.json['password_resets'][6]['is_used'])
        self.assertIn('requested_at', response.json['password_resets'][6])
        self.assertEqual("1.2.3.4", response.json['password_resets'][6]['ip_address'])
        self.assertEqual(1, response.json['password_resets'][6]['status'])
        self.assertIn('status_changed_at', response.json['password_resets'][6])
        self.assertIn("created_at", response.json['password_resets'][6])
        self.assertIn("updated_at", response.json['password_resets'][6])

    def test_get_password_resets_id_asc(self):

        response = self.client.get('/password_resets?order_by=id.asc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(7, response.json['total'])
        self.assertIn("password_resets", response.json)

        self.assertEqual(1, response.json['password_resets'][0]['id'])
        self.assertEqual(2, response.json['password_resets'][1]['id'])
        self.assertEqual(3, response.json['password_resets'][2]['id'])
        self.assertEqual(5, response.json['password_resets'][3]['id'])
        self.assertEqual(7, response.json['password_resets'][4]['id'])
        self.assertEqual(8, response.json['password_resets'][5]['id'])
        self.assertEqual(9, response.json['password_resets'][6]['id'])
    
    def test_get_password_resets_id_desc(self):

        response = self.client.get('/password_resets?order_by=id.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(7, response.json['total'])
        self.assertIn("password_resets", response.json)

        self.assertEqual(9, response.json['password_resets'][0]['id'])
        self.assertEqual(8, response.json['password_resets'][1]['id'])
        self.assertEqual(7, response.json['password_resets'][2]['id'])
        self.assertEqual(5, response.json['password_resets'][3]['id'])
        self.assertEqual(3, response.json['password_resets'][4]['id'])
        self.assertEqual(2, response.json['password_resets'][5]['id'])
        self.assertEqual(1, response.json['password_resets'][6]['id'])
    
    def test_get_password_resets_requested_at_asc(self):

        response = self.client.get('/password_resets?order_by=requested_at.asc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(7, response.json['total'])
        self.assertIn("password_resets", response.json)

        self.assertEqual(1, response.json['password_resets'][0]['id'])
        self.assertEqual(2, response.json['password_resets'][1]['id'])
        self.assertEqual(3, response.json['password_resets'][2]['id'])
        self.assertEqual(5, response.json['password_resets'][3]['id'])
        self.assertEqual(7, response.json['password_resets'][4]['id'])
        self.assertEqual(8, response.json['password_resets'][5]['id'])
        self.assertEqual(9, response.json['password_resets'][6]['id'])
    
    def test_get_password_resets_requested_at_desc(self):

        response = self.client.get('/password_resets?order_by=requested_at.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(7, response.json['total'])
        self.assertIn("password_resets", response.json)

        self.assertEqual(9, response.json['password_resets'][0]['id'])
        self.assertEqual(8, response.json['password_resets'][1]['id'])
        self.assertEqual(7, response.json['password_resets'][2]['id'])
        self.assertEqual(5, response.json['password_resets'][3]['id'])
        self.assertEqual(3, response.json['password_resets'][4]['id'])
        self.assertEqual(2, response.json['password_resets'][5]['id'])
        self.assertEqual(1, response.json['password_resets'][6]['id'])

    def test_get_password_resets_page_2(self):

        response = self.client.get('/password_resets/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(204, response.status_code)
        self.assertTrue(None == response.json)
    
    def test_get_password_resets_page_1_limit_2(self):

        response = self.client.get('/password_resets/1/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(2, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(7, response.json['total'])
        self.assertIn("password_resets", response.json)
        self.assertTrue(response.json['next_uri'].endswith('/password_resets/2/2'))

        self.assertEqual(1, response.json['password_resets'][0]['id'])
        self.assertEqual(2, response.json['password_resets'][1]['id'])
    
    def test_get_password_resets_page_2_limit_2(self):

        response = self.client.get('/password_resets/2/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(2, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(2, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(7, response.json['total'])
        self.assertIn("password_resets", response.json)
        self.assertTrue(response.json['previous_uri'].endswith('/password_resets/1/2'))
        self.assertTrue(response.json['next_uri'].endswith('/password_resets/3/2'))

        self.assertEqual(3, response.json['password_resets'][0]['id'])
        self.assertEqual(5, response.json['password_resets'][1]['id'])

    def test_get_password_resets_user_2(self):

        response = self.client.get('/password_resets?user_id=2&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(4, response.json['total'])
        self.assertIn("password_resets", response.json)

        self.assertEqual(2, response.json['password_resets'][0]['id'])
        self.assertEqual(7, response.json['password_resets'][1]['id'])
        self.assertEqual(8, response.json['password_resets'][2]['id'])
        self.assertEqual(9, response.json['password_resets'][3]['id'])
    
    def test_get_password_resets_status_enabled(self):

        response = self.client.get('/password_resets?status=1&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("password_resets", response.json)

        self.assertEqual(1, response.json['password_resets'][0]['id'])
        self.assertEqual(2, response.json['password_resets'][1]['id'])
        self.assertEqual(7, response.json['password_resets'][2]['id'])
        self.assertEqual(8, response.json['password_resets'][3]['id'])
        self.assertEqual(9, response.json['password_resets'][4]['id'])
    
    def test_get_password_resets_status_disabled(self):

        response = self.client.get('/password_resets?status=2&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("password_resets", response.json)

        self.assertEqual(3, response.json['password_resets'][0]['id'])
    
    def test_get_password_resets_status_archived(self):

        response = self.client.get('/password_resets?status=3&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("password_resets", response.json)

        self.assertEqual(4, response.json['password_resets'][0]['id'])
    
    def test_get_password_resets_status_deleted(self):

        response = self.client.get('/password_resets?status=4&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("password_resets", response.json)

        self.assertEqual(6, response.json['password_resets'][0]['id'])
    
    def test_get_password_resets_status_pending(self):

        response = self.client.get('/password_resets?status=5&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("password_resets", response.json)

        self.assertEqual(5, response.json['password_resets'][0]['id'])
    
    def test_get_password_resets_no_app_key(self):

        response = self.client.get('/password_resets',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_get_password_resets_bad_app_key(self):

        response = self.client.get('/password_resets?app_key=BAD_APP_KEY',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_get_password_resets_unauthorized(self):

        response = self.client.get('/password_resets?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_get_password_resets_no_permission(self):

        response = self.client.get('/password_resets?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
