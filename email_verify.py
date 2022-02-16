
from email.mime.text import MIMEText
from typing import Tuple
from urllib.parse import urlencode, urljoin
from db import refresh_verify_code
from smtp import send_email
import env


def make_verify_data(user_id: int, verify_code: str) -> str:
    '''인증 데이터를 만듭니다.
    '''
    return f"{user_id.to_bytes(8, 'big').hex()}_{verify_code}"


def parse_verify_data(verify_data: str) -> Tuple[int, str] or None:
    '''인증 데이터를 파싱합니다.
    '''
    try:
        vi = verify_data.find('_')
        if (vi < 1):
            return None
        return (int(verify_data[0:vi], 16), verify_data[vi+1:])
    except:
        return None


def make_verify_url(user_id: int, verify_code: str, redirect_url: str) -> str:
    '''인증 주소를 만듭니다.
    '''
    query = urlencode({
        'vc': make_verify_data(user_id, verify_code),
        'r': redirect_url
    })

    return urljoin(env.server_url, f"/auth/email_verify?{query}")


def send_verify_email(id: int, email: str, verify_code: str or None, redirect_url: str = "") -> bool | None:
    '''인증코드를 발신합니다.

    Args:
        verify_code: None 이면 새로운 인증코드를 생성합니다.

    Returns:
        None: sql 오류
        True: 발송됨
        False: 발송 실패
    '''
    # 인증코드 생성
    if verify_code == None:
        verify_code = refresh_verify_code(id)
    if (verify_code == None):
        return None
    # 메일 내용 생성
    content = create_email_content(id, verify_code, redirect_url)
    # 메일 전송
    return send_email(content, email)


def create_email_content(user_id: int, vef_id: str, red_url: str = "") -> MIMEText:
    msg = MIMEText(f"인증 ㄱ {make_verify_url(user_id, vef_id, red_url)}")
    msg['Subject'] = "회원가입 인증"
    return msg
