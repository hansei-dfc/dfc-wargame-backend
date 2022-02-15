import pymysql
import bcrypt
import os
from email.mime.text import MIMEText
from math import fabs
from multiprocessing import context
import uuid
from smtp import send_email

email_vefify_title = os.environ.get('email_vefify_title')
server_url = os.environ.get('server_url')


def db():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='abcdefu',
        db='war-game',
        charset='utf8'
    )


def is_user_exists(userId):
    conn = db()
    cus = conn.cursor()
    cus.execute(f"select exists(select 1 from `users` where `id`='{userId}')")
    conn.close()
    return cus.fetchone()[0] == 1


def is_user_exists_email(email):
    conn = db()
    cus = conn.cursor()
    cus.execute(f"select exists(select 1 from `users` where `email`=%s)", email)
    conn.close()
    return cus.fetchone()[0] == 1


def create_user(name, email, password):
    password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    conn = db()
    cus = conn.cursor()
    if (cus.execute(f"insert into `users` (`name`, `email`, `password`) values (%s, %s, %s)",
                    (name, email, password)) != 1):
        return None
    conn.commit()

    cus = conn.cursor()
    cus.execute(f"select `id` from `users` where email=%s and password=%s",
                (email, password))
    conn.close()
    return cus.fetchone()[0]


def db_create_verify(userId):
    vid = uuid.uuid1()
    conn = db()
    cus = conn.cursor()
    if (cus.execute(f"insert into `email_verify` (`userId`, `verifyCode`) values ({userId}, '{vid.hex}')") != 1):
        return None
    conn.commit()
    conn.close()
    return vid


def check_verify_code(verifyCode):
    conn = db()
    cus = conn.cursor()
    cus.execute(
        f"select exists(select 1 from `email_verify` where `verifyCode`='{verifyCode}')")
    conn.close()
    return cus.fetchone()[0] == 1


def is_verified(userId):
    conn = db()
    cus = conn.cursor()
    cus.execute(f"select `emailVerify` from `users` where `id`={userId}")
    conn.close()
    return cus.fetchone()[0] == 1


def send_verify_email(userId, email):
    vef_id = db_create_verify(userId)
    if (vef_id == None):
        return False
    content = create_email_content(vef_id)
    if (content == None):
        return False
    return send_email(content, email)


def create_email_content(vefId):
    msg = MIMEText(f"인증 ㄱ {server_url}/{vefId}")
    msg['Subject'] = "회원가입 인증"
    return msg
