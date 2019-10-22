from tests.BaseTest import BaseTest
from test_fixtures import *
from tests.utils import get_http_basic_auth_credentials
    
class CountriesTest(BaseTest):

    def test_get_countries(self):

        response = self.client.get('/countries?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("countries", response.json)

        self.assertEqual(1, response.json['countries'][0]['id'])
        self.assertEqual("United States", response.json['countries'][0]['name'])
        self.assertEqual("US", response.json['countries'][0]['code_2'])
        self.assertEqual("USA", response.json['countries'][0]['code_3'])
        self.assertEqual(1, response.json['countries'][0]['status'])
        self.assertEqual("2018-01-01T00:00:00+0000", response.json['countries'][0]['status_changed_at'])
        self.assertIn("created_at", response.json['countries'][0])
        self.assertIn("updated_at", response.json['countries'][0])

        self.assertEqual(2, response.json['countries'][1]['id'])
        self.assertEqual("Mexico", response.json['countries'][1]['name'])
        self.assertEqual("MX", response.json['countries'][1]['code_2'])
        self.assertEqual("MEX", response.json['countries'][1]['code_3'])
        self.assertEqual(1, response.json['countries'][1]['status'])
        self.assertEqual("2018-01-01T00:00:00+0000", response.json['countries'][1]['status_changed_at'])
        self.assertIn("created_at", response.json['countries'][1])
        self.assertIn("updated_at", response.json['countries'][1])

        self.assertEqual(3, response.json['countries'][2]['id'])
        self.assertEqual("Canada", response.json['countries'][2]['name'])
        self.assertEqual("CA", response.json['countries'][2]['code_2'])
        self.assertEqual("CAN", response.json['countries'][2]['code_3'])
        self.assertEqual(1, response.json['countries'][2]['status'])
        self.assertEqual("2018-01-01T00:00:00+0000", response.json['countries'][2]['status_changed_at'])
        self.assertIn("created_at", response.json['countries'][2])
        self.assertIn("updated_at", response.json['countries'][2])

        self.assertEqual(4, response.json['countries'][3]['id'])
        self.assertEqual("France", response.json['countries'][3]['name'])
        self.assertEqual("FR", response.json['countries'][3]['code_2'])
        self.assertEqual("FRA", response.json['countries'][3]['code_3'])
        self.assertEqual(2, response.json['countries'][3]['status'])
        self.assertEqual("2018-01-02T00:00:00+0000", response.json['countries'][3]['status_changed_at'])
        self.assertIn("created_at", response.json['countries'][3])
        self.assertIn("updated_at", response.json['countries'][3])

        self.assertEqual(7, response.json['countries'][4]['id'])
        self.assertEqual("Germany", response.json['countries'][4]['name'])
        self.assertEqual("DE", response.json['countries'][4]['code_2'])
        self.assertEqual("DEU", response.json['countries'][4]['code_3'])
        self.assertEqual(5, response.json['countries'][4]['status'])
        self.assertEqual("2018-01-05T00:00:00+0000", response.json['countries'][4]['status_changed_at'])
        self.assertIn("created_at", response.json['countries'][4])
        self.assertIn("updated_at", response.json['countries'][4])
    
    def test_get_countries_id_desc(self):

        response = self.client.get('/countries?order_by=id.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("countries", response.json)

        self.assertEqual(7, response.json['countries'][0]['id'])
        self.assertEqual(4, response.json['countries'][1]['id'])
        self.assertEqual(3, response.json['countries'][2]['id'])
        self.assertEqual(2, response.json['countries'][3]['id'])
        self.assertEqual(1, response.json['countries'][4]['id'])
    
    def test_get_countries_name_asc(self):

        response = self.client.get('/countries?order_by=name.asc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("countries", response.json)

        self.assertEqual(3, response.json['countries'][0]['id'])
        self.assertEqual(4, response.json['countries'][1]['id'])
        self.assertEqual(7, response.json['countries'][2]['id'])
        self.assertEqual(2, response.json['countries'][3]['id'])
        self.assertEqual(1, response.json['countries'][4]['id'])
    
    def test_get_countries_name_desc(self):

        response = self.client.get('/countries?order_by=name.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("countries", response.json)

        self.assertEqual(1, response.json['countries'][0]['id'])
        self.assertEqual(2, response.json['countries'][1]['id'])
        self.assertEqual(7, response.json['countries'][2]['id'])
        self.assertEqual(4, response.json['countries'][3]['id'])
        self.assertEqual(3, response.json['countries'][4]['id'])
    
    def test_get_countries_code_2_asc(self):

        response = self.client.get('/countries?order_by=code_2.asc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("countries", response.json)

        self.assertEqual(3, response.json['countries'][0]['id'])
        self.assertEqual(7, response.json['countries'][1]['id'])
        self.assertEqual(4, response.json['countries'][2]['id'])
        self.assertEqual(2, response.json['countries'][3]['id'])
        self.assertEqual(1, response.json['countries'][4]['id'])
    
    def test_get_countries_code_2_desc(self):

        response = self.client.get('/countries?order_by=code_2.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("countries", response.json)

        self.assertEqual(1, response.json['countries'][0]['id'])
        self.assertEqual(2, response.json['countries'][1]['id'])
        self.assertEqual(4, response.json['countries'][2]['id'])
        self.assertEqual(7, response.json['countries'][3]['id'])
        self.assertEqual(3, response.json['countries'][4]['id'])
    
    def test_get_countries_code_3_asc(self):

        response = self.client.get('/countries?order_by=code_3.asc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("countries", response.json)

        self.assertEqual(3, response.json['countries'][0]['id'])
        self.assertEqual(7, response.json['countries'][1]['id'])
        self.assertEqual(4, response.json['countries'][2]['id'])
        self.assertEqual(2, response.json['countries'][3]['id'])
        self.assertEqual(1, response.json['countries'][4]['id'])
    
    def test_get_countries_code_3_desc(self):

        response = self.client.get('/countries?order_by=code_3.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("countries", response.json)

        self.assertEqual(1, response.json['countries'][0]['id'])
        self.assertEqual(2, response.json['countries'][1]['id'])
        self.assertEqual(4, response.json['countries'][2]['id'])
        self.assertEqual(7, response.json['countries'][3]['id'])
        self.assertEqual(3, response.json['countries'][4]['id'])
    
    def test_get_countries_page_2(self):

        response = self.client.get('/countries/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(204, response.status_code)
        self.assertTrue(None == response.json)
    
    def test_get_countries_page_1_limit_2(self):

        response = self.client.get('/countries/1/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(2, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("countries", response.json)
        self.assertTrue(response.json['next_uri'].endswith('/countries/2/2'))

        self.assertEqual(1, response.json['countries'][0]['id'])
        self.assertEqual(2, response.json['countries'][1]['id'])
    
    def test_get_countries_page_2_limit_2(self):

        response = self.client.get('/countries/2/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(2, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(2, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("countries", response.json)
        self.assertTrue(response.json['previous_uri'].endswith('/countries/1/2'))
        self.assertTrue(response.json['next_uri'].endswith('/countries/3/2'))

        self.assertEqual(3, response.json['countries'][0]['id'])
        self.assertEqual(4, response.json['countries'][1]['id'])
    
    def test_get_countries_status_enabled(self):

        response = self.client.get('/countries?status=1&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("countries", response.json)

        self.assertEqual(1, response.json['countries'][0]['id'])
        self.assertEqual(2, response.json['countries'][1]['id'])
        self.assertEqual(3, response.json['countries'][2]['id'])
    
    def test_get_countries_status_disabled(self):

        response = self.client.get('/countries?status=2&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("countries", response.json)

        self.assertEqual(4, response.json['countries'][0]['id'])
    
    def test_get_countries_status_archived(self):

        response = self.client.get('/countries?status=3&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("countries", response.json)

        self.assertEqual(5, response.json['countries'][0]['id'])
    
    def test_get_countries_status_deleted(self):

        response = self.client.get('/countries?status=4&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("countries", response.json)

        self.assertEqual(6, response.json['countries'][0]['id'])
    
    def test_get_countries_status_pending(self):

        response = self.client.get('/countries?status=5&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("countries", response.json)

        self.assertEqual(7, response.json['countries'][0]['id'])
    
    def test_get_countries_no_app_key(self):

        response = self.client.get('/countries',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_get_countries_bad_app_key(self):

        response = self.client.get('/countries?app_key=BAD_APP_KEY',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_get_countries_unauthorized(self):

        response = self.client.get('/countries?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_get_countries_no_permission(self):

        response = self.client.get('/countries?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
