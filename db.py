from typing import Tuple
import pymysql
import bcrypt
import os
from email.mime.text import MIMEText
import uuid

from smtp import send_email

email_vefify_title = os.environ.get('email_vefify_title')
server_url = os.environ.get('server_url')

db_host = os.environ.get('db_host')
db_user = os.environ.get('db_user')
db_password = os.environ.get('db_password')
db_db = os.environ.get('db_db_name')
db_charset = 'utf8'

def db():
    return pymysql.connect(
        host = db_host,
        user = db_user,
        password = db_password,
        db = db_db,
        charset = db_charset
    )

def get_user_table(is_temp_user: bool) -> str:
    '''테이블 이름을 가져옵니다

    Args:
        is_temp_user: True면 임시 유저 테이블을 반환합니다.
    '''
    return "temp_users" if is_temp_user else "users"


def is_user_exists(id_or_email: int | str, is_email: bool, is_temp_user: bool) -> bool | None:
    '''id로 사용자가 있는지 확인합니다.

    Args:
        id_or_email: id(int) 또는 email(str)
        is_email: 이메일 여부
        is_temp_user: True면 임시 유저 테이블에서 확인합니다.

    Returns:
        True: 유저 있음
        False: 유저 없음
        None: sql오류
    '''
    table = get_user_table(is_temp_user)
    col = "email" if is_email else "id"
    conn = db()
    cus = conn.cursor()
    if (cus.execute(f"select exists(select 1 from {table} where `{col}`=%s)", 
        (id_or_email)) != 1): return None
    conn.close()
    return cus.fetchone()[0] == 1

def is_verified(id_or_email: int | str, is_email: bool) -> bool | None:
    '''사용자가 이메일 인증이 되었는지 여부를 반환합니다.

    Returns:
        None: 사용자가 등록되지 않았거나 sql 오류
        False: 인증되지 않음.
        True: 인증됨
    '''
    col = "email" if is_email else "id"
    conn = db()
    cus = conn.cursor()
    # 으악 더~러워
    if (cus.execute(f"select exists(select 1 from `{get_user_table(True)}` where `{col}`=%s)", 
        (id_or_email)) != 1): return None

    if (cus.fetchone()[0] == 1): return False

    if (cus.execute(f"select exists(select 1 from `{get_user_table(False)}` where `{col}`=%s)", 
        (id_or_email)) != 1): return None

    conn.close()
    return cus.fetchone()[0] == 1

def create_user(name: str, email: str, password: str, is_temp_user: bool) -> Tuple[int, str or None] or None:
    '''사용자를 만듭니다.

    Args:
        password: 평문 비밀번호
        is_temp_user: True면 임시 유저 테이블에서 확인합니다.

    Returns:
        None: sql오류
        Tuple: (사용자 id, 인증코드?)
    '''
    password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return create_user_binary(name, email, password, is_temp_user)

def create_user_binary(name: str, email: str, password: bytes, is_temp_user: bool) -> Tuple[int, str or None] or None:
    '''사용자를 만듭니다.

    Args:
        password: 암호문 비밀번호
        is_temp_user: True면 임시 유저 테이블에서 확인합니다.

    Returns:
        None: sql오류
        Tuple: (사용자 id, 인증코드(temp_user 에서만))
    '''
    table = get_user_table(is_temp_user)
    verify_code = uuid.uuid1().hex if is_temp_user else None
    sql = ", `verify_code`) values (%s, %s, %s, %s)" if is_temp_user else ") values (%s, %s, %s)"
    sql_data = (name, email, password, verify_code) if is_temp_user else (name, email, password)

    conn = db()
    cus = conn.cursor()
    if (cus.execute(f"insert into `{table}` (`name`, `email`, `password`{sql}", sql_data) != 1):
        return None
    conn.commit()

    cus = conn.cursor()
    cus.execute(f"select `id` from `{table}` where email=%s", (email))
    conn.close()
    return (cus.fetchone()[0], verify_code)

def delete_user(id: int, is_temp_user: bool) -> bool:
    '''사용자 계정을 제거합니다.

    Returns:
        True: 제거됨
        False: 제거 실패
    '''
    table = get_user_table(is_temp_user)
    conn = db()
    cus = conn.cursor()
    if (cus.execute(f"delete from `{table}` where `id`=%s",
        (id)) != 1): return False
    conn.commit()
    conn.close()
    return True


def get_user(id: int, is_temp_user: bool):
    '''사용자 튜플을 가져옵니다.
    '''
    table = get_user_table(is_temp_user)
    conn = db()
    cus = conn.cursor()
    if (cus.execute(f"select * from {table} where `id`=%s",
        (id)) != 1): return None
    res = cus.fetchone()
    conn.close()
    return res


def refresh_verify_code(id: int) -> str | None:
    '''임시 유저의 인증코드를 새로 만들고 반환합니다.
    '''
    vid = uuid.uuid1().hex
    conn = db()
    cus = conn.cursor()
    if (cus.execute(f"update `temp_users` set `verify_code`=%s where `id`=%s",
        (vid, id)) != 1):
        return None
    conn.commit()
    conn.close()
    return vid


def check_verify_code(id: int, verify_code: str) -> bool | None:
    '''사용자의 인증코드가 일치한지 확인합니다.
    '''
    conn = db()
    cus = conn.cursor()
    if(cus.execute("select exists(select 1 from `temp_users` where `id`=%s and `verify_code`=%s)",
        (id, verify_code)) != 1): return None
    conn.close()
    return cus.fetchone()[0] == 1


def send_verify_email(id: int, email: str) -> bool | None:
    '''인증코드를 생성 및 발신합니다.

    Returns:
        None: sql 오류
        True: 발송됨
        False: 발송 실패
    '''
    vef_id = refresh_verify_code(id)
    if (vef_id == None): return None
    content = create_email_content(vef_id)
    return send_email(content, email)


def transform_verified_user(id: int) -> int | None:
    '''임시 유저를 인증된 유저로 상태를 전환합니다.

    Returns:
        None: sql 오류
        int: 사용자 id
    '''
    user_data = get_user(id, True)
    if (user_data == None or not delete_user(id, True)): return None

    email = user_data[1]
    name = user_data[2]
    password = user_data[3]

    id = create_user_binary(name, email, password, False)
    if (id == None): return None
    return id[0]


def create_email_content(vefId: str) -> MIMEText:
    msg = MIMEText(f"인증 ㄱ {server_url}/{vefId}")
    msg['Subject'] = "회원가입 인증"
    return msg

