from tests.BaseTest import BaseTest
from test_fixtures import *
from tests.utils import get_http_basic_auth_credentials
    
class RegionsTest(BaseTest):

    def test_get_regions(self):

        response = self.client.get('/regions?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(6, response.json['total'])
        self.assertIn("regions", response.json)

        self.assertEqual(1, response.json['regions'][0]['id'])
        self.assertEqual("California", response.json['regions'][0]['name'])
        self.assertEqual("CA", response.json['regions'][0]['code_2'])
        self.assertNotIn("country_id", response.json['regions'][0])
        self.assertIn("country", response.json['regions'][0])
        self.assertEqual(1, response.json['regions'][0]['country']['id'])
        self.assertEqual("United States", response.json['regions'][0]['country']['name'])
        self.assertEqual("US", response.json['regions'][0]['country']['code_2'])
        self.assertEqual("USA", response.json['regions'][0]['country']['code_3'])
        self.assertEqual(1, response.json['regions'][0]['status'])
        self.assertEqual("2018-01-01T00:00:00+0000", response.json['regions'][0]['status_changed_at'])
        self.assertIn("created_at", response.json['regions'][0])
        self.assertIn("updated_at", response.json['regions'][0])

        self.assertEqual(2, response.json['regions'][1]['id'])
        self.assertEqual("Oregon", response.json['regions'][1]['name'])
        self.assertEqual("OR", response.json['regions'][1]['code_2'])
        self.assertNotIn("country_id", response.json['regions'][1])
        self.assertIn("country", response.json['regions'][1])
        self.assertEqual(1, response.json['regions'][1]['country']['id'])
        self.assertEqual("United States", response.json['regions'][1]['country']['name'])
        self.assertEqual("US", response.json['regions'][1]['country']['code_2'])
        self.assertEqual("USA", response.json['regions'][1]['country']['code_3'])
        self.assertEqual(1, response.json['regions'][1]['status'])
        self.assertEqual("2018-01-01T00:00:00+0000", response.json['regions'][1]['status_changed_at'])
        self.assertIn("created_at", response.json['regions'][1])
        self.assertIn("updated_at", response.json['regions'][1])
    
        self.assertEqual(3, response.json['regions'][2]['id'])
        self.assertEqual("Washington", response.json['regions'][2]['name'])
        self.assertEqual("WA", response.json['regions'][2]['code_2'])
        self.assertNotIn("country_id", response.json['regions'][2])
        self.assertIn("country", response.json['regions'][2])
        self.assertEqual(1, response.json['regions'][2]['country']['id'])
        self.assertEqual("United States", response.json['regions'][2]['country']['name'])
        self.assertEqual("US", response.json['regions'][2]['country']['code_2'])
        self.assertEqual("USA", response.json['regions'][2]['country']['code_3'])
        self.assertEqual(1, response.json['regions'][2]['status'])
        self.assertEqual("2018-01-01T00:00:00+0000", response.json['regions'][2]['status_changed_at'])
        self.assertIn("created_at", response.json['regions'][2])
        self.assertIn("updated_at", response.json['regions'][2])

        self.assertEqual(4, response.json['regions'][3]['id'])
        self.assertEqual("Alabama", response.json['regions'][3]['name'])
        self.assertEqual("AL", response.json['regions'][3]['code_2'])
        self.assertNotIn("country_id", response.json['regions'][3])
        self.assertIn("country", response.json['regions'][3])
        self.assertEqual(1, response.json['regions'][3]['country']['id'])
        self.assertEqual("United States", response.json['regions'][3]['country']['name'])
        self.assertEqual("US", response.json['regions'][3]['country']['code_2'])
        self.assertEqual("USA", response.json['regions'][3]['country']['code_3'])
        self.assertEqual(2, response.json['regions'][3]['status'])
        self.assertEqual("2018-01-02T00:00:00+0000", response.json['regions'][3]['status_changed_at'])
        self.assertIn("created_at", response.json['regions'][3])
        self.assertIn("updated_at", response.json['regions'][3])

        self.assertEqual(7, response.json['regions'][4]['id'])
        self.assertEqual("Arkansas", response.json['regions'][4]['name'])
        self.assertEqual("AR", response.json['regions'][4]['code_2'])
        self.assertNotIn("country_id", response.json['regions'][4])
        self.assertIn("country", response.json['regions'][4])
        self.assertEqual(1, response.json['regions'][4]['country']['id'])
        self.assertEqual("United States", response.json['regions'][4]['country']['name'])
        self.assertEqual("US", response.json['regions'][4]['country']['code_2'])
        self.assertEqual("USA", response.json['regions'][4]['country']['code_3'])
        self.assertEqual(5, response.json['regions'][4]['status'])
        self.assertEqual("2018-01-05T00:00:00+0000", response.json['regions'][4]['status_changed_at'])
        self.assertIn("created_at", response.json['regions'][4])
        self.assertIn("updated_at", response.json['regions'][4])

        self.assertEqual(8, response.json['regions'][5]['id'])
        self.assertEqual("British Columbia", response.json['regions'][5]['name'])
        self.assertEqual("BC", response.json['regions'][5]['code_2'])
        self.assertNotIn("country_id", response.json['regions'][5])
        self.assertIn("country", response.json['regions'][5])
        self.assertEqual(3, response.json['regions'][5]['country']['id'])
        self.assertEqual("Canada", response.json['regions'][5]['country']['name'])
        self.assertEqual("CA", response.json['regions'][5]['country']['code_2'])
        self.assertEqual("CAN", response.json['regions'][5]['country']['code_3'])
        self.assertEqual(1, response.json['regions'][5]['status'])
        self.assertEqual("2018-01-06T00:00:00+0000", response.json['regions'][5]['status_changed_at'])
        self.assertIn("created_at", response.json['regions'][5])
        self.assertIn("updated_at", response.json['regions'][5])
    
    def test_get_regions_id_desc(self):

        response = self.client.get('/regions?order_by=id.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(6, response.json['total'])
        self.assertIn("regions", response.json)

        self.assertEqual(8, response.json['regions'][0]['id'])
        self.assertEqual(7, response.json['regions'][1]['id'])
        self.assertEqual(4, response.json['regions'][2]['id'])
        self.assertEqual(3, response.json['regions'][3]['id'])
        self.assertEqual(2, response.json['regions'][4]['id'])
        self.assertEqual(1, response.json['regions'][5]['id'])
    
    def test_get_regions_name_asc(self):

        response = self.client.get('/regions?order_by=name.asc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(6, response.json['total'])
        self.assertIn("regions", response.json)

        self.assertEqual(4, response.json['regions'][0]['id'])
        self.assertEqual(7, response.json['regions'][1]['id'])
        self.assertEqual(8, response.json['regions'][2]['id'])
        self.assertEqual(1, response.json['regions'][3]['id'])
        self.assertEqual(2, response.json['regions'][4]['id'])
        self.assertEqual(3, response.json['regions'][5]['id'])
    
    def test_get_regions_name_desc(self):

        response = self.client.get('/regions?order_by=name.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(6, response.json['total'])
        self.assertIn("regions", response.json)

        self.assertEqual(3, response.json['regions'][0]['id'])
        self.assertEqual(2, response.json['regions'][1]['id'])
        self.assertEqual(1, response.json['regions'][2]['id'])
        self.assertEqual(8, response.json['regions'][3]['id'])
        self.assertEqual(7, response.json['regions'][4]['id'])
        self.assertEqual(4, response.json['regions'][5]['id'])
    
    def test_get_regions_code_2_asc(self):

        response = self.client.get('/regions?order_by=code_2.asc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(6, response.json['total'])
        self.assertIn("regions", response.json)

        self.assertEqual(4, response.json['regions'][0]['id'])
        self.assertEqual(7, response.json['regions'][1]['id'])
        self.assertEqual(8, response.json['regions'][2]['id'])
        self.assertEqual(1, response.json['regions'][3]['id'])
        self.assertEqual(2, response.json['regions'][4]['id'])
        self.assertEqual(3, response.json['regions'][5]['id'])
    
    def test_get_regions_code_2_desc(self):

        response = self.client.get('/regions?order_by=code_2.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(6, response.json['total'])
        self.assertIn("regions", response.json)

        self.assertEqual(3, response.json['regions'][0]['id'])
        self.assertEqual(2, response.json['regions'][1]['id'])
        self.assertEqual(1, response.json['regions'][2]['id'])
        self.assertEqual(8, response.json['regions'][3]['id'])
        self.assertEqual(7, response.json['regions'][4]['id'])
        self.assertEqual(4, response.json['regions'][5]['id'])
    
    def test_get_regions_page_2(self):

        response = self.client.get('/regions/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(204, response.status_code)
        self.assertTrue(None == response.json)

    def test_get_regions_page_1_limit_2(self):

        response = self.client.get('/regions/1/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(2, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(6, response.json['total'])
        self.assertIn("regions", response.json)
        self.assertTrue(response.json['next_uri'].endswith('/regions/2/2'))

        self.assertEqual(1, response.json['regions'][0]['id'])
        self.assertEqual(2, response.json['regions'][1]['id'])
    
    def test_get_regions_page_2_limit_2(self):

        response = self.client.get('/regions/2/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(2, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(2, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(6, response.json['total'])
        self.assertIn("regions", response.json)
        self.assertTrue(response.json['previous_uri'].endswith('/regions/1/2'))
        self.assertTrue(response.json['next_uri'].endswith('/regions/3/2'))

        self.assertEqual(3, response.json['regions'][0]['id'])
        self.assertEqual(4, response.json['regions'][1]['id'])
    
    def test_get_regions_country_1(self):

        response = self.client.get('/regions?country_id=1&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("regions", response.json)

        self.assertEqual(1, response.json['regions'][0]['id'])
        self.assertEqual(2, response.json['regions'][1]['id'])
        self.assertEqual(3, response.json['regions'][2]['id'])
        self.assertEqual(4, response.json['regions'][3]['id'])
        self.assertEqual(7, response.json['regions'][4]['id'])
    
    def test_get_regions_status_enabled(self):

        response = self.client.get('/regions?status=1&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(4, response.json['total'])
        self.assertIn("regions", response.json)

        self.assertEqual(1, response.json['regions'][0]['id'])
        self.assertEqual(2, response.json['regions'][1]['id'])
        self.assertEqual(3, response.json['regions'][2]['id'])
        self.assertEqual(8, response.json['regions'][3]['id'])
    
    def test_get_regions_status_disabled(self):

        response = self.client.get('/regions?status=2&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("regions", response.json)

        self.assertEqual(4, response.json['regions'][0]['id'])
    
    def test_get_regions_status_archived(self):

        response = self.client.get('/regions?status=3&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("regions", response.json)

        self.assertEqual(5, response.json['regions'][0]['id'])
    
    def test_get_regions_status_deleted(self):

        response = self.client.get('/regions?status=4&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("regions", response.json)

        self.assertEqual(6, response.json['regions'][0]['id'])
    
    def test_get_regions_status_pending(self):

        response = self.client.get('/regions?status=5&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("regions", response.json)

        self.assertEqual(7, response.json['regions'][0]['id'])
    
    def test_get_regions_no_app_key(self):

        response = self.client.get('/regions',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_get_regions_bad_app_key(self):

        response = self.client.get('/regions?app_key=BAD_APP_KEY',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_get_regions_unauthorized(self):

        response = self.client.get('/regions?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_get_regions_no_permission(self):

        response = self.client.get('/regions?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
