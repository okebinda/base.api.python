from tests.BaseTest import BaseTest
from test_fixtures import *
from tests.utils import get_http_basic_auth_credentials


class TermsOfServiceTest(BaseTest):

    def test_get_terms_of_service_current(self):

        response = self.client.get(
            '/terms_of_service/current?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, response.json['terms_of_service']['id'])
        self.assertEqual("This is TOS 2", response.json['terms_of_service']['text'])
        self.assertEqual("1.1", response.json['terms_of_service']['version'])
        self.assertEqual("2019-01-01T00:00:00+0000", response.json['terms_of_service']['publish_date'])
        self.assertNotIn("status", response.json['terms_of_service'])
        self.assertNotIn("status_changed_at", response.json['terms_of_service'])
        self.assertNotIn("created_at", response.json['terms_of_service'])
        self.assertNotIn("updated_at", response.json['terms_of_service'])
    
    def test_get_terms_of_service_current_no_app_key(self):

        response = self.client.get('/terms_of_service/current')

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_get_terms_of_service_current_bad_app_key(self):

        response = self.client.get(
            '/terms_of_service/current?app_key=BAD_APP_KEY')

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_get_terms_of_service(self):

        response = self.client.get(
            '/terms_of_service?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(404, response.status_code)
        self.assertEqual("Not found", response.json['error'])
