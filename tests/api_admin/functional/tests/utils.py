import base64

def get_http_basic_auth_credentials(user):
    credentials = user.username + ':' + user.password
    base64_credentials = base64.b64encode(credentials.encode('ascii')).decode('utf-8')
    return base64_credentials
