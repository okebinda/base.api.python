from tests.BaseTest import BaseTest
from test_fixtures import *
from tests.utils import get_http_basic_auth_credentials
    
class NotificationsTest(BaseTest):

    def test_get_notifications(self):

        response = self.client.get('/notifications?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("notifications", response.json)

        self.assertEqual(1, response.json['notifications'][0]['id'])
        self.assertIn('user', response.json['notifications'][0])
        self.assertEqual(1, response.json['notifications'][0]['user']['id'])
        self.assertTrue(response.json['notifications'][0]['user']['uri'].endswith('/user/1'))
        self.assertEqual("user1", response.json['notifications'][0]['user']['username'])
        self.assertEqual(1, response.json['notifications'][0]['channel'])
        self.assertEqual("template-1", response.json['notifications'][0]['template'])
        self.assertEqual("Service 1", response.json['notifications'][0]['service'])
        self.assertEqual("123456", response.json['notifications'][0]['notification_id'])
        self.assertEqual(1, response.json['notifications'][0]['accepted'])
        self.assertEqual(0, response.json['notifications'][0]['rejected'])
        self.assertEqual("2019-02-01T10:45:00+0000", response.json['notifications'][0]['sent_at'])
        self.assertEqual(1, response.json['notifications'][0]['status'])
        self.assertEqual("2019-02-01T00:00:00+0000", response.json['notifications'][0]['status_changed_at'])
        self.assertIn("created_at", response.json['notifications'][0])
        self.assertIn("updated_at", response.json['notifications'][0])

        self.assertEqual(2, response.json['notifications'][1]['id'])
        self.assertIn('user', response.json['notifications'][1])
        self.assertEqual(2, response.json['notifications'][1]['user']['id'])
        self.assertTrue(response.json['notifications'][1]['user']['uri'].endswith('/user/2'))
        self.assertEqual("user2", response.json['notifications'][1]['user']['username'])
        self.assertEqual(1, response.json['notifications'][1]['channel'])
        self.assertEqual("template-1", response.json['notifications'][1]['template'])
        self.assertEqual("Service 1", response.json['notifications'][1]['service'])
        self.assertEqual("123457", response.json['notifications'][1]['notification_id'])
        self.assertEqual(1, response.json['notifications'][1]['accepted'])
        self.assertEqual(0, response.json['notifications'][1]['rejected'])
        self.assertEqual("2019-02-03T12:10:07+0000", response.json['notifications'][1]['sent_at'])
        self.assertEqual(1, response.json['notifications'][1]['status'])
        self.assertEqual("2019-02-03T00:00:00+0000", response.json['notifications'][1]['status_changed_at'])
        self.assertIn("created_at", response.json['notifications'][1])
        self.assertIn("updated_at", response.json['notifications'][1])

        self.assertEqual(3, response.json['notifications'][2]['id'])
        self.assertIn('user', response.json['notifications'][2])
        self.assertEqual(1, response.json['notifications'][2]['user']['id'])
        self.assertTrue(response.json['notifications'][2]['user']['uri'].endswith('/user/1'))
        self.assertEqual("user1", response.json['notifications'][2]['user']['username'])
        self.assertEqual(1, response.json['notifications'][2]['channel'])
        self.assertEqual("template-2", response.json['notifications'][2]['template'])
        self.assertEqual("Service 1", response.json['notifications'][2]['service'])
        self.assertEqual("123458", response.json['notifications'][2]['notification_id'])
        self.assertEqual(0, response.json['notifications'][2]['accepted'])
        self.assertEqual(1, response.json['notifications'][2]['rejected'])
        self.assertEqual("2019-02-04T18:51:36+0000", response.json['notifications'][2]['sent_at'])
        self.assertEqual(2, response.json['notifications'][2]['status'])
        self.assertEqual("2019-02-04T00:00:00+0000", response.json['notifications'][2]['status_changed_at'])
        self.assertIn("created_at", response.json['notifications'][2])
        self.assertIn("updated_at", response.json['notifications'][2])

        self.assertEqual(6, response.json['notifications'][3]['id'])
        self.assertIn('user', response.json['notifications'][3])
        self.assertEqual(3, response.json['notifications'][3]['user']['id'])
        self.assertTrue(response.json['notifications'][3]['user']['uri'].endswith('/user/3'))
        self.assertEqual("user3", response.json['notifications'][3]['user']['username'])
        self.assertEqual(1, response.json['notifications'][3]['channel'])
        self.assertEqual("template-3", response.json['notifications'][3]['template'])
        self.assertEqual("Service 2", response.json['notifications'][3]['service'])
        self.assertEqual("AB123461", response.json['notifications'][3]['notification_id'])
        self.assertEqual(2, response.json['notifications'][3]['accepted'])
        self.assertEqual(1, response.json['notifications'][3]['rejected'])
        self.assertEqual("2019-02-10T06:21:39+0000", response.json['notifications'][3]['sent_at'])
        self.assertEqual(5, response.json['notifications'][3]['status'])
        self.assertEqual("2019-02-10T00:00:00+0000", response.json['notifications'][3]['status_changed_at'])
        self.assertIn("created_at", response.json['notifications'][3])
        self.assertIn("updated_at", response.json['notifications'][3])

        self.assertEqual(7, response.json['notifications'][4]['id'])
        self.assertIn('user', response.json['notifications'][4])
        self.assertEqual(1, response.json['notifications'][4]['user']['id'])
        self.assertTrue(response.json['notifications'][4]['user']['uri'].endswith('/user/1'))
        self.assertEqual("user1", response.json['notifications'][4]['user']['username'])
        self.assertEqual(2, response.json['notifications'][4]['channel'])
        self.assertEqual("template-3", response.json['notifications'][4]['template'])
        self.assertEqual("Service 1", response.json['notifications'][4]['service'])
        self.assertEqual("123462", response.json['notifications'][4]['notification_id'])
        self.assertEqual(0, response.json['notifications'][4]['accepted'])
        self.assertEqual(1, response.json['notifications'][4]['rejected'])
        self.assertEqual("2019-02-13T17:03:46+0000", response.json['notifications'][4]['sent_at'])
        self.assertEqual(1, response.json['notifications'][4]['status'])
        self.assertEqual("2019-02-13T00:00:00+0000", response.json['notifications'][4]['status_changed_at'])
        self.assertIn("created_at", response.json['notifications'][4])
        self.assertIn("updated_at", response.json['notifications'][4])
    
    def test_get_notifications_id_asc(self):

        response = self.client.get('/notifications?order_by=id.asc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("notifications", response.json)

        self.assertEqual(1, response.json['notifications'][0]['id'])
        self.assertEqual(2, response.json['notifications'][1]['id'])
        self.assertEqual(3, response.json['notifications'][2]['id'])
        self.assertEqual(6, response.json['notifications'][3]['id'])
        self.assertEqual(7, response.json['notifications'][4]['id'])

    def test_get_notifications_id_desc(self):

        response = self.client.get('/notifications?order_by=id.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("notifications", response.json)

        self.assertEqual(7, response.json['notifications'][0]['id'])
        self.assertEqual(6, response.json['notifications'][1]['id'])
        self.assertEqual(3, response.json['notifications'][2]['id'])
        self.assertEqual(2, response.json['notifications'][3]['id'])
        self.assertEqual(1, response.json['notifications'][4]['id'])
    
    def test_get_notifications_sent_at_asc(self):

        response = self.client.get('/notifications?order_by=sent_at.asc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("notifications", response.json)

        self.assertEqual(1, response.json['notifications'][0]['id'])
        self.assertEqual(2, response.json['notifications'][1]['id'])
        self.assertEqual(3, response.json['notifications'][2]['id'])
        self.assertEqual(6, response.json['notifications'][3]['id'])
        self.assertEqual(7, response.json['notifications'][4]['id'])

    def test_get_notifications_sent_at_desc(self):

        response = self.client.get('/notifications?order_by=sent_at.desc&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("notifications", response.json)

        self.assertEqual(7, response.json['notifications'][0]['id'])
        self.assertEqual(6, response.json['notifications'][1]['id'])
        self.assertEqual(3, response.json['notifications'][2]['id'])
        self.assertEqual(2, response.json['notifications'][3]['id'])
        self.assertEqual(1, response.json['notifications'][4]['id'])

    def test_get_notifications_page_2(self):

        response = self.client.get('/notifications/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(204, response.status_code)
        self.assertTrue(None == response.json)

    def test_get_notifications_page_1_limit_2(self):

        response = self.client.get('/notifications/1/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(2, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("notifications", response.json)
        self.assertTrue(response.json['next_uri'].endswith('/notifications/2/2'))

        self.assertEqual(1, response.json['notifications'][0]['id'])
        self.assertEqual(2, response.json['notifications'][1]['id'])
    
    def test_get_notifications_page_2_limit_2(self):

        response = self.client.get('/notifications/2/2?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(2, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(2, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(5, response.json['total'])
        self.assertIn("notifications", response.json)
        self.assertTrue(response.json['previous_uri'].endswith('/notifications/1/2'))
        self.assertTrue(response.json['next_uri'].endswith('/notifications/3/2'))

        self.assertEqual(3, response.json['notifications'][0]['id'])
        self.assertEqual(6, response.json['notifications'][1]['id'])

    def test_get_notifications_user_1(self):

        response = self.client.get('/notifications?user_id=1&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("notifications", response.json)

        self.assertEqual(1, response.json['notifications'][0]['id'])
        self.assertEqual(3, response.json['notifications'][1]['id'])
        self.assertEqual(7, response.json['notifications'][2]['id'])
    
    def test_get_notifications_channel_1(self):

        response = self.client.get('/notifications?channel=1&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(4, response.json['total'])
        self.assertIn("notifications", response.json)

        self.assertEqual(1, response.json['notifications'][0]['id'])
        self.assertEqual(2, response.json['notifications'][1]['id'])
        self.assertEqual(3, response.json['notifications'][2]['id'])
        self.assertEqual(6, response.json['notifications'][3]['id'])
    
    def test_get_notifications_status_enabled(self):

        response = self.client.get('/notifications?status=1&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(3, response.json['total'])
        self.assertIn("notifications", response.json)

        self.assertEqual(1, response.json['notifications'][0]['id'])
        self.assertEqual(2, response.json['notifications'][1]['id'])
        self.assertEqual(7, response.json['notifications'][2]['id'])
    
    def test_get_notifications_status_disabled(self):

        response = self.client.get('/notifications?status=2&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("notifications", response.json)

        self.assertEqual(3, response.json['notifications'][0]['id'])
    
    def test_get_notifications_status_archived(self):

        response = self.client.get('/notifications?status=3&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("notifications", response.json)

        self.assertEqual(4, response.json['notifications'][0]['id'])
    
    def test_get_notifications_status_deleted(self):

        response = self.client.get('/notifications?status=4&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("notifications", response.json)

        self.assertEqual(5, response.json['notifications'][0]['id'])

    def test_get_notifications_status_pending(self):

        response = self.client.get('/notifications?status=5&app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})
        
        self.assertEqual(200, response.status_code)
        self.assertIn("limit", response.json)
        self.assertEqual(10, response.json['limit'])
        self.assertIn("page", response.json)
        self.assertEqual(1, response.json['page'])
        self.assertIn("total", response.json)
        self.assertEqual(1, response.json['total'])
        self.assertIn("notifications", response.json)

        self.assertEqual(6, response.json['notifications'][0]['id'])

    def test_get_notifications_no_app_key(self):

        response = self.client.get('/notifications',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Missing application key", response.json['error'])
    
    def test_get_notifications_bad_app_key(self):

        response = self.client.get('/notifications?app_key=BAD_APP_KEY',
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id1_admin1)})

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad application key", response.json['error'])
    
    def test_get_notifications_unauthorized(self):

        response = self.client.get('/notifications?app_key=' + AppKeyData.id1_appkey1.key)

        self.assertEqual(401, response.status_code)
        self.assertEqual("Bad credentials", response.json['error'])
    
    def test_get_notifications_no_permission(self):

        response = self.client.get('/notifications?app_key=' + AppKeyData.id1_appkey1.key,
            headers={"Authorization": 'Basic ' 
                + get_http_basic_auth_credentials(AdministratorData.id3_admin3)})

        self.assertEqual(403, response.status_code)
        self.assertEqual("Permission denied", response.json['error'])
