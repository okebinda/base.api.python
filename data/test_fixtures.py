import datetime
from fixture import DataSet

from app.models.Administrator import Administrator
from app.models.User import User
from app.models.UserProfile import UserProfile
from app.models.TermsOfService import TermsOfService
from app.models.Country import Country
from app.models.Region import Region
from app.models.AppKey import AppKey
from app.models.PasswordReset import PasswordReset
from app.models.Notification import Notification
from app.models.Login import Login


class CountryData(DataSet):
    class id1_usa:
        name = "United States"
        code_2 = "US"
        code_3 = "USA"
        status = Country.STATUS_ENABLED
        status_changed_at = datetime.date(2018, 1, 1)
    class id2_mexico:
        name = "Mexico"
        code_2 = "MX"
        code_3 = "MEX"
        status = Country.STATUS_ENABLED
        status_changed_at = datetime.date(2018, 1, 1)
    class id3_canada:
        name = "Canada"
        code_2 = "CA"
        code_3 = "CAN"
        status = Country.STATUS_ENABLED
        status_changed_at = datetime.date(2018, 1, 1)
    class id4_france:
        name = "France"
        code_2 = "FR"
        code_3 = "FRA"
        status = Country.STATUS_DISABLED
        status_changed_at = datetime.date(2018, 1, 2)
    class id5_spain:
        name = "Spain"
        code_2 = "ES"
        code_3 = "ESP"
        status = Country.STATUS_ARCHIVED
        status_changed_at = datetime.date(2018, 1, 3)
    class id6_united_kingdom:
        name = "United Kingdom"
        code_2 = "GB"
        code_3 = "GBR"
        status = Country.STATUS_DELETED
        status_changed_at = datetime.date(2018, 1, 4)
    class id7_germany:
        name = "Germany"
        code_2 = "DE"
        code_3 = "DEU"
        status = Country.STATUS_PENDING
        status_changed_at = datetime.date(2018, 1, 5)


class RegionData(DataSet):
    class id1_california:
        name = "California"
        code_2 = "CA"
        country = CountryData.id1_usa
        status = Region.STATUS_ENABLED
        status_changed_at = datetime.date(2018, 1, 1)
    class id2_oregon:
        name = "Oregon"
        code_2 = "OR"
        country = CountryData.id1_usa
        status = Region.STATUS_ENABLED
        status_changed_at = datetime.date(2018, 1, 1)
    class id3_washington:
        name = "Washington"
        code_2 = "WA"
        country = CountryData.id1_usa
        status = Region.STATUS_ENABLED
        status_changed_at = datetime.date(2018, 1, 1)
    class id4_alabama:
        name = "Alabama"
        code_2 = "AL"
        country = CountryData.id1_usa
        status = Region.STATUS_DISABLED
        status_changed_at = datetime.date(2018, 1, 2)
    class id5_alaska:
        name = "Alaska"
        code_2 = "AK"
        country = CountryData.id1_usa
        status = Region.STATUS_ARCHIVED
        status_changed_at = datetime.date(2018, 1, 3)
    class id6_arizona:
        name = "Arizona"
        code_2 = "AZ"
        country = CountryData.id1_usa
        status = Region.STATUS_DELETED
        status_changed_at = datetime.date(2018, 1, 4)
    class id7_arkansas:
        name = "Arkansas"
        code_2 = "AR"
        country = CountryData.id1_usa
        status = Region.STATUS_PENDING
        status_changed_at = datetime.date(2018, 1, 5)
    class id8_british_columbia:
        name = "British Columbia"
        code_2 = "BC"
        country = CountryData.id3_canada
        status = Region.STATUS_ENABLED
        status_changed_at = datetime.date(2018, 1, 6)


class AppKeyData(DataSet):
    class id1_appkey1:
        application = "Application 1"
        key = "7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW"
        status = AppKey.STATUS_ENABLED
        status_changed_at = datetime.date(2018, 1, 1)
    class id2_appkey2:
        application = "Application 2"
        key = "cvBtQGgL9gNnSZk4DmKnva4QMcpTV7Mx"
        status = AppKey.STATUS_ENABLED
        status_changed_at = datetime.date(2018, 1, 5)
    class id3_appkey3:
        application = "Application 3"
        key = "9CR45hFpTahbqDvmZFJdENAKz5VPqLG3"
        status = AppKey.STATUS_DISABLED
        status_changed_at = datetime.date(2018, 1, 10)
    class id4_appkey4:
        application = "Application 4"
        key = "Zp4DFyUH6nYQb5acw2Y23sga5CfQhRgZ"
        status = AppKey.STATUS_ARCHIVED
        status_changed_at = datetime.date(2018, 1, 15)
    class id5_appkey5:
        application = "Application 5"
        key = "TRrD8GjTtHnGvJZZektcgg6DMVeBkhHB"
        status = AppKey.STATUS_DELETED
        status_changed_at = datetime.date(2018, 1, 20)
    class id6_appkey6:
        application = "Application 6"
        key = "kP4k7vun5RwTBbESwHrCuDdFUtRchbVf"
        status = AppKey.STATUS_PENDING
        status_changed_at = datetime.date(2018, 1, 25)


class RoleData(DataSet):
    class id1_user:
        name = "USER"
        is_admin_role = False
        priority = 100
        login_lockout_policy = False
        login_max_attempts = 10
        login_timeframe = 600
        login_ban_time = 1800
        login_ban_by_ip = True
        password_policy = False
        password_reuse_history = 10
        password_reset_days = 365
    class id2_admin:
        name = "SUPER_ADMIN"
        is_admin_role = True
        priority = 10
        login_lockout_policy = True
        login_max_attempts = 5
        login_timeframe = 300
        login_ban_time = 1800
        login_ban_by_ip = True
        password_policy = True
        password_reuse_history = 24
        password_reset_days = 90
    class id3_service:
        name = "SERVICE"
        is_admin_role = False
        priority = 50
        login_lockout_policy = True
        login_max_attempts = 5
        login_timeframe = 300
        login_ban_time = 1800
        login_ban_by_ip = True
        password_policy = True
        password_reuse_history = 24
        password_reset_days = 365


class AdministratorData(DataSet):
    class id1_admin1:
        username = "admin1"
        email = "admin1@test.com"
        password = "admin1pass"
        first_name = "Tommy"
        last_name = "Lund"
        joined_at = datetime.date(2018, 11, 1)
        roles = [RoleData.id2_admin]
        status = Administrator.STATUS_ENABLED
        status_changed_at = datetime.date(2018, 11, 1)
    class id2_admin2:
        username = "admin2"
        email = "admin2@test.com"
        password = "admin2pass"
        first_name = "Selma"
        last_name = "Keyes"
        joined_at = datetime.date(2018, 11, 5)
        roles = [RoleData.id2_admin]
        status = Administrator.STATUS_ENABLED
        status_changed_at = datetime.date(2018, 11, 5)
    class id3_admin3:
        username = "admin3"
        email = "admin3@test.com"
        password = "admin3pass"
        first_name = "Victor"
        last_name = "Landon"
        joined_at = datetime.date(2018, 11, 15)
        roles = []
        status = Administrator.STATUS_ENABLED
        status_changed_at = datetime.date(2018, 11, 15)
    class id4_admin4:
        username = "admin4"
        email = "admin4@test.com"
        password = "admin4pass"
        first_name = "Tamela"
        last_name = "Coburn"
        joined_at = datetime.date(2018, 11, 20)
        roles = [RoleData.id2_admin]
        status = Administrator.STATUS_DISABLED
        status_changed_at = datetime.date(2018, 11, 20)
    class id5_admin5:
        username = "admin5"
        email = "admin5@test.com"
        password = "admin5pass"
        first_name = "Leigh"
        last_name = "Beck"
        joined_at = datetime.date(2018, 11, 25)
        roles = [RoleData.id2_admin]
        status = Administrator.STATUS_ARCHIVED
        status_changed_at = datetime.date(2018, 11, 25)
    class id6_admin6:
        username = "admin6"
        email = "admin6@test.com"
        password = "admin6pass"
        first_name = "Bob"
        last_name = "Waters"
        joined_at = datetime.date(2018, 11, 30)
        roles = [RoleData.id2_admin]
        status = Administrator.STATUS_DELETED
        status_changed_at = datetime.date(2018, 11, 30)
    class id7_admin7:
        username = "admin7"
        email = "admin7@test.com"
        password = "admin7pass"
        first_name = "Nigel"
        last_name = "Sams"
        joined_at = datetime.date(2018, 11, 10)
        roles = [RoleData.id2_admin]
        status = Administrator.STATUS_PENDING
        status_changed_at = datetime.date(2018, 11, 10)


class TermsOfServiceData(DataSet):
    class id1_tos1:
        text = "This is TOS 1"
        version = "1.0"
        publish_date = datetime.date(2018, 6, 15)
        status = TermsOfService.STATUS_ENABLED
        status_changed_at = datetime.date(2018, 6, 15)
    class id2_tos2:
        text = "This is TOS 2"
        version = "1.1"
        publish_date = datetime.date(2019, 1, 1)
        status = TermsOfService.STATUS_ENABLED
        status_changed_at = datetime.date(2019, 1, 1)
    class id3_tos3:
        text = "This is TOS 3"
        version = "1.2"
        publish_date = datetime.date(2019, 1, 15)
        status = TermsOfService.STATUS_ARCHIVED
        status_changed_at = datetime.date(2019, 1, 15)
    class id4_tos4:
        text = "This is TOS 4"
        version = "1.3"
        publish_date = datetime.date(2019, 1, 20)
        status = TermsOfService.STATUS_DISABLED
        status_changed_at = datetime.date(2019, 1, 20)
    class id5_tos5:
        text = "This is TOS 5"
        version = "1.4"
        publish_date = datetime.date(2019, 1, 25)
        status = TermsOfService.STATUS_DELETED
        status_changed_at = datetime.date(2019, 1, 25)
    class id6_tos6:
        text = "This is TOS 6"
        version = "2.0"
        publish_date = datetime.date(2019, 1, 30)
        status = TermsOfService.STATUS_PENDING
        status_changed_at = datetime.date(2019, 1, 30)


class UserData(DataSet):
    class id1_user1:
        username = "user1"
        email = "user1@test.com"
        password = "user1pass"
        is_verified = False
        roles = []
        status = User.STATUS_ENABLED
        status_changed_at = datetime.date(2018, 12, 1)
    class id2_user2:
        username = "user2"
        email = "user2@test.com"
        password = "user2pass"
        is_verified = True
        roles = [RoleData.id1_user]
        status = User.STATUS_ENABLED
        status_changed_at = datetime.date(2018, 12, 10)
    class id3_user3:
        username = "user3"
        email = "user3@test.com"
        password = "user3pass"
        is_verified = True
        roles = [RoleData.id1_user]
        status = User.STATUS_ENABLED
        status_changed_at = datetime.date(2018, 12, 15)
    class id4_user4:
        username = "user4"
        email = "user4@test.com"
        password = "user4pass"
        is_verified = True
        roles = [RoleData.id1_user]
        status = User.STATUS_ARCHIVED
        status_changed_at = datetime.date(2018, 12, 20)
    class id5_user5:
        username = "user5"
        email = "user5@test.com"
        password = "user5pass"
        is_verified = False
        roles = [RoleData.id1_user]
        status = User.STATUS_DISABLED
        status_changed_at = datetime.date(2018, 12, 25)
    class id6_user6:
        username = "user6"
        email = "user6@test.com"
        password = "user6pass"
        is_verified = True
        roles = [RoleData.id1_user]
        status = User.STATUS_PENDING
        status_changed_at = datetime.date(2018, 12, 30)
    class id7_user7:
        username = "user7"
        email = "user7@test.com"
        password = "user7pass"
        is_verified = True
        roles = [RoleData.id1_user]
        status = User.STATUS_DELETED
        status_changed_at = datetime.date(2019, 1, 5)
    class id8_user8:
        username = "user8"
        email = "user8@test.com"
        password = "user8pass"
        is_verified = False
        roles = [RoleData.id1_user]
        status = User.STATUS_ENABLED
        status_changed_at = datetime.date(2019, 1, 10)
    class id9_service1:
        username = "service1"
        email = "service1@test.com"
        password = "service1pass"
        is_verified = False
        roles = [RoleData.id3_service]
        status = User.STATUS_ENABLED
        status_changed_at = datetime.date(2019, 2, 1)


class UserProfileData(DataSet):
    class id1_userprofile1:
        user = UserData.id1_user1
        first_name = "Fiona"
        last_name = "Farnham"
        joined_at = datetime.date(2018, 12, 1)
        status = UserProfile.STATUS_ENABLED
        status_changed_at = datetime.date(2018, 12, 1)
    class id2_userprofile2:
        user = UserData.id2_user2
        first_name = "Lynne"
        last_name = "Harford"
        joined_at = datetime.date(2018, 12, 10)
        status = UserProfile.STATUS_ENABLED
        status_changed_at = datetime.date(2018, 12, 10)
    class id3_userprofile3:
        user = UserData.id3_user3
        first_name = "Duane"
        last_name = "Hargrave"
        joined_at = datetime.date(2018, 12, 15)
        status = UserProfile.STATUS_ENABLED
        status_changed_at = datetime.date(2018, 12, 15)
    class id4_userprofile4:
        user = UserData.id4_user4
        first_name = "Leta"
        last_name = "Hillam"
        joined_at = datetime.date(2018, 12, 15)
        status = UserProfile.STATUS_ARCHIVED
        status_changed_at = datetime.date(2018, 12, 20)
    class id5_userprofile5:
        user = UserData.id5_user5
        first_name = "Elroy"
        last_name = "Hunnicutt"
        joined_at = datetime.date(2018, 12, 20)
        status = UserProfile.STATUS_DISABLED
        status_changed_at = datetime.date(2018, 12, 25)
    class id6_userprofile6:
        user = UserData.id6_user6
        first_name = "Alease"
        last_name = "Richards"
        joined_at = datetime.date(2018, 12, 29)
        status = UserProfile.STATUS_PENDING
        status_changed_at = datetime.date(2018, 12, 30)
    class id7_userprofile7:
        user = UserData.id7_user7
        first_name = "Thaddeus"
        last_name = "Towner"
        joined_at = datetime.date(2019, 1, 2)
        status = UserProfile.STATUS_DELETED
        status_changed_at = datetime.date(2019, 1, 5)
    class id8_userprofile8:
        user = UserData.id8_user8
        first_name = "Luke"
        last_name = "Tennyson"
        joined_at = datetime.date(2019, 1, 10)
        status = UserProfile.STATUS_ENABLED
        status_changed_at = datetime.date(2019, 1, 10)


class UserTermsOfServiceData(DataSet):
    class id1_u1_tos1:
        user = UserData.id1_user1
        terms_of_service = TermsOfServiceData.id1_tos1
        accept_date = datetime.date(2018, 6, 16)
        ip_address = '1.1.1.1'
    class id2_u1_tos2:
        user = UserData.id1_user1
        terms_of_service = TermsOfServiceData.id2_tos2
        accept_date = datetime.date(2019, 1, 1)
        ip_address = '1.1.1.1'
    class id3_u2_tos1:
        user = UserData.id2_user2
        terms_of_service = TermsOfServiceData.id1_tos1
        accept_date = datetime.date(2018, 12, 10)
        ip_address = '1.1.1.2'
    class id4_u2_tos2:
        user = UserData.id2_user2
        terms_of_service = TermsOfServiceData.id2_tos2
        accept_date = datetime.date(2019, 1, 6)
        ip_address = '1.1.1.2'
    class id5_u3_tos2:
        user = UserData.id3_user3
        terms_of_service = TermsOfServiceData.id2_tos2
        accept_date = datetime.date(2019, 1, 2)
        ip_address = '1.1.1.3'


class LoginData(DataSet):
    class id1_u1_login1:
        user_id = 1
        username = AdministratorData.id1_admin1.username
        ip_address = '1.1.1.1'
        api = Login.API_ADMIN
        success = True
        attempt_date = datetime.datetime(2018, 12, 1, 8, 32, 55)
    class id2_u1_login2:
        user_id = 1
        username = AdministratorData.id1_admin1.username
        ip_address = '1.1.1.1'
        api = Login.API_ADMIN
        success = False
        attempt_date = datetime.datetime(2018, 12, 2, 12, 2, 21)
    class id3_u1_login3:
        user_id = 1
        username = AdministratorData.id1_admin1.username
        ip_address = '1.1.1.1'
        api = Login.API_ADMIN
        success = True
        attempt_date = datetime.datetime(2018, 12, 2, 12, 3, 9)
    class id4_u2_login1:
        user_id = 2
        username = UserData.id2_user2.username
        ip_address = '1.1.1.2'
        api = Login.API_PUBLIC
        success = True
        attempt_date = datetime.datetime(2018, 12, 10, 20, 47, 30)
    class id5_u2_login2:
        user_id = 2
        username = UserData.id2_user2.username
        ip_address = '9.9.9.9'
        api = Login.API_PUBLIC
        success = False
        attempt_date = datetime.datetime(2018, 12, 22, 23, 11, 53)
    class id6_u2_login3:
        user_id = 2
        username = UserData.id2_user2.username
        ip_address = '9.9.9.9'
        api = Login.API_PUBLIC
        success = False
        attempt_date = datetime.datetime(2018, 12, 22, 23, 12, 28)
    class id7_u3_login1:
        user_id = 3
        username = UserData.id3_user3.username
        ip_address = '1.1.1.3'
        api = Login.API_PUBLIC
        success = True
        attempt_date = datetime.datetime(2018, 12, 15, 7, 32, 18)
    class id8_u0_login1:
        username = 'root'
        ip_address = '9.9.9.9'
        api = Login.API_PUBLIC
        success = False
        attempt_date = datetime.datetime(2019, 1, 8, 2, 40, 21)


class PasswordResetData(DataSet):
    class id1_password_reset1:
        user = UserData.id1_user1
        code = "HD7SF2"
        is_used = True
        requested_at = datetime.datetime(2019, 1, 10, 7, 13, 49)
        ip_address = '1.1.1.1'
        status = PasswordReset.STATUS_ENABLED
        status_changed_at = datetime.date(2019, 1, 10)
    class id2_password_reset2:
        user = UserData.id2_user2
        code = "M5AF8G"
        is_used = True
        requested_at = datetime.datetime(2019, 1, 12, 14, 2, 51)
        ip_address = '1.1.1.2'
        status = PasswordReset.STATUS_ENABLED
        status_changed_at = datetime.date(2019, 1, 12)
    class id3_password_reset3:
        user = UserData.id1_user1
        code = "QQ94ND"
        is_used = True
        requested_at = datetime.datetime(2019, 1, 15, 20, 46, 15)
        ip_address = '1.1.1.1'
        status = PasswordReset.STATUS_DISABLED
        status_changed_at = datetime.date(2019, 1, 15)
    class id4_password_reset4:
        user = UserData.id2_user2
        code = "2POL3F"
        is_used = True
        requested_at = datetime.datetime(2019, 1, 15, 22, 7, 30)
        ip_address = '1.1.1.2'
        status = PasswordReset.STATUS_ARCHIVED
        status_changed_at = datetime.date(2019, 1, 15)
    class id5_password_reset5:
        user = UserData.id3_user3
        code = "XAY87R"
        is_used = True
        requested_at = datetime.datetime(2019, 1, 20, 3, 37, 10)
        ip_address = '1.1.1.3'
        status = PasswordReset.STATUS_PENDING
        status_changed_at = datetime.date(2019, 1, 20)
    class id6_password_reset6:
        user = UserData.id1_user1
        code = "73GV0K"
        is_used = False
        requested_at = datetime.datetime(2019, 1, 25, 10, 21, 3)
        ip_address = '9.9.9.9'
        status = PasswordReset.STATUS_DELETED
        status_changed_at = datetime.date(2019, 1, 25)
    class id7_password_reset7:
        user = UserData.id2_user2
        code = "AM8A4N"
        is_used = False
        requested_at = datetime.datetime(2019, 1, 28, 9, 38, 58)
        ip_address = '1.2.3.4'
        status = PasswordReset.STATUS_ENABLED
        status_changed_at = datetime.date(2019, 1, 28)
    class id8_password_reset8:
        user = UserData.id2_user2
        code = "PRQ7M2"
        is_used = True
        requested_at = datetime.datetime.now()
        ip_address = '1.2.3.4'
        status = PasswordReset.STATUS_ENABLED
        status_changed_at = datetime.datetime.now()
    class id9_password_reset9:
        user = UserData.id2_user2
        code = "J91NP0"
        is_used = False
        requested_at = datetime.datetime.now()
        ip_address = '1.2.3.4'
        status = PasswordReset.STATUS_ENABLED
        status_changed_at = datetime.datetime.now()


class NotificationData(DataSet):
    class id1_notification1:
        user = UserData.id1_user1
        channel = 1
        template = "template-1"
        service = "Service 1"
        notification_id = "123456"
        accepted = 1
        rejected = 0
        sent_at = datetime.datetime(2019, 2, 1, 10, 45, 0)
        status = Notification.STATUS_ENABLED
        status_changed_at = datetime.date(2019, 2, 1)
    class id2_notification2:
        user = UserData.id2_user2
        channel = 1
        template = "template-1"
        service = "Service 1"
        notification_id = "123457"
        accepted = 1
        rejected = 0
        sent_at = datetime.datetime(2019, 2, 3, 12, 10, 7)
        status = Notification.STATUS_ENABLED
        status_changed_at = datetime.date(2019, 2, 3)
    class id3_notification3:
        user = UserData.id1_user1
        channel = 1
        template = "template-2"
        service = "Service 1"
        notification_id = "123458"
        accepted = 0
        rejected = 1
        sent_at = datetime.datetime(2019, 2, 4, 18, 51, 36)
        status = Notification.STATUS_DISABLED
        status_changed_at = datetime.date(2019, 2, 4)
    class id4_notification4:
        user = UserData.id3_user3
        channel = 1
        template = "template-1"
        service = "Service 1"
        notification_id = "123459"
        accepted = 1
        rejected = 0
        sent_at = datetime.datetime(2019, 2, 6, 21, 29, 15)
        status = Notification.STATUS_ARCHIVED
        status_changed_at = datetime.date(2019, 2, 6)
    class id5_notification5:
        user = UserData.id2_user2
        channel = 1
        template = "template-2"
        service = "Service 2"
        notification_id = "123460"
        accepted = 1
        rejected = 0
        sent_at = datetime.datetime(2019, 2, 6, 22, 0, 40)
        status = Notification.STATUS_DELETED
        status_changed_at = datetime.date(2019, 2, 1)
    class id6_notification6:
        user = UserData.id3_user3
        channel = 1
        template = "template-3"
        service = "Service 2"
        notification_id = "AB123461"
        accepted = 2
        rejected = 1
        sent_at = datetime.datetime(2019, 2, 10, 6, 21, 39)
        status = Notification.STATUS_PENDING
        status_changed_at = datetime.date(2019, 2, 10)
    class id7_notification7:
        user = UserData.id1_user1
        channel = 2
        template = "template-3"
        service = "Service 1"
        notification_id = "123462"
        accepted = 0
        rejected = 1
        sent_at = datetime.datetime(2019, 2, 13, 17, 3, 46)
        status = Notification.STATUS_ENABLED
        status_changed_at = datetime.date(2019, 2, 13)
