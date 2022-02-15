
import uuid
from db import db

def db_create_verify(userId):
    vid = uuid.uuid1();
    conn = db()
    conn.cursor().execute(f"insert into `email_verify` (`userId`, `verifyCode`) values ({userId}, '{vid.hex}')")
    conn.close()
    return vid

def check_verify_code(verifyCode):
    conn = db()
    exists = conn.cursor().execute(f"select exists(select 1 from `email_verify` where `verifyCode`='{verifyCode}')")
    conn.close()
    return exists