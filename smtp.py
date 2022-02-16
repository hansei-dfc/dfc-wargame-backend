import smtplib
from email.mime.text import MIMEText
import env

def make_connection():
    '''smtp 연결을 만들고 로그인합니다.
    '''
    smtp = smtplib.SMTP(env.smtp_server, env.smtp_port)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(env.smtp_user, env.smtp_pass)
    return smtp


def send_email(mime: MIMEText, to: str) -> bool:
    '''smtp 연결하고 보냅니다.

    Args:
        mime: 내용
        to: 수신자
    '''
    try:
        smtp = make_connection()
        smtp.sendmail(env.smtp_server, to, mime.as_string())
        smtp.quit()
        return True
    except:
        return False
