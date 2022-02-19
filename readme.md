## .env **needs** to be created

```
smtp_user=
smtp_sender=
smtp_pass=
smtp_server=[ex) smtp.gmail.com]
smtp_port=[ex) 587]

server_url=[backend server_ip or domain]
default_email_verify_redirect_url=[front email verify redirect url]

db_host=[db host]
db_port=3306
db_user=[ex) root]
db_password=
db_db_name=
db_charset=utf8

jwt_secret=[string]
jwt_exp_period=[seconds]
```


## Necessary Python Packages
```
bcrypt
Flask
Flask-Cors
flask-restx
PyJWT
PyMySQL
python-dotenv
```

### installation
```
pip install -r requirements.txt
```