from tests.BaseTest import BaseTest
from test_fixtures import *
from tests.utils import get_http_basic_auth_credentials
    
class LoginsTest(BaseTest):

    def test_get_logins(self):

        response = self.client.get('/logins?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(25, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(8+1, response.json['total'])
        self.assertIn("logins", response.json)

        self.assertEqual(1, response.json['logins'][0]['id'])
        self.assertEqual(1, response.json['logins'][0]['user_id'])
        self.assertEqual("admin1", response.json['logins'][0]['username'])
        self.assertEqual("1.1.1.1", response.json['logins'][0]['ip_address'])
        self.assertTrue(response.json['logins'][0]['success'])
        self.assertEqual("2018-12-01T08:32:55+0000", response.json['logins'][0]['attempt_date'])
        self.assertIn("created_at", response.json['logins'][0])
        self.assertIn("updated_at", response.json['logins'][0])

        self.assertEqual(2, response.json['logins'][1]['id'])
        self.assertEqual(1, response.json['logins'][1]['user_id'])
        self.assertEqual("admin1", response.json['logins'][1]['username'])
        self.assertEqual("1.1.1.1", response.json['logins'][1]['ip_address'])
        self.assertFalse(response.json['logins'][1]['success'])
        self.assertEqual("2018-12-02T12:02:21+0000", response.json['logins'][1]['attempt_date'])
        self.assertIn("created_at", response.json['logins'][1])
        self.assertIn("updated_at", response.json['logins'][1])

        self.assertEqual(3, response.json['logins'][2]['id'])
        self.assertEqual(1, response.json['logins'][2]['user_id'])
        self.assertEqual("admin1", response.json['logins'][2]['username'])
        self.assertEqual("1.1.1.1", response.json['logins'][2]['ip_address'])
        self.assertTrue(response.json['logins'][2]['success'])
        self.assertEqual("2018-12-02T12:03:09+0000", response.json['logins'][2]['attempt_date'])
        self.assertIn("created_at", response.json['logins'][2])
        self.assertIn("updated_at", response.json['logins'][2])

        self.assertEqual(4, response.json['logins'][3]['id'])
        self.assertEqual(2, response.json['logins'][3]['user_id'])
        self.assertEqual("user2", response.json['logins'][3]['username'])
        self.assertEqual("1.1.1.2", response.json['logins'][3]['ip_address'])
        self.assertTrue(response.json['logins'][3]['success'])
        self.assertEqual("2018-12-10T20:47:30+0000", response.json['logins'][3]['attempt_date'])
        self.assertIn("created_at", response.json['logins'][3])
        self.assertIn("updated_at", response.json['logins'][3])

        self.assertEqual(5, response.json['logins'][4]['id'])
        self.assertEqual(2, response.json['logins'][4]['user_id'])
        self.assertEqual("user2", response.json['logins'][4]['username'])
        self.assertEqual("9.9.9.9", response.json['logins'][4]['ip_address'])
        self.assertFalse(response.json['logins'][4]['success'])
        self.assertEqual("2018-12-22T23:11:53+0000", response.json['logins'][4]['attempt_date'])
        self.assertIn("created_at", response.json['logins'][4])
        self.assertIn("updated_at", response.json['logins'][4])

        self.assertEqual(6, response.json['logins'][5]['id'])
        self.assertEqual(2, response.json['logins'][5]['user_id'])
        self.assertEqual("user2", response.json['logins'][5]['username'])
        self.assertEqual("9.9.9.9", response.json['logins'][5]['ip_address'])
        self.assertFalse(response.json['logins'][5]['success'])
        self.assertEqual("2018-12-22T23:12:28+0000", response.json['logins'][5]['attempt_date'])
        self.assertIn("created_at", response.json['logins'][5])
        self.assertIn("updated_at", response.json['logins'][5])

        self.assertEqual(7, response.json['logins'][6]['id'])
        self.assertEqual(3, response.json['logins'][6]['user_id'])
        self.assertEqual("user3", response.json['logins'][6]['username'])
        self.assertEqual("1.1.1.3", response.json['logins'][6]['ip_address'])
        self.assertTrue(response.json['logins'][6]['success'])
        self.assertEqual("2018-12-15T07:32:18+0000", response.json['logins'][6]['attempt_date'])
        self.assertIn("created_at", response.json['logins'][6])
        self.assertIn("updated_at", response.json['logins'][6])

        self.assertEqual(8, response.json['logins'][7]['id'])
        self.assertEqual(None, response.json['logins'][7]['user_id'])
        self.assertEqual("root", response.json['logins'][7]['username'])
        self.assertEqual("9.9.9.9", response.json['logins'][7]['ip_address'])
        self.assertFalse(response.json['logins'][7]['success'])
        self.assertEqual("2019-01-08T02:40:21+0000", response.json['logins'][7]['attempt_date'])
        self.assertIn("created_at", response.json['logins'][7])
        self.assertIn("updated_at", response.json['logins'][7])

        self.assertEqual(9, response.json['logins'][8]['id'])
        self.assertEqual(1, response.json['logins'][8]['user_id'])
        self.assertEqual("admin1", response.json['logins'][8]['username'])
        self.assertEqual("127.0.0.1", response.json['logins'][8]['ip_address'])
        self.assertTrue(response.json['logins'][8]['success'])
        self.assertIn("attempt_date", response.json['logins'][8])
        self.assertIn("created_at", response.json['logins'][8])
        self.assertIn("updated_at", response.json['logins'][8])

        self.assertEqual(9, response.json['logins'][8]['id'])
    
    def test_get_logins_id_desc(self):

        response = self.client.get('/logins?order_by=id.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(25, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(8+1, response.json['total'])
        self.assertIn("logins", response.json)

        self.assertEqual(9, response.json['logins'][0]['id'])
        self.assertEqual(8, response.json['logins'][1]['id'])
        self.assertEqual(7, response.json['logins'][2]['id'])
        self.assertEqual(6, response.json['logins'][3]['id'])
        self.assertEqual(5, response.json['logins'][4]['id'])
        self.assertEqual(4, response.json['logins'][5]['id'])
        self.assertEqual(3, response.json['logins'][6]['id'])
        self.assertEqual(2, response.json['logins'][7]['id'])
        self.assertEqual(1, response.json['logins'][8]['id'])
    
    def test_get_logins_attempt_date_asc(self):

        response = self.client.get('/logins?order_by=attempt_date.asc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(25, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(8+1, response.json['total'])
        self.assertIn("logins", response.json)

        self.assertEqual(1, response.json['logins'][0]['id'])
        self.assertEqual(2, response.json['logins'][1]['id'])
        self.assertEqual(3, response.json['logins'][2]['id'])
        self.assertEqual(4, response.json['logins'][3]['id'])
        self.assertEqual(7, response.json['logins'][4]['id'])
        self.assertEqual(5, response.json['logins'][5]['id'])
        self.assertEqual(6, response.json['logins'][6]['id'])
        self.assertEqual(8, response.json['logins'][7]['id'])
        self.assertEqual(9, response.json['logins'][8]['id'])
    
    def test_get_logins_attempt_date_desc(self):

        response = self.client.get('/logins?order_by=attempt_date.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(25, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(8+1, response.json['total'])
        self.assertIn("logins", response.json)

        self.assertEqual(9, response.json['logins'][0]['id'])
        self.assertEqual(8, response.json['logins'][1]['id'])
        self.assertEqual(6, response.json['logins'][2]['id'])
        self.assertEqual(5, response.json['logins'][3]['id'])
        self.assertEqual(7, response.json['logins'][4]['id'])
        self.assertEqual(4, response.json['logins'][5]['id'])
        self.assertEqual(3, response.json['logins'][6]['id'])
        self.assertEqual(2, response.json['logins'][7]['id'])
        self.assertEqual(1, response.json['logins'][8]['id'])
    
    def test_get_logins_page_2(self):

        response = self.client.get('/logins/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(204, response.status_code)
        self.assertTrue(None == response.json)
    
    def test_get_logins_page_1_limit_2(self):

        response = self.client.get('/logins/1/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(2, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(8+1, response.json['total'])
        self.assertIn("logins", response.json)
        self.assertTrue(response.json['next_uri'].endswith('/logins/2/2'))

        self.assertEqual(1, response.json['logins'][0]['id'])
        self.assertEqual(2, response.json['logins'][1]['id'])

    def test_get_logins_page_2_limit_2(self):

        response = self.client.get('/logins/2/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(2, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(2, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(8+1, response.json['total'])
        self.assertIn("logins", response.json)
        self.assertTrue(response.json['previous_uri'].endswith('/logins/1/2'))
        self.assertTrue(response.json['next_uri'].endswith('/logins/3/2'))

        self.assertEqual(3, response.json['logins'][0]['id'])
        self.assertEqual(4, response.json['logins'][1]['id'])

    def test_get_logins_user_id_1(self):

        response = self.client.get('/logins?user_id=1&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(25, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3+1, response.json['total'])
        self.assertIn("logins", response.json)

        self.assertEqual(1, response.json['logins'][0]['id'])
        self.assertEqual(2, response.json['logins'][1]['id'])
        self.assertEqual(3, response.json['logins'][2]['id'])
        self.assertEqual(9, response.json['logins'][3]['id'])
    
    def test_get_logins_username_user1(self):

        response = self.client.get('/logins?username=user2&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(25, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("logins", response.json)

        self.assertEqual(4, response.json['logins'][0]['id'])
        self.assertEqual(5, response.json['logins'][1]['id'])
        self.assertEqual(6, response.json['logins'][2]['id'])
    
    def test_get_logins_ip_address_9999(self):

        response = self.client.get('/logins?ip_address=9.9.9.9&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(25, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("logins", response.json)

        self.assertEqual(5, response.json['logins'][0]['id'])
        self.assertEqual(6, response.json['logins'][1]['id'])
        self.assertEqual(8, response.json['logins'][2]['id'])

    def test_get_logins_no_app_key(self):

        response = self.client.get('/logins')

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_get_logins_bad_app_key(self):

        response = self.client.get('/logins?app_key=BAD_APP_KEY')

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])

    def test_get_logins_unauthorized(self):

        response = self.client.get('/logins?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_get_logins_no_permission(self):

        response = self.client.get('/logins?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
