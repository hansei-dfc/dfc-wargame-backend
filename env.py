from datetime import timedelta
import os

#email verification
email_vefify_title = os.environ.get('email_vefify_title')

# url
server_url = os.environ.get('server_url')
default_email_verify_redirect_url = os.environ.get('default_email_verify_redirect_url')

# db
db_host = os.environ.get('db_host')
db_port = int(os.environ.get('db_port'))
db_user = os.environ.get('db_user')
db_password = os.environ.get('db_password')
db_db = os.environ.get('db_db_name')
db_charset = os.environ.get('db_charset')

# smtp
smtp_port = os.environ.get('smtp_port')
smtp_server = os.environ.get('smtp_server')
smtp_user = os.environ.get('smtp_user')
smtp_pass = os.environ.get('smtp_pass')

#jwt
jwt_secret = os.environ.get('jwt_secret')
jwt_exp_period = timedelta(seconds=int(os.environ.get('jwt_exp_period')))