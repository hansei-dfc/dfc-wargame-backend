import hashlib
import os
from db import db

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
    password = hashlib.sha256((password + os.environ.get('pass_salt')).encode()).hexdigest()
    conn = db()
    cus = conn.cursor()
    if (cus.execute(f"insert into `users` (`name`, `email`, `password`) values (%s, %s, %s)",
        (name, email, password)) != 1): return None
    conn.commit()

    cus = conn.cursor()
    cus.execute(f"select `id` from `users` where email=%s and password=%s",
        (email, password))
    conn.close()
    return cus.fetchone()[0]
