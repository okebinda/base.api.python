from tests.BaseTest import BaseTest
from test_fixtures import *
from tests.utils import get_http_basic_auth_credentials


class AppKeysTest(BaseTest):

    def test_get_app_keys(self):

        response = self.client.get('/app_keys?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(4, response.json['total'])
        self.assertIn("app_keys", response.json)

        self.assertEqual(1, response.json['app_keys'][0]['id'])
        self.assertEqual("Application 1", response.json['app_keys'][0]['application'])
        self.assertEqual("7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW", response.json['app_keys'][0]['key'])
        self.assertEqual(1, response.json['app_keys'][0]['status'])
        self.assertEqual("2018-01-01T00:00:00+0000", response.json['app_keys'][0]['status_changed_at'])
        self.assertIn("created_at", response.json['app_keys'][0])
        self.assertIn("updated_at", response.json['app_keys'][0])

        self.assertEqual(2, response.json['app_keys'][1]['id'])
        self.assertEqual("Application 2", response.json['app_keys'][1]['application'])
        self.assertEqual("cvBtQGgL9gNnSZk4DmKnva4QMcpTV7Mx", response.json['app_keys'][1]['key'])
        self.assertEqual(1, response.json['app_keys'][1]['status'])
        self.assertEqual("2018-01-05T00:00:00+0000", response.json['app_keys'][1]['status_changed_at'])
        self.assertIn("created_at", response.json['app_keys'][1])
        self.assertIn("updated_at", response.json['app_keys'][1])

        self.assertEqual(3, response.json['app_keys'][2]['id'])
        self.assertEqual("Application 3", response.json['app_keys'][2]['application'])
        self.assertEqual("9CR45hFpTahbqDvmZFJdENAKz5VPqLG3", response.json['app_keys'][2]['key'])
        self.assertEqual(2, response.json['app_keys'][2]['status'])
        self.assertEqual("2018-01-10T00:00:00+0000", response.json['app_keys'][2]['status_changed_at'])
        self.assertIn("created_at", response.json['app_keys'][2])
        self.assertIn("updated_at", response.json['app_keys'][2])

        self.assertEqual(6, response.json['app_keys'][3]['id'])
        self.assertEqual("Application 6", response.json['app_keys'][3]['application'])
        self.assertEqual("kP4k7vun5RwTBbESwHrCuDdFUtRchbVf", response.json['app_keys'][3]['key'])
        self.assertEqual(5, response.json['app_keys'][3]['status'])
        self.assertEqual("2018-01-25T00:00:00+0000", response.json['app_keys'][3]['status_changed_at'])
        self.assertIn("created_at", response.json['app_keys'][3])
        self.assertIn("updated_at", response.json['app_keys'][3])
    
    def test_get_app_keys_id_asc(self):

        response = self.client.get('/app_keys?order_by=id.asc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(4, response.json['total'])
        self.assertIn("app_keys", response.json)

        self.assertEqual(1, response.json['app_keys'][0]['id'])
        self.assertEqual(2, response.json['app_keys'][1]['id'])
        self.assertEqual(3, response.json['app_keys'][2]['id'])
        self.assertEqual(6, response.json['app_keys'][3]['id'])
    
    def test_get_app_keys_id_desc(self):

        response = self.client.get('/app_keys?order_by=id.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(4, response.json['total'])
        self.assertIn("app_keys", response.json)

        self.assertEqual(6, response.json['app_keys'][0]['id'])
        self.assertEqual(3, response.json['app_keys'][1]['id'])
        self.assertEqual(2, response.json['app_keys'][2]['id'])
        self.assertEqual(1, response.json['app_keys'][3]['id'])

    def test_get_app_keys_application_asc(self):

        response = self.client.get('/app_keys?order_by=application.asc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(4, response.json['total'])
        self.assertIn("app_keys", response.json)

        self.assertEqual(1, response.json['app_keys'][0]['id'])
        self.assertEqual(2, response.json['app_keys'][1]['id'])
        self.assertEqual(3, response.json['app_keys'][2]['id'])
        self.assertEqual(6, response.json['app_keys'][3]['id'])
    
    def test_get_app_keys_application_desc(self):

        response = self.client.get('/app_keys?order_by=application.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(4, response.json['total'])
        self.assertIn("app_keys", response.json)

        self.assertEqual(6, response.json['app_keys'][0]['id'])
        self.assertEqual(3, response.json['app_keys'][1]['id'])
        self.assertEqual(2, response.json['app_keys'][2]['id'])
        self.assertEqual(1, response.json['app_keys'][3]['id'])
    
    def test_get_app_keys_page_2(self):

        response = self.client.get('/app_keys/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(204, response.status_code)
        self.assertTrue(None == response.json)

    def test_get_app_keys_page_1_limit_1(self):

        response = self.client.get('/app_keys/1/1?app_key=' + AppKeyData.id1_appkey1.key,
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
        self.assertTrue(response.json['next_uri'].endswith('/app_keys/2/1'))
        self.assertIn("app_keys", response.json)

        self.assertEqual(1, response.json['app_keys'][0]['id'])
        self.assertEqual("Application 1", response.json['app_keys'][0]['application'])
        self.assertEqual("7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW", response.json['app_keys'][0]['key'])
        self.assertEqual(1, response.json['app_keys'][0]['status'])
        self.assertEqual("2018-01-01T00:00:00+0000", response.json['app_keys'][0]['status_changed_at'])
        self.assertIn("created_at", response.json['app_keys'][0])
        self.assertIn("updated_at", response.json['app_keys'][0])

    def test_get_app_keys_page_2_limit_1(self):

        response = self.client.get('/app_keys/2/1?app_key=' + AppKeyData.id1_appkey1.key,
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
        self.assertTrue(response.json['next_uri'].endswith('/app_keys/3/1'))
        self.assertTrue(response.json['previous_uri'].endswith('/app_keys/1/1'))
        self.assertIn("app_keys", response.json)

        self.assertEqual(2, response.json['app_keys'][0]['id'])
        self.assertEqual("Application 2", response.json['app_keys'][0]['application'])
        self.assertEqual("cvBtQGgL9gNnSZk4DmKnva4QMcpTV7Mx", response.json['app_keys'][0]['key'])
        self.assertEqual(1, response.json['app_keys'][0]['status'])
        self.assertEqual("2018-01-05T00:00:00+0000", response.json['app_keys'][0]['status_changed_at'])
        self.assertIn("created_at", response.json['app_keys'][0])
        self.assertIn("updated_at", response.json['app_keys'][0])
    
    def test_get_app_keys_status_enabled(self):

        response = self.client.get('/app_keys?status=1&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(2, response.json['total'])
        self.assertIn("app_keys", response.json)

        self.assertEqual(1, response.json['app_keys'][0]['id'])
        self.assertEqual(2, response.json['app_keys'][1]['id'])
    
    def test_get_app_keys_status_disabled(self):

        response = self.client.get('/app_keys?status=2&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("app_keys", response.json)

        self.assertEqual(3, response.json['app_keys'][0]['id'])
    
    def test_get_app_keys_status_archived(self):

        response = self.client.get('/app_keys?status=3&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("app_keys", response.json)

        self.assertEqual(4, response.json['app_keys'][0]['id'])
    
    def test_get_app_keys_status_deleted(self):

        response = self.client.get('/app_keys?status=4&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("app_keys", response.json)

        self.assertEqual(5, response.json['app_keys'][0]['id'])
    
    def test_get_app_keys_status_pending(self):

        response = self.client.get('/app_keys?status=5&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("app_keys", response.json)

        self.assertEqual(6, response.json['app_keys'][0]['id'])
    
    def test_get_app_keys_no_app_key(self):

        response = self.client.get('/app_keys',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_get_app_keys_bad_app_key(self):

        response = self.client.get('/app_keys?app_key=BAD_APP_KEY',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_get_app_keys_unauthorized(self):

        response = self.client.get('/app_keys?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_get_app_keys_no_permission(self):

        response = self.client.get('/app_keys?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])

    def test_get_app_key_1(self):

        response = self.client.get('/app_key/1?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.json['app_key']['id'])
        self.assertEqual("Application 1", response.json['app_key']['application'])
        self.assertEqual("7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW", response.json['app_key']['key'])
        self.assertEqual(1, response.json['app_key']['status'])
        self.assertEqual("2018-01-01T00:00:00+0000", response.json['app_key']['status_changed_at'])
        self.assertIn("created_at", response.json['app_key'])
        self.assertIn("updated_at", response.json['app_key'])
    
    def test_get_app_key_250(self):

        response = self.client.get('/app_key/250?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(404, response.status_code)
        self.assertEqual("Not found", response.json['error'])
    
    def test_get_app_key_no_app_key(self):

        response = self.client.get('/app_key/1',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_get_app_key_bad_app_key(self):

        response = self.client.get('/app_key/1?app_key=BAD_APP_KEY',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_get_app_key_unauthorized(self):

        response = self.client.get('/app_key/1?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_get_app_key_no_permission(self):

        response = self.client.get('/app_key/1?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
    
    def test_post_app_keys_error(self):

        response = self.client.post(
            '/app_keys?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"foo":"bar"}', headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("application", response.json['error'])
        self.assertIn("key", response.json['error'])
        self.assertIn("status", response.json['error'])

    def test_post_app_keys_unique_key_error(self):

        response = self.client.post(
            '/app_keys?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"application":"Application 7","key":"7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW","status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("key", response.json['error'])
        self.assertEqual(["Value must be unique."], response.json['error']['key'])
        self.assertNotIn("application", response.json['error'])
        self.assertNotIn("status", response.json['error'])

    def test_post_app_keys_success(self):

        response = self.client.post(
            '/app_keys?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"application":"Application 7","key":"DWRDwTSSQDZSwM76wpWAmAedkfZkTZqV","status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(201, response.status_code)
        self.assertEqual(7, response.json['app_key']['id'])
        self.assertEqual("Application 7", response.json['app_key']['application'])
        self.assertEqual("DWRDwTSSQDZSwM76wpWAmAedkfZkTZqV", response.json['app_key']['key'])
        self.assertEqual(1, response.json['app_key']['status'])
        self.assertIn("status_changed_at", response.json['app_key'])
        self.assertIn("created_at", response.json['app_key'])
        self.assertIn("updated_at", response.json['app_key'])
    
    def test_post_app_keys_no_app_key(self):

        response = self.client.post(
            '/app_keys',
            data='{"application":"Application 7","key":"DWRDwTSSQDZSwM76wpWAmAedkfZkTZqV","status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_post_app_keys_bad_app_key(self):

        response = self.client.post(
            '/app_keys?app_key=BAD_APP_KEY',
            data='{"application":"Application 7","key":"DWRDwTSSQDZSwM76wpWAmAedkfZkTZqV","status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])

    def test_post_app_keys_unauthorized(self):

        response = self.client.post(
            '/app_keys?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"application":"Application 7","key":"DWRDwTSSQDZSwM76wpWAmAedkfZkTZqV","status":1}',
            headers={
                "Content-Type": "application/json"})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_post_app_keys_no_permission(self):

        response = self.client.post(
            '/app_keys?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"application":"Application 7","key":"DWRDwTSSQDZSwM76wpWAmAedkfZkTZqV","status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
    
    def test_put_app_key_error(self):

        response = self.client.put(
            '/app_key/2?app_key=' + AppKeyData.id1_appkey1.key, data='{"foo":"bar"}', headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("application", response.json['error'])
        self.assertIn("key", response.json['error'])
        self.assertIn("status", response.json['error'])
    
    def test_put_app_key_empty(self):

        response = self.client.put(
            '/app_key/250?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"application":"Application 7","key":"DWRDwTSSQDZSwM76wpWAmAedkfZkTZqV","status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(404, response.status_code)
        self.assertEqual("Not found", response.json['error'])

    def test_put_app_key_unique_key_error(self):

        response = self.client.put(
            '/app_key/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"application":"Application 2a","key":"7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW","status":5}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("key", response.json['error'])
        self.assertEqual(["Value must be unique."], response.json['error']['key'])
        self.assertNotIn("application", response.json['error'])
        self.assertNotIn("status", response.json['error'])

    def test_put_app_key_id2(self):

        response = self.client.put(
            '/app_key/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"application":"Application 2a","key":"qgRrkRCyJJ5smD3uY9mugzPsD7EsKT7c","status":5}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, response.json['app_key']['id'])
        self.assertEqual("Application 2a", response.json['app_key']['application'])
        self.assertEqual("qgRrkRCyJJ5smD3uY9mugzPsD7EsKT7c", response.json['app_key']['key'])
        self.assertEqual(5, response.json['app_key']['status'])
        self.assertIn("status_changed_at", response.json['app_key'])
        self.assertIn("created_at", response.json['app_key'])
        self.assertIn("updated_at", response.json['app_key'])

    def test_put_app_key_no_app_key(self):

        response = self.client.put(
            '/app_key/2',
            data='{"application":"Application 2a","key":"qgRrkRCyJJ5smD3uY9mugzPsD7EsKT7c","status":5}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_put_app_key_bad_app_key(self):

        response = self.client.put(
            '/app_key/2?app_key=BAD_APP_KEY',
            data='{"application":"Application 2a","key":"qgRrkRCyJJ5smD3uY9mugzPsD7EsKT7c","status":5}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_put_app_key_unauthorized(self):

        response = self.client.put(
            '/app_key/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"application":"Application 2a","key":"qgRrkRCyJJ5smD3uY9mugzPsD7EsKT7c","status":5}',
            headers={
                "Content-Type": "application/json"})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_put_app_key_no_permission(self):

        response = self.client.put(
            '/app_key/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"application":"Application 2a","key":"qgRrkRCyJJ5smD3uY9mugzPsD7EsKT7c","status":5}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
    
    def test_delete_app_key_empty(self):

        response = self.client.delete(
            '/app_key/250?app_key=' + AppKeyData.id1_appkey1.key,
            headers={
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(404, response.status_code)
        self.assertEqual("Not found", response.json['error'])
    
    def test_delete_app_key_id5(self):

        response = self.client.delete(
            '/app_key/5?app_key=' + AppKeyData.id1_appkey1.key,
            headers={
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(204, response.status_code)
        self.assertEqual(None, response.json)

    def test_delete_app_key_no_app_key(self):

        response = self.client.delete('/app_key/5',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_delete_app_key_bad_app_key(self):

        response = self.client.delete('/app_key/5?app_key=BAD_APP_KEY',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_delete_app_key_unauthorized(self):

        response = self.client.delete('/app_key/5?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_delete_app_key_no_permission(self):

        response = self.client.delete(
            '/app_key/5?app_key=' + AppKeyData.id1_appkey1.key,
            headers={
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
