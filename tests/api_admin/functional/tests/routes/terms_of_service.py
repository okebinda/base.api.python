from tests.BaseTest import BaseTest
from test_fixtures import *
from tests.utils import get_http_basic_auth_credentials
    
class TermsOfServiceTest(BaseTest):

    def test_get_terms_of_services(self):

        response = self.client.get(
            '/terms_of_services?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(4, response.json['total'])
        self.assertIn("terms_of_services", response.json)

        self.assertEqual(1, response.json['terms_of_services'][0]['id'])
        self.assertEqual("This is TOS 1", response.json['terms_of_services'][0]['text'])
        self.assertEqual("1.0", response.json['terms_of_services'][0]['version'])
        self.assertEqual("2018-06-15T00:00:00+0000", response.json['terms_of_services'][0]['publish_date'])
        self.assertEqual(1, response.json['terms_of_services'][0]['status'])
        self.assertEqual("2018-06-15T00:00:00+0000", response.json['terms_of_services'][0]['status_changed_at'])
        self.assertIn("created_at", response.json['terms_of_services'][0])
        self.assertIn("updated_at", response.json['terms_of_services'][0])

        self.assertEqual(2, response.json['terms_of_services'][1]['id'])
        self.assertEqual("This is TOS 2", response.json['terms_of_services'][1]['text'])
        self.assertEqual("1.1", response.json['terms_of_services'][1]['version'])
        self.assertEqual("2019-01-01T00:00:00+0000", response.json['terms_of_services'][1]['publish_date'])
        self.assertEqual(1, response.json['terms_of_services'][1]['status'])
        self.assertEqual("2019-01-01T00:00:00+0000", response.json['terms_of_services'][1]['status_changed_at'])
        self.assertIn("created_at", response.json['terms_of_services'][1])
        self.assertIn("updated_at", response.json['terms_of_services'][1])

        self.assertEqual(4, response.json['terms_of_services'][2]['id'])
        self.assertEqual("This is TOS 4", response.json['terms_of_services'][2]['text'])
        self.assertEqual("1.3", response.json['terms_of_services'][2]['version'])
        self.assertEqual("2019-01-20T00:00:00+0000", response.json['terms_of_services'][2]['publish_date'])
        self.assertEqual(2, response.json['terms_of_services'][2]['status'])
        self.assertEqual("2019-01-20T00:00:00+0000", response.json['terms_of_services'][2]['status_changed_at'])
        self.assertIn("created_at", response.json['terms_of_services'][2])
        self.assertIn("updated_at", response.json['terms_of_services'][2])

        self.assertEqual(6, response.json['terms_of_services'][3]['id'])
        self.assertEqual("This is TOS 6", response.json['terms_of_services'][3]['text'])
        self.assertEqual("2.0", response.json['terms_of_services'][3]['version'])
        self.assertEqual("2019-01-30T00:00:00+0000", response.json['terms_of_services'][3]['publish_date'])
        self.assertEqual(5, response.json['terms_of_services'][3]['status'])
        self.assertEqual("2019-01-30T00:00:00+0000", response.json['terms_of_services'][3]['status_changed_at'])
        self.assertIn("created_at", response.json['terms_of_services'][3])
        self.assertIn("updated_at", response.json['terms_of_services'][3])

    def test_get_terms_of_services_id_asc(self):

        response = self.client.get(
            '/terms_of_services?order_by=id.asc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(4, response.json['total'])
        self.assertIn("terms_of_services", response.json)

        self.assertEqual(1, response.json['terms_of_services'][0]['id'])
        self.assertEqual(2, response.json['terms_of_services'][1]['id'])
        self.assertEqual(4, response.json['terms_of_services'][2]['id'])
        self.assertEqual(6, response.json['terms_of_services'][3]['id'])
    
    def test_get_terms_of_services_id_desc(self):

        response = self.client.get(
            '/terms_of_services?order_by=id.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(4, response.json['total'])
        self.assertIn("terms_of_services", response.json)

        self.assertEqual(6, response.json['terms_of_services'][0]['id'])
        self.assertEqual(4, response.json['terms_of_services'][1]['id'])
        self.assertEqual(2, response.json['terms_of_services'][2]['id'])
        self.assertEqual(1, response.json['terms_of_services'][3]['id'])
    
    def test_get_terms_of_services_publish_date_asc(self):

        response = self.client.get(
            '/terms_of_services?order_by=publish_date.asc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(4, response.json['total'])
        self.assertIn("terms_of_services", response.json)

        self.assertEqual(1, response.json['terms_of_services'][0]['id'])
        self.assertEqual(2, response.json['terms_of_services'][1]['id'])
        self.assertEqual(4, response.json['terms_of_services'][2]['id'])
        self.assertEqual(6, response.json['terms_of_services'][3]['id'])
    
    def test_get_terms_of_services_publish_date_desc(self):

        response = self.client.get(
            '/terms_of_services?order_by=publish_date.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(4, response.json['total'])
        self.assertIn("terms_of_services", response.json)

        self.assertEqual(6, response.json['terms_of_services'][0]['id'])
        self.assertEqual(4, response.json['terms_of_services'][1]['id'])
        self.assertEqual(2, response.json['terms_of_services'][2]['id'])
        self.assertEqual(1, response.json['terms_of_services'][3]['id'])
    
    def test_get_terms_of_services_version_asc(self):

        response = self.client.get(
            '/terms_of_services?order_by=version.asc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(4, response.json['total'])
        self.assertIn("terms_of_services", response.json)

        self.assertEqual(1, response.json['terms_of_services'][0]['id'])
        self.assertEqual(2, response.json['terms_of_services'][1]['id'])
        self.assertEqual(4, response.json['terms_of_services'][2]['id'])
        self.assertEqual(6, response.json['terms_of_services'][3]['id'])
    
    def test_get_terms_of_services_version_desc(self):

        response = self.client.get(
            '/terms_of_services?order_by=version.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(4, response.json['total'])
        self.assertIn("terms_of_services", response.json)

        self.assertEqual(6, response.json['terms_of_services'][0]['id'])
        self.assertEqual(4, response.json['terms_of_services'][1]['id'])
        self.assertEqual(2, response.json['terms_of_services'][2]['id'])
        self.assertEqual(1, response.json['terms_of_services'][3]['id'])
    
    def test_get_terms_of_services_page_2(self):

        response = self.client.get(
            '/terms_of_services/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(204, response.status_code)
        self.assertTrue(None == response.json)

    def test_get_terms_of_services_page_1_limit_1(self):

        response = self.client.get(
            '/terms_of_services/1/1?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(1, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(4, response.json['total'])
        self.assertIn("next_uri", response.json)
        self.assertTrue(response.json['next_uri'].endswith('/terms_of_services/2/1'))
        self.assertIn("terms_of_services", response.json)

        self.assertEqual(1, response.json['terms_of_services'][0]['id'])
        self.assertEqual("This is TOS 1", response.json['terms_of_services'][0]['text'])
        self.assertEqual("1.0", response.json['terms_of_services'][0]['version'])
        self.assertEqual("2018-06-15T00:00:00+0000", response.json['terms_of_services'][0]['publish_date'])
        self.assertEqual(1, response.json['terms_of_services'][0]['status'])
        self.assertEqual("2018-06-15T00:00:00+0000", response.json['terms_of_services'][0]['status_changed_at'])
        self.assertIn("created_at", response.json['terms_of_services'][0])
        self.assertIn("updated_at", response.json['terms_of_services'][0])
    
    def test_get_terms_of_services_page_2_limit_1(self):

        response = self.client.get(
            '/terms_of_services/2/1?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(1, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(2, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(4, response.json['total'])
        self.assertIn("previous_uri", response.json)
        self.assertTrue(response.json['next_uri'].endswith('/terms_of_services/3/1'))
        self.assertTrue(response.json['previous_uri'].endswith('/terms_of_services/1/1'))
        self.assertIn("terms_of_services", response.json)

        self.assertEqual(2, response.json['terms_of_services'][0]['id'])
        self.assertEqual("This is TOS 2", response.json['terms_of_services'][0]['text'])
        self.assertEqual("1.1", response.json['terms_of_services'][0]['version'])
        self.assertEqual("2019-01-01T00:00:00+0000", response.json['terms_of_services'][0]['publish_date'])
        self.assertEqual(1, response.json['terms_of_services'][0]['status'])
        self.assertEqual("2019-01-01T00:00:00+0000", response.json['terms_of_services'][0]['status_changed_at'])
        self.assertIn("created_at", response.json['terms_of_services'][0])
        self.assertIn("updated_at", response.json['terms_of_services'][0])
    
    def test_get_terms_of_services_status_enabled(self):

        response = self.client.get(
            '/terms_of_services?status=1&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(2, response.json['total'])
        self.assertIn("terms_of_services", response.json)

        self.assertEqual(1, response.json['terms_of_services'][0]['id'])
        self.assertEqual(2, response.json['terms_of_services'][1]['id'])

    def test_get_terms_of_services_status_disabled(self):

        response = self.client.get(
            '/terms_of_services?status=2&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("terms_of_services", response.json)

        self.assertEqual(4, response.json['terms_of_services'][0]['id'])
    
    def test_get_terms_of_services_status_archived(self):

        response = self.client.get(
            '/terms_of_services?status=3&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("terms_of_services", response.json)

        self.assertEqual(3, response.json['terms_of_services'][0]['id'])
    
    def test_get_terms_of_services_status_deleted(self):

        response = self.client.get(
            '/terms_of_services?status=4&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("terms_of_services", response.json)

        self.assertEqual(5, response.json['terms_of_services'][0]['id'])
    
    def test_get_terms_of_services_status_pending(self):

        response = self.client.get(
            '/terms_of_services?status=5&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("terms_of_services", response.json)

        self.assertEqual(6, response.json['terms_of_services'][0]['id'])
    
    def test_get_terms_of_services_no_app_key(self):

        response = self.client.get(
            '/terms_of_services',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_get_terms_of_services_bad_app_key(self):

        response = self.client.get(
            '/terms_of_services?app_key=BAD_APP_KEY',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
        
    def test_get_terms_of_services_unauthorized(self):

        response = self.client.get('/terms_of_services?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_get_terms_of_services_no_permission(self):

        response = self.client.get(
            '/terms_of_services?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
    
    def test_get_terms_of_service_1(self):

        response = self.client.get(
            '/terms_of_service/1?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.json['terms_of_service']['id'])
        self.assertEqual("This is TOS 1", response.json['terms_of_service']['text'])
        self.assertEqual("1.0", response.json['terms_of_service']['version'])
        self.assertEqual("2018-06-15T00:00:00+0000", response.json['terms_of_service']['publish_date'])
        self.assertEqual(1, response.json['terms_of_service']['status'])
        self.assertEqual("2018-06-15T00:00:00+0000", response.json['terms_of_service']['status_changed_at'])
        self.assertIn("created_at", response.json['terms_of_service'])
        self.assertIn("updated_at", response.json['terms_of_service'])
    
    def test_get_terms_of_service_250(self):

        response = self.client.get(
            '/terms_of_service/250?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(404, response.status_code)
        self.assertEqual("Not found", response.json['error'])
    
    def test_get_terms_of_service_no_app_key(self):

        response = self.client.get(
            '/terms_of_service/1',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_get_terms_of_service_bad_app_key(self):

        response = self.client.get(
            '/terms_of_service/1?app_key=BAD_APP_KEY',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])

    def test_get_terms_of_service_unauthorized(self):

        response = self.client.get('/terms_of_service/1?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_get_terms_of_service_no_permission(self):

        response = self.client.get(
            '/terms_of_service/1?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
    
    def test_post_terms_of_services_error(self):

        response = self.client.post(
            '/terms_of_services?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"foo":"bar"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("text", response.json['error'])
        self.assertIn("publish_date", response.json['error'])
        self.assertIn("status", response.json['error'])
    
    def test_post_terms_of_services_success(self):

        response = self.client.post(
            '/terms_of_services?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"text":"This is TOS 7","version":"2.1","publish_date":"2019-02-05T08:00:00+0000","status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(201, response.status_code)
        self.assertEqual(7, response.json['terms_of_service']['id'])
        self.assertEqual("This is TOS 7", response.json['terms_of_service']['text'])
        self.assertEqual("2.1", response.json['terms_of_service']['version'])
        self.assertEqual("2019-02-05T08:00:00+0000", response.json['terms_of_service']['publish_date'])
        self.assertEqual(1, response.json['terms_of_service']['status'])
        self.assertIn("status_changed_at", response.json['terms_of_service'])
        self.assertIn("created_at", response.json['terms_of_service'])
        self.assertIn("updated_at", response.json['terms_of_service'])
    
    def test_post_terms_of_service_no_app_key(self):

        response = self.client.post(
            '/terms_of_services',
            data='{"text":"This is TOS 7","version":"2.1","publish_date":"2019-02-05T08:00:00+0000","status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_post_terms_of_service_bad_app_key(self):

        response = self.client.post(
            '/terms_of_services?app_key=BAD_APP_KEY',
            data='{"text":"This is TOS 7","version":"2.1","publish_date":"2019-02-05T08:00:00+0000","status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_post_terms_of_services_unauthorized(self):

        response = self.client.post(
            '/terms_of_services?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"text":"This is TOS 7","version":"2.1","publish_date":"2019-02-05T08:00:00+0000","status":1}',
            headers={
                "Content-Type": "application/json"})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_post_terms_of_services_no_permission(self):

        response = self.client.post(
            '/terms_of_services?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"text":"This is TOS 7","version":"2.1","publish_date":"2019-02-05T08:00:00+0000","status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
    
    def test_put_terms_of_service_error(self):

        response = self.client.put(
            '/terms_of_service/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"foo":"bar"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("text", response.json['error'])
        self.assertIn("publish_date", response.json['error'])
        self.assertIn("status", response.json['error'])

    def test_put_terms_of_service_empty(self):

        response = self.client.put(
            '/terms_of_service/250?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"text":"This is TOS 2a","version":"1.1.1","publish_date":"2019-01-23T11:00:00+0000","status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(404, response.status_code)
        self.assertEqual("Not found", response.json['error'])
    
    def test_put_terms_of_service_tos2(self):

        response = self.client.put(
            '/terms_of_service/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"text":"This is TOS 2a","version":"1.1.1","publish_date":"2019-01-23T11:00:00+0000","status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, response.json['terms_of_service']['id'])
        self.assertEqual("This is TOS 2a", response.json['terms_of_service']['text'])
        self.assertEqual("1.1.1", response.json['terms_of_service']['version'])
        self.assertEqual("2019-01-23T11:00:00+0000", response.json['terms_of_service']['publish_date'])
        self.assertEqual(1, response.json['terms_of_service']['status'])
        self.assertIn("status_changed_at", response.json['terms_of_service'])
        self.assertIn("created_at", response.json['terms_of_service'])
        self.assertIn("updated_at", response.json['terms_of_service'])
    
    def test_put_terms_of_service_no_app_key(self):

        response = self.client.put(
            '/terms_of_service/2',
            data='{"text":"This is TOS 2a","version":"1.1.1","publish_date":"2019-01-23T11:00:00+0000","status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_put_terms_of_service_bad_app_key(self):

        response = self.client.put(
            '/terms_of_service/2?app_key=BAD_APP_KEY',
            data='{"text":"This is TOS 2a","version":"1.1.1","publish_date":"2019-01-23T11:00:00+0000","status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_put_terms_of_service_unauthorized(self):

        response = self.client.put(
            '/terms_of_service/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"text":"This is TOS 2a","version":"1.1.1","publish_date":"2019-01-23T11:00:00+0000","status":1}',
            headers={
                "Content-Type": "application/json"})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_put_terms_of_service_no_permission(self):

        response = self.client.put(
            '/terms_of_service/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"text":"This is TOS 2a","version":"1.1.1","publish_date":"2019-01-23T11:00:00+0000","status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
    
    def test_delete_terms_of_service_empty(self):

        response = self.client.delete(
            '/terms_of_service/250?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(404, response.status_code)
        self.assertEqual("Not found", response.json['error'])
    
    def test_delete_terms_of_service_tos5(self):

        response = self.client.delete(
            '/terms_of_service/5?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(204, response.status_code)
        self.assertEqual(None, response.json)
    
    def test_delete_terms_of_service_no_app_key(self):

        response = self.client.delete(
            '/terms_of_service/5',
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_delete_terms_of_service_bad_app_key(self):

        response = self.client.delete(
            '/terms_of_service/5?app_key=BAD_APP_KEY',
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_delete_terms_of_service_unauthorized(self):

        response = self.client.delete('/terms_of_service/5?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_delete_terms_of_service_no_permission(self):

        response = self.client.delete(
            '/terms_of_service/5?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
