from tests.BaseTest import BaseTest
from test_fixtures import *
from tests.utils import get_http_basic_auth_credentials


class UserProfilesTest(BaseTest):

    def test_get_user_profiles(self):

        response = self.client.get(
            '/user_profiles?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(6, response.json['total'])
        self.assertIn("user_profiles", response.json)

        self.assertEqual(1, response.json['user_profiles'][0]['id'])
        self.assertEqual(1, response.json['user_profiles'][0]['user_id'])
        self.assertEqual("Fiona", response.json['user_profiles'][0]['first_name'])
        self.assertEqual("Farnham", response.json['user_profiles'][0]['last_name'])
        self.assertEqual("2018-12-01T00:00:00+0000", response.json['user_profiles'][0]['joined_at'])
        self.assertEqual(1, response.json['user_profiles'][0]['status'])
        self.assertEqual("2018-12-01T00:00:00+0000", response.json['user_profiles'][0]['status_changed_at'])
        self.assertIn("created_at", response.json['user_profiles'][0])
        self.assertIn("updated_at", response.json['user_profiles'][0])

        self.assertEqual(2, response.json['user_profiles'][1]['id'])
        self.assertEqual(2, response.json['user_profiles'][1]['user_id'])
        self.assertEqual("Lynne", response.json['user_profiles'][1]['first_name'])
        self.assertEqual("Harford", response.json['user_profiles'][1]['last_name'])
        self.assertEqual("2018-12-10T00:00:00+0000", response.json['user_profiles'][1]['joined_at'])
        self.assertEqual(1, response.json['user_profiles'][1]['status'])
        self.assertEqual("2018-12-10T00:00:00+0000", response.json['user_profiles'][1]['status_changed_at'])
        self.assertIn("created_at", response.json['user_profiles'][1])
        self.assertIn("updated_at", response.json['user_profiles'][1])

        self.assertEqual(3, response.json['user_profiles'][2]['id'])
        self.assertEqual(3, response.json['user_profiles'][2]['user_id'])
        self.assertEqual("Duane", response.json['user_profiles'][2]['first_name'])
        self.assertEqual("Hargrave", response.json['user_profiles'][2]['last_name'])
        self.assertEqual("2018-12-15T00:00:00+0000", response.json['user_profiles'][2]['joined_at'])
        self.assertEqual(1, response.json['user_profiles'][2]['status'])
        self.assertEqual("2018-12-15T00:00:00+0000", response.json['user_profiles'][2]['status_changed_at'])
        self.assertIn("created_at", response.json['user_profiles'][2])
        self.assertIn("updated_at", response.json['user_profiles'][2])

        self.assertEqual(5, response.json['user_profiles'][3]['id'])
        self.assertEqual(5, response.json['user_profiles'][3]['user_id'])
        self.assertEqual("Elroy", response.json['user_profiles'][3]['first_name'])
        self.assertEqual("Hunnicutt", response.json['user_profiles'][3]['last_name'])
        self.assertEqual("2018-12-20T00:00:00+0000", response.json['user_profiles'][3]['joined_at'])
        self.assertEqual(2, response.json['user_profiles'][3]['status'])
        self.assertEqual("2018-12-25T00:00:00+0000", response.json['user_profiles'][3]['status_changed_at'])
        self.assertIn("created_at", response.json['user_profiles'][3])
        self.assertIn("updated_at", response.json['user_profiles'][3])

        self.assertEqual(6, response.json['user_profiles'][4]['id'])
        self.assertEqual(6, response.json['user_profiles'][4]['user_id'])
        self.assertEqual("Alease", response.json['user_profiles'][4]['first_name'])
        self.assertEqual("Richards", response.json['user_profiles'][4]['last_name'])
        self.assertEqual("2018-12-29T00:00:00+0000", response.json['user_profiles'][4]['joined_at'])
        self.assertEqual(5, response.json['user_profiles'][4]['status'])
        self.assertEqual("2018-12-30T00:00:00+0000", response.json['user_profiles'][4]['status_changed_at'])
        self.assertIn("created_at", response.json['user_profiles'][4])
        self.assertIn("updated_at", response.json['user_profiles'][4])

        self.assertEqual(8, response.json['user_profiles'][5]['id'])
        self.assertEqual(8, response.json['user_profiles'][5]['user_id'])
        self.assertEqual("Luke", response.json['user_profiles'][5]['first_name'])
        self.assertEqual("Tennyson", response.json['user_profiles'][5]['last_name'])
        self.assertEqual("2019-01-10T00:00:00+0000", response.json['user_profiles'][5]['joined_at'])
        self.assertEqual(1, response.json['user_profiles'][5]['status'])
        self.assertEqual("2019-01-10T00:00:00+0000", response.json['user_profiles'][5]['status_changed_at'])
        self.assertIn("created_at", response.json['user_profiles'][5])
        self.assertIn("updated_at", response.json['user_profiles'][5])
    
    def test_get_user_profiles_id_asc(self):

        response = self.client.get(
            '/user_profiles?order_by=id.asc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(6, response.json['total'])
        self.assertIn("user_profiles", response.json)

        self.assertEqual(1, response.json['user_profiles'][0]['id'])
        self.assertEqual(2, response.json['user_profiles'][1]['id'])
        self.assertEqual(3, response.json['user_profiles'][2]['id'])
        self.assertEqual(5, response.json['user_profiles'][3]['id'])
        self.assertEqual(6, response.json['user_profiles'][4]['id'])
        self.assertEqual(8, response.json['user_profiles'][5]['id'])

    def test_get_user_profiles_id_desc(self):

        response = self.client.get(
            '/user_profiles?order_by=id.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(6, response.json['total'])
        self.assertIn("user_profiles", response.json)

        self.assertEqual(8, response.json['user_profiles'][0]['id'])
        self.assertEqual(6, response.json['user_profiles'][1]['id'])
        self.assertEqual(5, response.json['user_profiles'][2]['id'])
        self.assertEqual(3, response.json['user_profiles'][3]['id'])
        self.assertEqual(2, response.json['user_profiles'][4]['id'])
        self.assertEqual(1, response.json['user_profiles'][5]['id'])

    def test_get_user_profiles_user_id_asc(self):

        response = self.client.get(
            '/user_profiles?order_by=user_id.asc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(6, response.json['total'])
        self.assertIn("user_profiles", response.json)

        self.assertEqual(1, response.json['user_profiles'][0]['id'])
        self.assertEqual(2, response.json['user_profiles'][1]['id'])
        self.assertEqual(3, response.json['user_profiles'][2]['id'])
        self.assertEqual(5, response.json['user_profiles'][3]['id'])
        self.assertEqual(6, response.json['user_profiles'][4]['id'])
        self.assertEqual(8, response.json['user_profiles'][5]['id'])
    
    def test_get_user_profiles_user_id_desc(self):

        response = self.client.get(
            '/user_profiles?order_by=user_id.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(6, response.json['total'])
        self.assertIn("user_profiles", response.json)

        self.assertEqual(8, response.json['user_profiles'][0]['id'])
        self.assertEqual(6, response.json['user_profiles'][1]['id'])
        self.assertEqual(5, response.json['user_profiles'][2]['id'])
        self.assertEqual(3, response.json['user_profiles'][3]['id'])
        self.assertEqual(2, response.json['user_profiles'][4]['id'])
        self.assertEqual(1, response.json['user_profiles'][5]['id'])

    def test_get_user_profiles_joined_at_asc(self):

        response = self.client.get(
            '/user_profiles?order_by=joined_at.asc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(6, response.json['total'])
        self.assertIn("user_profiles", response.json)

        self.assertEqual(1, response.json['user_profiles'][0]['id'])
        self.assertEqual(2, response.json['user_profiles'][1]['id'])
        self.assertEqual(3, response.json['user_profiles'][2]['id'])
        self.assertEqual(5, response.json['user_profiles'][3]['id'])
        self.assertEqual(6, response.json['user_profiles'][4]['id'])
        self.assertEqual(8, response.json['user_profiles'][5]['id'])
    
    def test_get_user_profiles_joined_at_desc(self):

        response = self.client.get(
            '/user_profiles?order_by=joined_at.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(6, response.json['total'])
        self.assertIn("user_profiles", response.json)

        self.assertEqual(8, response.json['user_profiles'][0]['id'])
        self.assertEqual(6, response.json['user_profiles'][1]['id'])
        self.assertEqual(5, response.json['user_profiles'][2]['id'])
        self.assertEqual(3, response.json['user_profiles'][3]['id'])
        self.assertEqual(2, response.json['user_profiles'][4]['id'])
        self.assertEqual(1, response.json['user_profiles'][5]['id'])
    
    def test_get_user_profiles_page_2(self):

        response = self.client.get(
            '/user_profiles/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(204, response.status_code)
        self.assertTrue(None == response.json)
    
    def test_get_user_profiles_page_1_limit_2(self):

        response = self.client.get(
            '/user_profiles/1/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(2, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(6, response.json['total'])
        self.assertIn("next_uri", response.json)
        self.assertTrue(response.json['next_uri'].endswith('/user_profiles/2/2'))
        self.assertIn("user_profiles", response.json)

        self.assertEqual(1, response.json['user_profiles'][0]['id'])
        self.assertEqual(2, response.json['user_profiles'][1]['id'])

    def test_get_user_profiles_page_2_limit_2(self):

        response = self.client.get(
            '/user_profiles/2/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(2, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(2, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(6, response.json['total'])
        self.assertIn("next_uri", response.json)
        self.assertTrue(response.json['next_uri'].endswith('/user_profiles/3/2'))
        self.assertIn("previous_uri", response.json)
        self.assertTrue(response.json['previous_uri'].endswith('/user_profiles/1/2'))
        self.assertIn("user_profiles", response.json)

        self.assertEqual(3, response.json['user_profiles'][0]['id'])
        self.assertEqual(5, response.json['user_profiles'][1]['id'])

    def test_get_user_profiles_status_enabled(self):

        response = self.client.get(
            '/user_profiles?status=1&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(4, response.json['total'])
        self.assertIn("user_profiles", response.json)

        self.assertEqual(1, response.json['user_profiles'][0]['id'])
        self.assertEqual(2, response.json['user_profiles'][1]['id'])
        self.assertEqual(3, response.json['user_profiles'][2]['id'])
        self.assertEqual(8, response.json['user_profiles'][3]['id'])

    def test_get_user_profiles_status_disabled(self):

        response = self.client.get(
            '/user_profiles?status=2&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("user_profiles", response.json)

        self.assertEqual(5, response.json['user_profiles'][0]['id'])
    
    def test_get_user_profiles_status_archived(self):

        response = self.client.get(
            '/user_profiles?status=3&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("user_profiles", response.json)

        self.assertEqual(4, response.json['user_profiles'][0]['id'])
    
    def test_get_user_profiles_status_deleted(self):

        response = self.client.get(
            '/user_profiles?status=4&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("user_profiles", response.json)

        self.assertEqual(7, response.json['user_profiles'][0]['id'])
    
    def test_get_user_profiles_status_pending(self):

        response = self.client.get(
            '/user_profiles?status=5&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("user_profiles", response.json)

        self.assertEqual(6, response.json['user_profiles'][0]['id'])

    def test_get_user_profiles_no_app_key(self):

        response = self.client.get(
            '/user_profiles',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_get_user_profiles_bad_app_key(self):

        response = self.client.get(
            '/user_profiles?app_key=BAD_APP_KEY',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_get_user_profiles_unauthorized(self):

        response = self.client.get('/user_profiles?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_get_user_profiles_no_permission(self):

        response = self.client.get(
            '/user_profiles?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
    
    def test_get_user_profile_1(self):

        response = self.client.get(
            '/user_profile/1?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.json['user_profile']['id'])
        self.assertEqual(1, response.json['user_profile']['user_id'])
        self.assertEqual("Fiona", response.json['user_profile']['first_name'])
        self.assertEqual("Farnham", response.json['user_profile']['last_name'])
        self.assertEqual("2018-12-01T00:00:00+0000", response.json['user_profile']['joined_at'])
        self.assertEqual(1, response.json['user_profile']['status'])
        self.assertEqual("2018-12-01T00:00:00+0000", response.json['user_profile']['status_changed_at'])
        self.assertIn("created_at", response.json['user_profile'])
        self.assertIn("updated_at", response.json['user_profile'])
    
    def test_get_user_profile_250(self):

        response = self.client.get(
            '/user_profile/250?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(404, response.status_code)
        self.assertEqual("Not found", response.json['error'])
    
    def test_get_user_profile_no_app_key(self):

        response = self.client.get(
            '/user_profile/1',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_get_user_profile_bad_app_key(self):

        response = self.client.get(
            '/user_profile/1?app_key=BAD_APP_KEY',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_get_user_profile_unauthorized(self):

        response = self.client.get('/user_profile/1?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_get_user_profile_no_permission(self):

        response = self.client.get(
            '/user_profile/1?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
    
    def test_post_user_profiles_error(self):

        response = self.client.post(
            '/user_profiles?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"foo":"bar"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("user_id", response.json['error'])
        self.assertIn("first_name", response.json['error'])
        self.assertIn("last_name", response.json['error'])
        self.assertIn("joined_at", response.json['error'])
        self.assertIn("status", response.json['error'])

    def test_post_user_profiles_bad_user_error(self):

        response = self.client.post(
            '/user_profiles?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"user_id":250,"first_name":"Service","last_name":"Account","joined_at":"2019-02-04T00:00:00+0000","status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("user_id", response.json['error'])
        self.assertEqual(["Invalid value."], response.json['error']['user_id'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("joined_at", response.json['error'])
        self.assertNotIn("status", response.json['error'])

    def test_post_user_profiles_success(self):

        response = self.client.post(
            '/user_profiles?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"user_id":9,"first_name":"Service","last_name":"Account","joined_at":"2019-02-04T00:00:00+0000","status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(201, response.status_code)
        self.assertEqual(9, response.json['user_profile']['id'])
        self.assertEqual(9, response.json['user_profile']['user_id'])
        self.assertEqual("Service", response.json['user_profile']['first_name'])
        self.assertEqual("Account", response.json['user_profile']['last_name'])
        self.assertEqual("2019-02-04T00:00:00+0000", response.json['user_profile']['joined_at'])
        self.assertEqual(1, response.json['user_profile']['status'])
        self.assertIn("status_changed_at", response.json['user_profile'])
        self.assertIn("created_at", response.json['user_profile'])
        self.assertIn("updated_at", response.json['user_profile'])
    
    def test_post_user_profiles_whitespace_success(self):

        response = self.client.post(
            '/user_profiles?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"user_id":9,"first_name":"Service ","last_name":"  Account","joined_at":"2019-02-04T00:00:00+0000","status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(201, response.status_code)
        self.assertEqual(9, response.json['user_profile']['id'])
        self.assertEqual(9, response.json['user_profile']['user_id'])
        self.assertEqual("Service", response.json['user_profile']['first_name'])
        self.assertEqual("Account", response.json['user_profile']['last_name'])
        self.assertEqual("2019-02-04T00:00:00+0000", response.json['user_profile']['joined_at'])
        self.assertEqual(1, response.json['user_profile']['status'])
        self.assertIn("status_changed_at", response.json['user_profile'])
        self.assertIn("created_at", response.json['user_profile'])
        self.assertIn("updated_at", response.json['user_profile'])

    def test_post_user_profiles_no_app_key(self):

        response = self.client.post(
            '/user_profiles',
            data='{"user_id":9,"first_name":"Service","last_name":"Account","joined_at":"2019-02-04T00:00:00+0000","status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_post_user_profiles_bad_app_key(self):

        response = self.client.post(
            '/user_profiles?app_key=BAD_APP_KEY',
            data='{"user_id":9,"first_name":"Service","last_name":"Account","joined_at":"2019-02-04T00:00:00+0000","status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_post_user_profiles_unauthorized(self):

        response = self.client.post(
            '/user_profiles?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"user_id":9,"first_name":"Service","last_name":"Account","joined_at":"2019-02-04T00:00:00+0000","status":1}',
            headers={
                "Content-Type": "application/json"})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_post_user_profiles_no_permission(self):

        response = self.client.post(
            '/user_profiles?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"user_id":9,"first_name":"Service","last_name":"Account","joined_at":"2019-02-04T00:00:00+0000","status":1}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
    
    def test_put_user_profile_error(self):

        response = self.client.put(
            '/user_profile/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"foo":"bar"}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("user_id", response.json['error'])
        self.assertIn("first_name", response.json['error'])
        self.assertIn("last_name", response.json['error'])
        self.assertIn("joined_at", response.json['error'])
        self.assertIn("status", response.json['error'])
        self.assertNotIn("region_id", response.json['error'])

    def test_put_user_profile_invalid_user_id(self):

        response = self.client.put(
            '/user_profile/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"user_id":250,"first_name":"LynneA","last_name":"HarfordA","joined_at":"2019-01-15T00:00:00+0000","status":2}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)
        self.assertIn("user_id", response.json['error'])
        self.assertEqual(["Invalid value."], response.json['error']['user_id'])
        self.assertNotIn("first_name", response.json['error'])
        self.assertNotIn("last_name", response.json['error'])
        self.assertNotIn("joined_at", response.json['error'])
        self.assertNotIn("status", response.json['error'])

    def test_put_user_profile_empty(self):

        response = self.client.put(
            '/user_profile/250?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"user_id":9,"first_name":"LynneA","last_name":"HarfordA","joined_at":"2019-01-15T00:00:00+0000","status":2}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(404, response.status_code)
        self.assertEqual("Not found", response.json['error'])

    def test_put_user_profile_2(self):

        response = self.client.put(
            '/user_profile/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"user_id":9,"first_name":"LynneA","last_name":"HarfordA","joined_at":"2019-01-15T00:00:00+0000","status":2}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, response.json['user_profile']['id'])
        self.assertEqual(9, response.json['user_profile']['user_id'])
        self.assertEqual("LynneA", response.json['user_profile']['first_name'])
        self.assertEqual("HarfordA", response.json['user_profile']['last_name'])
        self.assertEqual("2019-01-15T00:00:00+0000", response.json['user_profile']['joined_at'])
        self.assertEqual(2, response.json['user_profile']['status'])
        self.assertIn("status_changed_at", response.json['user_profile'])
        self.assertIn("created_at", response.json['user_profile'])
        self.assertIn("updated_at", response.json['user_profile'])

    def test_put_user_profile_whitespace_2(self):

        response = self.client.put(
            '/user_profile/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"user_id":9,"first_name":"LynneA ","last_name":"  HarfordA","joined_at":"2019-01-15T00:00:00+0000","status":2}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, response.json['user_profile']['id'])
        self.assertEqual(9, response.json['user_profile']['user_id'])
        self.assertEqual("LynneA", response.json['user_profile']['first_name'])
        self.assertEqual("HarfordA", response.json['user_profile']['last_name'])
        self.assertEqual("2019-01-15T00:00:00+0000", response.json['user_profile']['joined_at'])
        self.assertEqual(2, response.json['user_profile']['status'])
        self.assertIn("status_changed_at", response.json['user_profile'])
        self.assertIn("created_at", response.json['user_profile'])
        self.assertIn("updated_at", response.json['user_profile'])

    def test_put_user_profile_no_app_key(self):

        response = self.client.put(
            '/user_profile/2',
            data='{"user_id":9,"first_name":"LynneA","last_name":"HarfordA","joined_at":"2019-01-15T00:00:00+0000","status":2}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_put_user_profile_bad_app_key(self):

        response = self.client.put(
            '/user_profile/2?app_key=BAD_APP_KEY',
            data='{"user_id":9,"first_name":"LynneA","last_name":"HarfordA","joined_at":"2019-01-15T00:00:00+0000","status":2}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])

    def test_put_user_profile_unauthorized(self):

        response = self.client.put(
            '/user_profile/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"user_id":9,"first_name":"LynneA","last_name":"HarfordA","joined_at":"2019-01-15T00:00:00+0000","status":2}',
            headers={
                "Content-Type": "application/json"})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_put_user_profile_no_permission(self):

        response = self.client.put(
            '/user_profile/2?app_key=' + AppKeyData.id1_appkey1.key,
            data='{"user_id":9,"first_name":"LynneA","last_name":"HarfordA","joined_at":"2019-01-15T00:00:00+0000","status":2}',
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Basic '
                    + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])

    def test_delete_user_profile_empty(self):

        response = self.client.delete(
            '/user_profile/250?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(404, response.status_code)
        self.assertEqual("Not found", response.json['error'])
    
    def test_delete_user_profile_7(self):

        response = self.client.delete(
            '/user_profile/7?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(204, response.status_code)
        self.assertEqual(None, response.json)
    
    def test_delete_user_profile_no_app_key(self):

        response = self.client.delete(
            '/user_profile/7',
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_delete_user_profile_bad_app_key(self):

        response = self.client.delete(
            '/user_profile/7?app_key=BAD_APP_KEY',
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_delete_user_profile_unauthorized(self):

        response = self.client.delete('/user_profile/7?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_delete_user_profile_no_permission(self):

        response = self.client.delete(
            '/user_profile/7?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic '
                + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
