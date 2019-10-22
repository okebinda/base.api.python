from tests.BaseTest import BaseTest
from test_fixtures import *
from tests.utils import get_http_basic_auth_credentials
    
class RegionsTest(BaseTest):

    def test_get_regions(self):

        response = self.client.get(
            '/regions?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(404, response.status_code)
        self.assertEqual("Not found", response.json['error'])

    def test_get_regions_US(self):

        response = self.client.get(
            '/regions/US?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(100, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("regions", response.json)

        self.assertEqual(1, response.json['regions'][0]['id'])
        self.assertEqual("California", response.json['regions'][0]['name'])
        self.assertEqual("CA", response.json['regions'][0]['code_2'])
        self.assertNotIn("country_id", response.json['regions'][0])
        self.assertNotIn("country", response.json['regions'][0])
        self.assertNotIn("status", response.json['regions'][0])
        self.assertNotIn("status_changed_at", response.json['regions'][0])
        self.assertNotIn("created_at", response.json['regions'][0])
        self.assertNotIn("updated_at", response.json['regions'][0])

        self.assertEqual(2, response.json['regions'][1]['id'])
        self.assertEqual("Oregon", response.json['regions'][1]['name'])
        self.assertEqual("OR", response.json['regions'][1]['code_2'])        
        self.assertNotIn("country_id", response.json['regions'][1])
        self.assertNotIn("country", response.json['regions'][1])
        self.assertNotIn("status", response.json['regions'][1])
        self.assertNotIn("status_changed_at", response.json['regions'][1])
        self.assertNotIn("created_at", response.json['regions'][1])
        self.assertNotIn("updated_at", response.json['regions'][1])
    
        self.assertEqual(3, response.json['regions'][2]['id'])
        self.assertEqual("Washington", response.json['regions'][2]['name'])
        self.assertEqual("WA", response.json['regions'][2]['code_2'])
        self.assertNotIn("country_id", response.json['regions'][2])
        self.assertNotIn("country", response.json['regions'][2])
        self.assertNotIn("status", response.json['regions'][2])
        self.assertNotIn("status_changed_at", response.json['regions'][2])
        self.assertNotIn("created_at", response.json['regions'][2])
        self.assertNotIn("updated_at", response.json['regions'][2])
    
    def test_get_regions_CA(self):

        response = self.client.get(
            '/regions/CA?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(100, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("regions", response.json)

        self.assertEqual(8, response.json['regions'][0]['id'])
        self.assertEqual("British Columbia", response.json['regions'][0]['name'])
        self.assertEqual("BC", response.json['regions'][0]['code_2'])
        self.assertNotIn("country_id", response.json['regions'][0])
        self.assertNotIn("country", response.json['regions'][0])
        self.assertNotIn("status", response.json['regions'][0])
        self.assertNotIn("status_changed_at", response.json['regions'][0])
        self.assertNotIn("created_at", response.json['regions'][0])
        self.assertNotIn("updated_at", response.json['regions'][0])
    
    def test_get_regions_MX(self):

        response = self.client.get(
            '/regions/MX?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(204, response.status_code)
        self.assertTrue(None == response.json)

    def test_get_regions_US_id_asc(self):

        response = self.client.get(
            '/regions/US?order_by=id.asc&app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(100, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("regions", response.json)

        self.assertEqual(1, response.json['regions'][0]['id'])
        self.assertEqual(2, response.json['regions'][1]['id'])
        self.assertEqual(3, response.json['regions'][2]['id'])
    
    def test_get_regions_US_id_desc(self):

        response = self.client.get(
            '/regions/US?order_by=id.desc&app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(100, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("regions", response.json)

        self.assertEqual(3, response.json['regions'][0]['id'])
        self.assertEqual(2, response.json['regions'][1]['id'])
        self.assertEqual(1, response.json['regions'][2]['id'])
    
    def test_get_regions_US_name_asc(self):

        response = self.client.get(
            '/regions/US?order_by=name.asc&app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(100, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("regions", response.json)

        self.assertEqual(1, response.json['regions'][0]['id'])
        self.assertEqual(2, response.json['regions'][1]['id'])
        self.assertEqual(3, response.json['regions'][2]['id'])
    
    def test_get_regions_US_name_desc(self):

        response = self.client.get(
            '/regions/US?order_by=name.desc&app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(100, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("regions", response.json)

        self.assertEqual(3, response.json['regions'][0]['id'])
        self.assertEqual(2, response.json['regions'][1]['id'])
        self.assertEqual(1, response.json['regions'][2]['id'])
    
    def test_get_regions_US_code_2_asc(self):

        response = self.client.get(
            '/regions/US?order_by=code_2.asc&app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(100, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("regions", response.json)

        self.assertEqual(1, response.json['regions'][0]['id'])
        self.assertEqual(2, response.json['regions'][1]['id'])
        self.assertEqual(3, response.json['regions'][2]['id'])
    
    def test_get_regions_US_code_2_desc(self):

        response = self.client.get(
            '/regions/US?order_by=code_2.desc&app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(100, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("regions", response.json)

        self.assertEqual(3, response.json['regions'][0]['id'])
        self.assertEqual(2, response.json['regions'][1]['id'])
        self.assertEqual(1, response.json['regions'][2]['id'])
    
    def test_get_regions_US_page_2(self):

        response = self.client.get(
            '/regions/US/2?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(204, response.status_code)
        self.assertTrue(None == response.json)

    def test_get_regions_US_page_1_limit_2(self):

        response = self.client.get(
            '/regions/US/1/2?app_key=' + AppKeyData.id1_appkey1.key)
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(2, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("regions", response.json)
        self.assertTrue(response.json['next_uri'].endswith('/regions/US/2/2'))
        self.assertNotIn("previous_uri", response.json)

        self.assertEqual(1, response.json['regions'][0]['id'])
        self.assertEqual(2, response.json['regions'][1]['id'])
    
    def test_get_regions_US_page_2_limit_2(self):

        response = self.client.get(
            '/regions/US/2/2?app_key=' + AppKeyData.id1_appkey1.key)
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(2, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(2, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("regions", response.json)
        self.assertTrue(response.json['previous_uri'].endswith('/regions/US/1/2'))
        self.assertNotIn("next_uri", response.json)

        self.assertEqual(3, response.json['regions'][0]['id'])
    
    def test_get_regions_US_no_app_key(self):

        response = self.client.get('/regions/US')

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_get_regions_US_bad_app_key(self):

        response = self.client.get('/regions/US?app_key=BAD_APP_KEY')

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
