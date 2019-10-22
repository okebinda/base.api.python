from tests.BaseTest import BaseTest
from test_fixtures import *
from tests.utils import get_http_basic_auth_credentials
    
class CountriesTest(BaseTest):

    def test_get_countries(self):

        response = self.client.get(
            '/countries?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(250, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("countries", response.json)

        self.assertEqual(3, response.json['countries'][0]['id'])
        self.assertEqual("Canada", response.json['countries'][0]['name'])
        self.assertEqual("CA", response.json['countries'][0]['code_2'])
        self.assertEqual("CAN", response.json['countries'][0]['code_3'])
        self.assertTrue(response.json['countries'][0]['regions_uri'].endswith('/regions/CA'))
        self.assertNotIn("status", response.json['countries'][0])
        self.assertNotIn("status_changed_at", response.json['countries'][0])
        self.assertNotIn("created_at", response.json['countries'][0])
        self.assertNotIn("updated_at", response.json['countries'][0])

        self.assertEqual(2, response.json['countries'][1]['id'])
        self.assertEqual("Mexico", response.json['countries'][1]['name'])
        self.assertEqual("MX", response.json['countries'][1]['code_2'])
        self.assertEqual("MEX", response.json['countries'][1]['code_3'])
        self.assertTrue(response.json['countries'][1]['regions_uri'].endswith('/regions/MX'))
        self.assertNotIn("status", response.json['countries'][1])
        self.assertNotIn("status_changed_at", response.json['countries'][1])
        self.assertNotIn("created_at", response.json['countries'][1])
        self.assertNotIn("updated_at", response.json['countries'][1])

        self.assertEqual(1, response.json['countries'][2]['id'])
        self.assertEqual("United States", response.json['countries'][2]['name'])
        self.assertEqual("US", response.json['countries'][2]['code_2'])
        self.assertEqual("USA", response.json['countries'][2]['code_3'])
        self.assertTrue(response.json['countries'][2]['regions_uri'].endswith('/regions/US'))
        self.assertNotIn("status", response.json['countries'][2])
        self.assertNotIn("status_changed_at", response.json['countries'][2])
        self.assertNotIn("created_at", response.json['countries'][2])
        self.assertNotIn("updated_at", response.json['countries'][2])

    def test_get_countries_id_asc(self):

        response = self.client.get(
            '/countries?order_by=id.asc&app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(250, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("countries", response.json)

        self.assertEqual(1, response.json['countries'][0]['id'])
        self.assertEqual(2, response.json['countries'][1]['id'])
        self.assertEqual(3, response.json['countries'][2]['id'])

    def test_get_countries_id_desc(self):

        response = self.client.get(
            '/countries?order_by=id.desc&app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(250, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("countries", response.json)

        self.assertEqual(3, response.json['countries'][0]['id'])
        self.assertEqual(2, response.json['countries'][1]['id'])
        self.assertEqual(1, response.json['countries'][2]['id'])
    
    def test_get_countries_name_asc(self):

        response = self.client.get(
            '/countries?order_by=name.asc&app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(250, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("countries", response.json)

        self.assertEqual(3, response.json['countries'][0]['id'])
        self.assertEqual(2, response.json['countries'][1]['id'])
        self.assertEqual(1, response.json['countries'][2]['id'])
    
    def test_get_countries_name_desc(self):

        response = self.client.get(
            '/countries?order_by=name.desc&app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(250, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("countries", response.json)

        self.assertEqual(1, response.json['countries'][0]['id'])
        self.assertEqual(2, response.json['countries'][1]['id'])
        self.assertEqual(3, response.json['countries'][2]['id'])
    
    def test_get_countries_code_2_asc(self):

        response = self.client.get(
            '/countries?order_by=code_2.asc&app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(250, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("countries", response.json)

        self.assertEqual(3, response.json['countries'][0]['id'])
        self.assertEqual(2, response.json['countries'][1]['id'])
        self.assertEqual(1, response.json['countries'][2]['id'])
    
    def test_get_countries_code_2_desc(self):

        response = self.client.get(
            '/countries?order_by=code_2.desc&app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(250, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("countries", response.json)

        self.assertEqual(1, response.json['countries'][0]['id'])
        self.assertEqual(2, response.json['countries'][1]['id'])
        self.assertEqual(3, response.json['countries'][2]['id'])
    
    def test_get_countries_code_3_asc(self):

        response = self.client.get(
            '/countries?order_by=code_3.asc&app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(250, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("countries", response.json)

        self.assertEqual(3, response.json['countries'][0]['id'])
        self.assertEqual(2, response.json['countries'][1]['id'])
        self.assertEqual(1, response.json['countries'][2]['id'])
    
    def test_get_countries_code_3_desc(self):

        response = self.client.get(
            '/countries?order_by=code_3.desc&app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(250, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("countries", response.json)

        self.assertEqual(1, response.json['countries'][0]['id'])
        self.assertEqual(2, response.json['countries'][1]['id'])
        self.assertEqual(3, response.json['countries'][2]['id'])
    
    def test_get_countries_page_2(self):

        response = self.client.get(
            '/countries/2?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(204, response.status_code)
        self.assertTrue(None == response.json)
    
    def test_get_countries_page_1_limit_2(self):

        response = self.client.get(
            '/countries/1/2?app_key=' + AppKeyData.id1_appkey1.key)
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(2, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("countries", response.json)
        self.assertTrue(response.json['next_uri'].endswith('/countries/2/2'))
        self.assertNotIn("previous_uri", response.json)

        self.assertEqual(3, response.json['countries'][0]['id'])
        self.assertEqual(2, response.json['countries'][1]['id'])
    
    def test_get_countries_page_2_limit_2(self):

        response = self.client.get(
            '/countries/2/2?app_key=' + AppKeyData.id1_appkey1.key)
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(2, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(2, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("countries", response.json)
        self.assertTrue(response.json['previous_uri'].endswith('/countries/1/2'))
        self.assertNotIn("next_uri", response.json)

        self.assertEqual(1, response.json['countries'][0]['id'])
    
    def test_get_countries_no_app_key(self):

        response = self.client.get('/countries')

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_get_countries_bad_app_key(self):

        response = self.client.get('/countries?app_key=BAD_APP_KEY')

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
