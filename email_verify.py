
from email.mime.text import MIMEText
from math import fabs
from multiprocessing import context
import os
import uuid
from db import db
from smtp import send_email

email_vefify_title = os.environ.get('email_vefify_title')
server_url = os.environ.get('server_url')

def db_create_verify(userId):
    vid = uuid.uuid1();
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
    cus.execute(f"select exists(select 1 from `email_verify` where `verifyCode`='{verifyCode}')")
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
    if (vef_id == None): return False
    content = create_email_content(vef_id)
    if (content == None): return False
    return send_email(content, email)

def create_email_content(vefId):
    msg = MIMEText(f"인증 ㄱ {server_url}/{vefId}")
    msg['Subject'] = email_vefify_title
    return msg
